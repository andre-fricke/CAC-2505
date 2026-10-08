// Read-only derivative of alexsorokoletov/vm7100tool_macos (MIT).
// No flash, reset or memory-write commands.
import Foundation
import IOKit
import IOKit.usb
import IOKit.hid
let VMM_VENDOR_ID: Int32 = 0x06CB
let VMM_PRODUCT_ID: Int32 = 0x7100
let HID_REPORT_SIZE = 62
enum RCCommand: UInt8 { case enableRC=0x01, disableRC=0x02, readFromEEPROM=0x30, readFromMemory=0x31 }
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
print("CAC-HDMI-Zustand v1 — read-only")
let transport = VMM7100HIDTransport()
guard transport.open() else { return 1 }
defer { transport.close() }
func command(_ cmd: RCCommand,_ addr: UInt32,_ length: UInt32,_ payload: Data=Data()) -> Data? {
 guard transport.sendReport(buildRCPacket(cmd:cmd,offset:addr,length:length,data:payload)) else {printErr("Send failed");return nil}
 usleep(20000)
 for _ in 0..<100 {
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
guard let version=command(.readFromEEPROM,0x4000,4), version==Data([7,2,116,0]) else {printErr("Wrong firmware; no RAM reads");return 3}
let reads:[(RCCommand,UInt32,UInt32,String)] = [
 (.readFromMemory,0x90000217,1,"RAM config flags"),
 (.readFromMemory,0x9000028E,1,"Packet path config"),
 (.readFromMemory,0x900001CC,4,"Port packet counters"),
 (.readFromMemory,0x90000A60,32,"Port 0 status"),
 (.readFromMemory,0x90000E76,1,"Port timing-table/VIC candidate"),
 (.readFromMemory,0x90000E52,2,"Packet base refresh field"),
 (.readFromMemory,0x900011DC,32,"Packet scratch header and first 28 bytes"),
 (.readFromMemory,0x900011FC,4,"Packet scratch control")]

var failed=false
for (cmd,addr,n,label) in reads {
 if let d=command(cmd,addr,n) {
 print(label+String(format:" @ 0x%08X: ",addr)+d.map{String(format:"%02X",$0)}.joined(separator:" "))
 if addr==0x90000217 { print(String(format:"  Config bit 0x40: %@",d[0]&0x40 != 0 ? "set":"clear")) }
 if addr==0x90000A60 || addr==0x90000E9C {let status=UInt32(d[20])|(UInt32(d[21])<<8)|(UInt32(d[22])<<16)|(UInt32(d[23])<<24);print(String(format:"  Port status14=0x%08X; MSA-ignore mirror bit12=%@",status,status&0x1000 != 0 ? "set":"clear"));let flags=UInt16(d[24])|(UInt16(d[25])<<8); print(String(format:"  Port flags18=0x%04X; HDMI VRR mask 0x0100=%@",flags,flags&0x100 != 0 ? "set":"clear"))}
 if addr==0x900011DC {print(String(format:"  Packet scratch index7=0x%02X (raw bit0=%@); buffered data is NOT proof of current transmission.",d[11],d[11]&1 != 0 ? "set":"clear"))}
 }
 else {failed=true;printErr("Failed: "+label)}
}
return failed ? 3 : 0
}
exit(run())
