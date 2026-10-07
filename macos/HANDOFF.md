# Handoff — 7 October 2026, Europe/Berlin

## Objective and constraints

Achieve stable real dynamic VRR on Mac → CAC-2505 → LG at4K120 HDR. Steam Deck already solved with root auto-helper, reconnect/boot/short-resume verified in both modes. No adapter flashing or firmware changes. User rejected kernel/driver modification risk; no new arbitrary RAM or DPCD writes. User prefers autonomous analysis, concise progress logging, and saved command output instead of pasting. macOS UI is English. User runs native hardware-access scripts in iTerm; agent reads output files.

## Original workspace and repository

Original working directory: `/Users/mainuser/Documents/Codex/2026-10-07/referenced-chatgpt-conversation-this-is-an`; all original tools/results in `outputs`, disassembled firmware and analysis in `work`. Repository: `/Users/mainuser/git/CAC-2505`, remote `git@github.com:andre-fricke/CAC-2505.git`, branch main. Raw broad IORegistry captures and binaries remain in original workspace; this folder includes relevant source and derived evidence.

## Known hardware and firmware

M1 Pro MacBook ProA2485. CAC-2505 Synaptics VMM7100A1, USB06CB7100, DP branch90CC24/SYNAq. LG65QNED869QA, LGTVSSCR2, EDIDmanufacturer/product1E6D:0001. Apple firmware7.02.116 flashed earlier by user. Stock7.01.124 and Apple were both supplied directly by Wiktor/Club3D. Fullrom files are1MiB each, two duplicated banks; no patched firmware created.

Apple SHA256:8d4eb2e8473c1b3e88d18cfefaf5db6165ca20347bb4d676c043bc13e15fb73b.
Stock SHA256:08b9b6d6cba65002dca0f2760149257041f5b9eee4594662a90bd78d0d8f3935.

## Working Deck settings / Mac experimental settings

RAM90000217:08→48 enables advertised MSA-ignore and adaptive-sync-SDP support: DPCD7/2207= C1 vs81,2214=03 vs00.
RAM9000025B:0A→02 changes detailed downstream DPCD80..83 from08080808 to0BF01AFE (HDMI). This bit also gates EDID interface rewriting in Apple ROM13162–13178; do not consider it solely a type flag.

## Mac tests so far

1. RAM48/02 plus software reinitialize: stable picture, no native VRR option.
2. EDID continuous-frequency feature only: OS adopted it and parsed CVTv1X, VRR still false.
3. RAM48/02 + continuous EDID: VRR false.
4. Add general EDIDrange48–120 instead24–120: OS parsed48–120, VRR false.
5. Attempt1080p: logical/HiDPI and even listed non-HiDPI choices kept physical4K withDSC. Cannot count these as no-DSC tests. Direct resolution setter failed and cleanup succeeded.
6. Explicit offered4K60 SDR8-bit mode: verified physical4K60, HDRoff, DSCNo, stillVRRfalse. Active HDR/DSC are not sufficient explanations.
7. KeepRAM25B0A detailedDP and set21748 with same EDID, uncompressed4K60: stillVRRfalse.
8. Registry before/during/after48/02 + EDID: attributes updated24–120→48–120, ContinuousNone→CVTv1X, timing dict count71→73→71, but allVRRranges0 and supportfalse. EDID attributes were regenerated, complete DPCD-cache freshness remained unknown.
9. **Physical HDMI hotplug while USB-C stays powered** afterRAM48/02, verify RAM survives, apply same temporary EDID: macOS supportTRUE,70 timing dicts,51 with nonzeroVRRrange. User saw variable rate in System Settings and selected it, TV thenNoSignal. Picture later returned. Recognition achieved, functional output unresolved.

## Latest cleanup

Hotplug log verifies21708,25B0A restored, CLI auto-applyoff/factoryapply/customclear all exit0. FactoryEDID differs from initial only at13:04→03,14:85→80,checksum7F:E5→EB; both blocks checksumvalid. Strict ORIGINAL equality failed. Independent watchdog subsequently finished, repeating successful RAM/CLI cleanup and same equalityfailure. User confirmed pictureback. Do not claim exact originalEDID restoration. New current snapshot requested but still pending.

Initial EDID SHA256bf2274a4e755af146ce21b7233a62898734c1b99475e641af8d9c29825f3db70.
Original fixed display mode before hotplug was4K60 SDR8-bit. User's exact selected variable mode and failure-time DSC/FRL/stream values were NOT captured: reports occurred before selection. Do not assume a4K120HDR VRR attempt.

## Immediate next step

Read results of `CAC-Mac-Cache-Lesen.py` once user runs it. In original workspace it writes timestamped cache folder and `CAC-Mac-Cache-latest-path.txt`; read current customEDID,autoApply,OS/I2CEDID,VRRcapability,mode,DSC,DPCD,RAM and timing tables. Preserve new baseline and repair future preflight/cleanup to account for documented factoryEDID changes, without blindly accepting arbitrary EDIDs.

Then prepare a bounded test that captures source-side current mode/VRRrange,DSC,DP MSA-ignore control0x107,HDMI link3036/303B and timing snapshot AFTER variable selection, with confirmed fixed-mode recovery BEFORE reverting adaptercapabilities. The previous script restores RAM while the user may have selectedVRR: it lacks explicit fixed-mode rollback. Fix that sequencing before reproducingNoSignal. Use only known mode selections and RAM addresses. Prefer beginning with a verified low-bandwidth SDR mode rather than immediately4K120HDR. Capture exact requested and active variable range. Do not jump tofirmwarepatching.

Physical hotplug succeeded where reinitialize alone did not; contribution ofhotplug,EDID and typebytes isnotisolated. Avoid claiming proven driverblock or definitive cachebug. Earlier manualDCPforcing attempts were unreliable (someNoSignal); do not repeat without reviewing prior `outputs/HDMI-FRL-Befund.md` and recovery design.

## Corrected DPCD decoding

BetterDisplay labels coarseDPCD5=1D reserved, but Linuxdrm_dp.h mask06 givesTMDS04; present/conversion/detailed bitsset. AppleROM8F84 and stockROM8BA8 hardcode1D in DPCD5 response. Not anApple-only difference, not evidence ofmalformedcapability. Cached fullDPCD isnotexposed in collectedregistry. Source: https://raw.githubusercontent.com/torvalds/linux/master/include/drm/display/drm_dp.h.

## Evidence and source safety

`evidence/Hotplug-timing-before.json` vsduring; `Hotplug-breakthrough.md`; hotplug main/watchdoglogs. Macmainlogs anonymizedhomepath and nullbytes represented as literal\0; originals remain in workspace. Sources retain exacttestedbehaviour, including recovery limitation; repositorytools are not turnkey generalMacsupport. Use originalworkspacebinaries unlessrebuildnecessary. Firmwarebinaries excluded.
