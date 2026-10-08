# Controlled software DPCD read-shadow marker

User reports stable picture. Test exit 0. Normal restoration verified RAM9000080D=0B; independent guard stopped. Original RAM217=08 / RAM25B=0A and source DPCD107=00 were confirmed after cleanup. No flash/MMIO/DPCD/display-mode/EDID writes.

## Intervention and result

One volatile flag was changed: RAM9000080D 0B -> 8B -> 0B. This bit normally mirrors DPCD107 bit4 in the firmware software path; it is not MSA-ignore bit7 or a VRR-enable control.

During verified8B:

- Source API single read107h: 00. Software request buffer retains preceding500h identity request.
- Source API read0FFh/16: 00 1E 84 00 02 02 02 02 00 00 00 00 00 00 00 00.
- Adapter software buffer: header90 00 00 FF 0F, payload00 1E 84 00 02 02 02 02 **10** 00 00 00 00 00 00 00. Byte8 of the payload corresponds to107h.
- Port status RAMA74 remained06600444; MSA-ignore mirror bit12 remained clear.

## Conclusion

The controlled marker establishes a discrepancy between the adapter software-generated response buffer and the source API result for the same crossing request. The firmware read-handler interpretation is experimentally supported by the marker changing only the predicted software response byte. This is stronger than comparing unrelated state snapshots.

It does not identify where the value is replaced: adapter autonomous response hardware, host-side AUX/controller processing, or later host software remain possible. The buffer is not a physical bus capture, and no end-to-end macOS VRR success has occurred. Do not label this conclusively a host cache bug.

Offline DCP read code includes a post-read AUX tracing callback at0x5F1B4–0x5F1E0. The identified callback0xE52DC and helper0xE53A0 copy the passed data into a ring buffer; inspected code does not write back into the caller data. This is a trace logger, not evidence of a modifying filter. Native readworker copies receiver FIFO bytes at0x5F0F0–0x5F10C. Runtime class/path selection remains unresolved.
