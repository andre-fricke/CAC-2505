# macOS research — recognition achieved, working VRR unresolved

This directory preserves experimental CAC-2505 VRR work on an Apple M1 Pro Mac and LG 65QNED869QA, using vendor-supplied Apple/4K120 firmware **7.02.116**. It is **not a working macOS VRR installer**. The supported Steam Deck workaround is in `../steamdeck`.

## Most recent result — 8 October 2026

The comparison is now narrower: dynamic VRR worked on the J560J15 monitor both through CAC/HDMI from the Steam Deck and directly over USB-C from the M1 Pro Mac. Through CAC/HDMI from the Mac, selecting Variable still produced a black picture, including a verified RGB8 SDR mode without DSC. Stable macOS VRR remains unresolved.

Two passive AUX staging measurements did not capture the decisive DPCD0x107 request. The shorter run completed262 samples in8seconds without timeout, but the buffer is not a lossless bus trace. This does not prove the Mac failed to send that request. The user confirmed black output during the latest test and normal output after verified restoration.

See [the current comparison and measurement archive](evidence/J560-comparison-20261008/README.md) and [HANDOFF.md](HANDOFF.md). No new firmware, driver patch or macOS installer was produced.

## Contents

- `tools/`: source code for the actual diagnostic/test runners, Swift HID helpers and generated EDID test files. Firmware binaries are excluded.
- `evidence/`: console logs and LG-specific timing snapshots. Local home paths are anonymized; broad IORegistry dumps are not published.
- `notes/`: intermediate findings, including unsuccessful tests.

## Prerequisites and portability

These scripts target this exact setup and are research artifacts. They identify the LG by a **hardcoded BetterDisplay UUID**, specific to the original Mac installation. A different Mac must use its own identity and baseline EDID, with a reviewed backup/recovery path. Do not run the scripts unchanged on another setup.

Original setup: BetterDisplay 5.0.6 build53700 and `/opt/homebrew/bin/betterdisplaycli`, macOS system Python at `/usr/bin/python3`, Xcode Command Line Tools with `xcrun swiftc`, HID06CB:7100 and exact firmware7.02.116. Native IOKit/HID access was unavailable from the agent sandbox but worked from the user's iTerm session. Run only one hardware test at a time.

Build the three helper binaries on the Mac:

```bash
sh macos/tools/build.sh
```

The tests locate binaries and EDID files beside themselves. Generated logs and snapshots are written there too. The scripts use only whitelisted RAM writes; they do not flash firmware. Some older prompts still use `JA`; newer runners use `YES`. Review each runner's prompt and source before use.

## Current continuation boundary

No hardware test is pending. Earlier cache and signal captures listed in this archive have completed. There is currently no concrete new hardware-changing test justified by the latest results. Continue only from a new documented/code-supported hypothesis or a supported trace that can distinguish actual AUX reception from source/API reporting. Do not interpret missing staging samples as missing bus transactions or force an internal status bit as a substitute for the firmware handler.

## Recovery caveat

The hotplug test restored RAM08/0A, requested factory EDID, cleared custom EDID and disabled auto-apply. However, the returned factory EDID changed interface bytes from initial1.4/85 to1.3/80, with a valid checksum. The strict original-byte comparison therefore failed. Its independent watchdog finished and encountered the same mismatch. A restored picture is confirmed; exact restoration to the initial EDID bytes is not. Do not repeatedly run that unchanged test: its original-EDID precondition and recovery assertion need review against the newly captured baseline.

## Provenance

The Swift HID helpers identify themselves as derivatives of [alexsorokoletov/vm7100tool_macos](https://github.com/alexsorokoletov/vm7100tool_macos), an MIT-licensed project. This archive is not a vendor firmware release. No license to redistribute vendor firmware is asserted.


Research update, 8 October 2026: TV No Signal persists even with verified physical 720p RGB8 SDR VRR without DSC. See HANDOFF.md and dated evidence. Added tools are bounded diagnostic experiments, not a working macOS solution. The native 720p EDID is a temporary host override. The Signal-Diagnose runner is prepared but has not yet been run.
