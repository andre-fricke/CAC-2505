// Derived from alexsorokoletov/vm7100tool_macos (MIT).
// Experimental tool: inspect source for the whitelisted volatile RAM writes. No flash-write operation.
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
              deviceSet.count == 1, let device = deviceSet.first else {
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
guard mode == ["--inspect"] || mode == ["--enable"] || mode == ["--restore"] else {printErr("Use --inspect; read-only.");return 4}
print("CAC-Mac-Typ-RAM — two-byte volatile test")
let transport = VMM7100HIDTransport()
guard transport.open() else { return 1 }
defer { transport.close() }
func command(_ cmd: RCCommand,_ addr: UInt32,_ length: UInt32,_ payload: Data=Data()) -> Data? {
 if cmd == .writeToMemory {
  guard length==1, (addr==0x90000217 && (payload==Data([0x08]) || payload==Data([0x48]))) || (addr==0x9000025B && (payload==Data([0x0A]) || payload==Data([0x02]))) else {printErr("Forbidden write");return nil}
 }
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
guard let version=command(.readFromEEPROM,0x4000,4),version==Data([7,2,116,0]) else {printErr("Wrong firmware");return 3}
let pairs:[(UInt32,UInt8,UInt8)]=[(0x90000217,0x08,0x48),(0x9000025B,0x0A,0x02)]
if mode == ["--inspect"] {
 for (address,_,_) in pairs {
  guard let value=command(.readFromMemory,address,1) else {return 3}
  print(String(format:"RAM %08X = %02X",address,value[0]))
 }
 return 0
}
// Validate both bytes before the first write. Restore permits either known state.
for (address,original,test) in pairs {
 guard let value=command(.readFromMemory,address,1),value.count==1 else {return 3}
 guard value[0]==original || (mode == ["--restore"] && value[0]==test) else {printErr("Unexpected RAM state");return 5}
}
var failed=false
let ordered=mode == ["--enable"] ? Array(pairs.reversed()):pairs
for (address,original,test) in ordered {
 let target=mode == ["--enable"] ? test:original
 guard command(.writeToMemory,address,1,Data([target])) != nil,
       let value=command(.readFromMemory,address,1),value==Data([target]) else {
  failed=true
  if mode == ["--enable"] {break}
  continue
 }
 print(String(format:"VERIFIED RAM %08X = %02X",address,target))
}
return failed ? 8:0
}
exit(run())
