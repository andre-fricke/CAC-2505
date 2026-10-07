// Read-only derivative of alexsorokoletov/vm7100tool_macos (MIT).
// Only one-byte volatile RAM change at 0x90000217. No flash/reset commands.
import Foundation
import IOKit
import IOKit.usb
import IOKit.hid
let VMM_VENDOR_ID: Int32 = 0x06CB
let VMM_PRODUCT_ID: Int32 = 0x7100
let HID_REPORT_SIZE = 62
enum RCCommand: UInt8 { case enableRC=0x01, disableRC=0x02, writeToMemory=0x21, readFromEEPROM=0x30, readFromMemory=0x31 }
func printErr(_ s:String) { fputs(s+"\n",stderr) }
func buildRCPacket(cmd: RCCommand, offset: UInt32 = 0, length: UInt32 = 0, data: Data = Data()) -> Data {
    var packet = Data(count: HID_REPORT_SIZE)
    packet[0] = 0x01 // Report ID
    packet[1] = 0x00
    let payloadLen = min(5 + 4 + 4 + data.count, 59)
    packet[2] = UInt8(payloadLen)
    packet[3] = 0x00
    packet[4] = 0x00
    packet[5] = cmd.rawValue | 0x80
    packet[6] = 0x00
    // Offset (LE)
    packet[7] = UInt8(offset & 0xFF)
    packet[8] = UInt8((offset >> 8) & 0xFF)
    packet[9] = UInt8((offset >> 16) & 0xFF)
    packet[10] = UInt8((offset >> 24) & 0xFF)
    // Length (LE)
    packet[11] = UInt8(length & 0xFF)
    packet[12] = UInt8((length >> 8) & 0xFF)
    packet[13] = UInt8((length >> 16) & 0xFF)
    packet[14] = UInt8((length >> 24) & 0xFF)
    // Data
    for i in 0..<min(data.count, 47) {
        packet[15 + i] = data[i]
    }
    return packet
}

protocol VMM7100Transport {
    func open() -> Bool
    func close()
    func sendReport(_ data: Data) -> Bool
    func readReport() -> Data?
    var isOpen: Bool { get }
}

class VMM7100HIDTransport: VMM7100Transport {
    var manager: IOHIDManager?
    var hidDevice: IOHIDDevice?
    var _isOpen = false
    var isOpen: Bool { _isOpen }

    func open() -> Bool {
        manager = IOHIDManagerCreate(kCFAllocatorDefault, IOOptionBits(kIOHIDOptionsTypeNone))
        guard let mgr = manager else { return false }

        let matchDict: [String: Any] = [
            kIOHIDVendorIDKey: VMM_VENDOR_ID,
            kIOHIDProductIDKey: VMM_PRODUCT_ID
        ]
        IOHIDManagerSetDeviceMatching(mgr, matchDict as CFDictionary)
        IOHIDManagerScheduleWithRunLoop(mgr, CFRunLoopGetCurrent(), CFRunLoopMode.defaultMode.rawValue)

        let openRet = IOHIDManagerOpen(mgr, IOOptionBits(kIOHIDOptionsTypeNone))
        guard openRet == kIOReturnSuccess else {
            if UInt32(bitPattern: Int32(openRet)) == 0xe00002c5 { // kIOReturnExclusiveAccess
                printErr("Device is busy — another process has exclusive access. Close other tools and retry.")
            } else {
                printErr("Cannot open HID manager (0x\(String(format: "%x", openRet)))")
            }
            return false
        }

        guard let deviceSet = IOHIDManagerCopyDevices(mgr) as? Set<IOHIDDevice>,
              let device = deviceSet.first else {
            printErr("VMM7100 not found. Is the adapter connected?")
            IOHIDManagerClose(mgr, IOOptionBits(kIOHIDOptionsTypeNone))
            return false
        }

        self.hidDevice = device
        _isOpen = true
        return true
    }

    func close() {
        if let mgr = manager {
            IOHIDManagerClose(mgr, IOOptionBits(kIOHIDOptionsTypeNone))
        }
        hidDevice = nil
        manager = nil
        _isOpen = false
    }

    func sendReport(_ data: Data) -> Bool {
        guard _isOpen, let device = hidDevice else { return false }
        var bytes = [UInt8](data)
        let ret = IOHIDDeviceSetReport(device, kIOHIDReportTypeOutput, 1, &bytes, bytes.count)
        return ret == kIOReturnSuccess
    }

