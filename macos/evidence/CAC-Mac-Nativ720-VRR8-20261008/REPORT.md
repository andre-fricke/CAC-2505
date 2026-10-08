# macOS VRR investigation, 8 October 2026

The adapter still runs the unmodified Apple firmware 7.02.116. No firmware or driver patch was installed.

| Comparison | Verified physical signal | User observation |
| --- | --- | --- |
| System Settings Variable | 3840x2160, maximum 120 Hz, YCbCr420, 8-bit SDR, DSC enabled | No Signal |
| Native 720p Variable | 1280x720, maximum 60 Hz, RGB, 10-bit SDR, DSC disabled | No Signal |
| Compatible 720p Variable RGB8 | 1280x720, maximum 60 Hz, RGB, 8-bit SDR, DSC disabled | No Signal |

The 720p RGB8 state was verified in two snapshots: Variable Refresh Rate Yes, DPCD 0x107=80, 0x160=00, DP lane status 77/77, alignment 01. HDMI 0x3036=00 and 0x303B=03; TX active/ready flags do not establish a visible valid image. Consequently, HDR, 10-bit color, DSC and 4K bandwidth are not individually necessary explanations for this failure. This does not exclude interactions at the target 4K120 HDR mode or diagnose the exact failed packet/timing path.

A normal desktop resolution selection did not produce a physical 720p signal. A temporary host EDID override with native 720p was needed. Its preferred timing is 74.25 MHz, totals 1650x750, 60 Hz. It retains actual HDMI Forum VRR capability 48–120 Hz and advertises a general range of 48–60 Hz. It removes 4K video codes and related mappings. Structural boundaries, timing and both checksums were checked; full edid-decode conformance was not verified. It is a diagnostic EDID, not a production configuration.

Recovery after the latest RGB8 test verified fixed 4K60 RGB8 SDR without DSC, RAM 0x90000217=08 and 0x9000025B=0A, and identical known factory OS/I2C EDID. Process exit 0; independent recovery guard terminated. Earlier runs sometimes needed a USB-C power cycle to restore a visible picture.

## Next prepared measurement, not yet run

CAC-Mac-Signal-Diagnose-Test.py repeats the bounded, already tested 720p RGB8 comparison with additional read-only instrumentation: exact active DCP timing and color IDs matched to TimingElements, plus adapter port status, packet-path gate, counters and shared scratch buffer before/during/after. The scratch buffer is reused and cannot prove current HDMI packet transmission. The firmware read helper verifies version 7.02.116. No additional write addresses or driver changes are introduced. Independent recovery is scheduled after 420 seconds; normal execution ends earlier.

The objective is a concrete source-timing versus adapter-state comparison, not another arbitrary mode change. User must run via iTerm because agent sandbox device access fails. All results remain research evidence; functioning macOS VRR has not been achieved.
