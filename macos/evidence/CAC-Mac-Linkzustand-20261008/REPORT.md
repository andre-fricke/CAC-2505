# Apple link-training state, fixed 4K120 HDR

Read-only capture completed with exit 0. IODPDeviceGetLinkTrainingData (selector 2, 0x98-byte output) returned success. Apple formatter reports 4 lanes, 8.1 Gbit/s per lane, enhanced mode enabled, downspread disabled, fast training disabled, FEC enabled, PSR disabled, swing voltage 2 and pre-emphasis 0 on all lanes.

Source DPCD 0x107 reads 00. Receiver processing byte 0x9000080D=0B; port status 0x06600444, bit12 clear; configuration 08/type0A. This describes current fixed operation and does not prove the cause of VRR failure. The getter has no MSA-ignore/VRR field in the inspected formatter.

Additional static check: native AUX header emitter in installed DCP VM 0x5DD88–0x5DDEC writes length and full address bytes to controller offsets 0x794/0x798/0x79C/0x7A0. No special branch for 0x100–0x107 is present in that emitter. This does not establish which runtime device implementation invokes it.

Prepared next observation: adapter control registers 0x20230000, 0x2023001C, 0x20230068, 0x20230074. Each is read by the firmware itself: ROM 0x8CAC, 0x8C6E/0x245DA/0x24780, 0x8C82, 0x8C42 respectively. Reader contains only RC enable/disable and commands 0x30/0x31, verifies firmware 7.02.116, validates reply status/end address. It contains no memory-write command. Register meanings remain undocumented; read values are for comparison, not an instruction to modify them.
