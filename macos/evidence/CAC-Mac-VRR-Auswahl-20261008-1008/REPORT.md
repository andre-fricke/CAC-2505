2026-10-08: Native macOS variable refresh selection measured.

User reports No Signal during VRR, still no picture after software restoration. Selected and settled snapshots report physical 3840x2160 at approximately 120Hz, YCbCr420 limited 8-bit SDR, Variable Refresh Rate Yes, DSC enabled (DPCD 0x160=01), MSA ignore enabled (0x107=80). This is NOT a 4K60/no-DSC VRR test: selecting Variable changed physical connection mode. HDMI TX status 0x303B=03 in both samples; active/ready bits do not establish a visible valid image. 0x3036 C1 then 85.

Cleanup verified RAM217=08 and RAM25B=0A and equal known factory OS/I2C EDID. Final fixed4K60 RGB8 SDR/no DSC verified by reports but user still sees no image. Initial hdr=off request failed; retained transient error prevented marking recovery successful and left watchdog scheduled. Safe restart required to stop guard and fully power-cycle USB-C. No firmware write.

Subsequent full USB-C power cycle and read-only capture CAC-Mac-Cache-20261008-101028 confirmed original RAM08/0A, original identical OS/I2C EDID, fixed4K60 RGB10 SDR without DSC. Variable timing table includes maximum60Hz/minimum48Hz entries; exact available connection-mode selectors remain to be captured.