    func readReport() -> Data? {
        guard _isOpen, let device = hidDevice else { return nil }
        var buffer = [UInt8](repeating: 0, count: HID_REPORT_SIZE)
        var length = buffer.count
        let ret = IOHIDDeviceGetReport(device, kIOHIDReportTypeInput, 1, &buffer, &length)
        guard ret == kIOReturnSuccess else { return nil }
        return Data(buffer.prefix(length))
    }
}


func run() -> Int32 {
let mode=Array(CommandLine.arguments.dropFirst())
guard mode == ["--enable"] || mode == ["--restore"] else {printErr("Use --enable or --restore; no device access performed.");return 4}
print("CAC-VRR-RAM-Test v1 — volatile configuration test")
let transport = VMM7100HIDTransport()
guard transport.open() else { return 1 }
defer { transport.close() }
func command(_ cmd: RCCommand,_ addr: UInt32,_ length: UInt32,_ payload: Data=Data()) -> Data? {
 guard transport.sendReport(buildRCPacket(cmd:cmd,offset:addr,length:length,data:payload)) else {printErr("Send failed");return nil}
 usleep(20000)
 for _ in 0..<10 {
  guard let r=transport.readReport(),r.count>=15 else {printErr("Read failed");return nil}
  if r[5] & 0x80 != 0 {usleep(10000);continue}
  print(String(format:"Reply cmd=%02X request=%08X: ",cmd.rawValue,addr)+r.map{String(format:"%02X",$0)}.joined(separator:" "))
  guard r[0]==1,r[5]==cmd.rawValue else {printErr("Wrong report/command echo; data NOT interpreted");return nil}
  if cmd == .enableRC {
   // Read-only commands can be attempted when the returned RC state is enabled.
   // Do not equate this with a successful enable result: report it explicitly.
   guard r[4]==1 else {printErr("RC channel is not enabled");return nil}
   if r[6] != 0 {print(String(format:"RC state is enabled; enable status=%02X (unresolved). Attempting reads with strict result checks.",r[6]))}
   return Data()
  }
  guard r[6]==0 else {printErr(String(format:"Command error=%02X; data NOT interpreted",r[6]));return nil}
  let echoedAddr=UInt32(r[7])|(UInt32(r[8])<<8)|(UInt32(r[9])<<16)|(UInt32(r[10])<<24)
  // Successful reads advance the address by the requested byte count.
  // RC enable/disable have no addressed memory target; their offset field
  // must not be used as a memory-address validation condition.
  if cmd == .enableRC || cmd == .disableRC { return Data() }
  if cmd == .writeToMemory { return Data() }
  guard echoedAddr==addr &+ length else {
   printErr(String(format:"Address echo mismatch: expected end %08X, got %08X; data NOT interpreted",addr &+ length,echoedAddr));return nil
  }
  let count=Int(length)
  guard count<=r.count-15 else {printErr("Short response");return nil}
  return r.subdata(in:15..<(15+count))
 }
 printErr("Timeout");return nil
}
defer { _ = command(.disableRC,0,0) }
guard command(.enableRC,0,5,Data("PRIUS".utf8)) != nil else {return 2}
let args=Array(CommandLine.arguments.dropFirst())
guard args == ["--enable"] || args == ["--restore"] else {
 printErr("Usage: CAC-VRR-RAM-Test --enable OR --restore; changes only RAM 0x90000217")
 return 4
}
let address:UInt32=0x90000217
guard let current=command(.readFromMemory,address,1), current.count==1 else {return 3}
let enabling=args == ["--enable"]
let expected:UInt8=enabling ? 0x08:0x48
let target:UInt8=enabling ? 0x48:0x08
if current[0]==target {print("Already at target; no write performed.");return 0}
guard current[0]==expected else {printErr(String(format:"Unexpected config %02X; no write performed.",current[0]));return 5}
if enabling {
 guard let flags=command(.readFromMemory,0x90000A78,2),flags.count==2 else {return 3}
 let value=UInt16(flags[0])|(UInt16(flags[1])<<8)
 guard value&0x100 != 0 else {printErr("TV VRR flag not set; no write performed.");return 6}
}
guard command(.writeToMemory,address,1,Data([target])) != nil else {return 7}
guard let after=command(.readFromMemory,address,1),after==Data([target]) else {
 printErr("Readback failed. RAM state not confirmed. Restore or power-cycle adapter.")
 return 8
}
print(String(format:"Verified RAM 0x90000217: %02X -> %02X. No flash write.",expected,target))
return 0
}
exit(run())
