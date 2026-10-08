# macOS DPCD address-boundary control

Read-only run completed with exit 0. No configuration, DPCD or flash writes. Receiver RC enable/disable and memory reads were used for observation.

| Source request | Receiver software request header | Match |
|---|---|---|
| 0x403 / 16 bytes | 0x403 / 16 bytes | True |
| 0xfe / 16 bytes | 0xfe / 16 bytes | True |
| 0xff / 9 bytes | 0xff / 9 bytes | True |
| 0x100 / 8 bytes | 0x500 / 16 bytes | False |
| 0x101 / 7 bytes | 0x500 / 16 bytes | False |
| 0x107 / 1 bytes | 0x500 / 16 bytes | False |

Requests starting at 0xFE or 0xFF reached the observed firmware software request buffer. Requests starting at 0x100, 0x101 or 0x107 left the identity preflight 0x500/16 header in that buffer, consistent with earlier observations. This is repeatable across tested lengths, but does not prove absence of physical AUX traffic or identify host versus receiver hardware interception. Background requests can overwrite snapshots.

DPCD 0x403/16 returned zeros via the source API and matched the receiver software buffer. No “Virtua” identity marker was observed. This excludes that particular marker in this capture, not all virtualization.

Final receiver state: configuration 0x90000217=08, type 0x9000025B=0A, processing byte 0x9000080D=0B; port word 0x06600444, MSA-ignore mirror bit 12 clear.

Static DCP firmware investigation identified property name `virtual-dpcd` at VM 0x3059E7. At 0x58280–0x582E8 a property value is converted to address/value pairs in controller dictionary +0x2C0; device selection at 0x62368 consults this dictionary. Read-only live IODeviceTree and IOService searches exposed no `virtual-dpcd`, `no-virtual-display` or `EarlyDPCD600Override` property. Private firmware properties may not appear in host IORegistry, so this is inconclusive. No setters were called.
