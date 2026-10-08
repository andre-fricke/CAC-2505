# macOS research — recognition achieved, working VRR unresolved

This directory preserves experimental CAC-2505 VRR work on an Apple M1 Pro Mac and LG 65QNED869QA, using vendor-supplied Apple/4K120 firmware **7.02.116**. It is **not a working macOS VRR installer**. The supported Steam Deck workaround is in `../steamdeck`.

## Most recent result

After applying two known volatile RAM settings and physically reconnecting **HDMI only while leaving USB-C powered**, macOS offered a variable refresh rate. Its display attributes reported VRR support and 51 timing dictionaries had nonzero variable ranges. Selecting the variable rate caused the TV to show **No Signal**. The user later confirmed the picture returned.

Evidence, limitations and the exact next step are in [HANDOFF.md](HANDOFF.md). [The breakthrough report](evidence/Hotplug-breakthrough.md) records the successful recognition sequence and unsuccessful output activation.

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

## Current safe next action

For the original user's setup, the next pending command is **read-only**:

```bash
/usr/bin/python3 macos/tools/CAC-Mac-Cache-Lesen.py
```

It captures current EDID/custom-EDID status, display modes, DPCD, RAM values and registry data. Its full output stays local and should be reviewed before sharing. The last instruction was issued before this repository snapshot; the subsequent post-hotplug capture is now complete; see `evidence/Post-hotplug-current/REPORT.md`.

## Recovery caveat

The hotplug test restored RAM08/0A, requested factory EDID, cleared custom EDID and disabled auto-apply. However, the returned factory EDID changed interface bytes from initial1.4/85 to1.3/80, with a valid checksum. The strict original-byte comparison therefore failed. Its independent watchdog finished and encountered the same mismatch. A restored picture is confirmed; exact restoration to the initial EDID bytes is not. Do not repeatedly run that unchanged test: its original-EDID precondition and recovery assertion need review against the newly captured baseline.

## Provenance

The Swift HID helpers identify themselves as derivatives of [alexsorokoletov/vm7100tool_macos](https://github.com/alexsorokoletov/vm7100tool_macos), an MIT-licensed project. This archive is not a vendor firmware release. No license to redistribute vendor firmware is asserted.


Research update, 8 October 2026: TV No Signal persists even with verified physical 720p RGB8 SDR VRR without DSC. See HANDOFF.md and dated evidence. Added tools are bounded diagnostic experiments, not a working macOS solution. The native 720p EDID is a temporary host override. The Signal-Diagnose runner is prepared but has not yet been run.
