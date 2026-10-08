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

## Latest continuation: post-hotplug snapshot completed

The previously pending read-only command was executed. See `evidence/Post-hotplug-current/REPORT.md` and accompanying data. Confirmed RAM08/0A, auto-applyoff, identicalOS/I2CEDID with valid1.3/80 factoryheader and SHA256fcb048faa03baf2d3c106f2b0b1cd191df1557322022c94ab8c48b39488a57b0. macOSVRRsupport remainsTRUE, range48–120, continuousNone. Currentfixed4K60SDR8-bitYCbCr444limited,DSCNo. No further variable-rate attempt was performed. The previous next-step request to read the snapshot is now complete; proceed with safe fixed-mode-recovery-first diagnostic design. New factorybaseline must be explicitly backed up and validated, not silently substituted into older tests.


## Update: 8 October 2026


The adapter still runs the unmodified Apple firmware 7.02.116. No firmware or driver patch was installed.

| Comparison | Verified physical signal | User observation |
| --- | --- | --- |
| System Settings Variable | 3840x2160, maximum 120 Hz, YCbCr420, 8-bit SDR, DSC enabled | No Signal |
| Native 720p Variable | 1280x720, maximum 60 Hz, RGB, 10-bit SDR, DSC disabled | No Signal |
| Compatible 720p Variable RGB8 | 1280x720, maximum 60 Hz, RGB, 8-bit SDR, DSC disabled | No Signal |

The 720p RGB8 state was verified in two snapshots: Variable Refresh Rate Yes, DPCD 0x107=80, 0x160=00, DP lane status 77/77, alignment 01. HDMI 0x3036=00 and 0x303B=03; TX active/ready flags do not establish a visible valid image. Consequently, HDR, 10-bit color, DSC and 4K bandwidth are not individually necessary explanations for this failure. This does not exclude interactions at the target 4K120 HDR mode or diagnose the exact failed packet/timing path.

A normal desktop resolution selection did not produce a physical 720p signal. A temporary host EDID override with native 720p was needed. Its preferred timing is 74.25 MHz, totals 1650x750, 60 Hz. It retains actual HDMI Forum VRR capability 48–120 Hz and advertises a general range of 48–60 Hz. It removes 4K video codes and related mappings. Structural boundaries, timing and both checksums were checked; full edid-decode conformance was not verified. It is a diagnostic EDID, not a production configuration.

Recovery after the latest RGB8 test verified fixed 4K60 RGB8 SDR without DSC, RAM 0x90000217=08 and 0x9000025B=0A, and identical known factory OS/I2C EDID. Process exit 0; independent recovery guard terminated. Earlier runs sometimes needed a USB-C power cycle to restore a visible picture.

## Historical prepared measurement (subsequently completed)

CAC-Mac-Signal-Diagnose-Test.py repeats the bounded, already tested 720p RGB8 comparison with additional read-only instrumentation: exact active DCP timing and color IDs matched to TimingElements, plus adapter port status, packet-path gate, counters and shared scratch buffer before/during/after. The scratch buffer is reused and cannot prove current HDMI packet transmission. The firmware read helper verifies version 7.02.116. No additional write addresses or driver changes are introduced. Independent recovery is scheduled after 420 seconds; normal execution ends earlier.

The objective is a concrete source-timing versus adapter-state comparison, not another arbitrary mode change. User must run via iTerm because agent sandbox device access fails. All results remain research evidence; functioning macOS VRR has not been achieved.

HID busy polling was extended from 10 to 100 iterations; inspect/restore retries are bounded, enable is not retried. Recovery now evaluates the final fixed-mode state after factory cleanup. Git email globally and locally is fricke.andre@gmail.com, as requested by the user; prior six commits were rewritten.


## Latest update: 8 October 2026, after AUX controls

See notes/AUX-path-investigation-20261008.md and the new derived evidence folders. Earlier prepared signal-diagnostic and subsequent controls have completed. Current user-confirmed state is stable fixed4K120HDR after full USB-C power cycle. The two known RAM values alone and HDMI re-enumeration did not resolve the Mac read-path difference. There is no currently armed test or recovery watchdog, no patched firmware, and no confirmed macOS VRR fix. Next work is localization of the AUX response discrepancy; no additional hardware-changing experiment is yet justified.

## Current handoff: J560 controls and short AUX capture completed

The latest authoritative state is in [J560-comparison-20261008](evidence/J560-comparison-20261008/README.md). Direct Mac USB-C VRR and Deck/CAC HDMI VRR were visually positive on J560. Mac/CAC HDMI Variable remains black even with RGB8 SDR and no DSC. The latest user confirmed picture returned after the test; RAM08/0A, factory OS EDID and cleared override were verified restored. These J560 settings are SDR, not the LG4K120HDR baseline described earlier.

The28-second sampler terminated after about16seconds with a timeout. A subsequent8-second single-buffer sampler completed262 reads, exit0. Neither observed00107; neither is a complete wire trace. Source connection reports fell back from Variable to fixed, and the user observed black output during the latest Variable interval.

Static firmware and DCP findings are archived with offsets and uncertainty. DPCD2214 is tied to the RAM217 capability bit; the DCP consumes its bit0 in a broader feature decision involving Panel Replay and Autonomous FRL. This is not a proven VRR activation switch or failure cause. No new configuration bytes, firmware image or installer should be inferred from this work. There is no prepared next hardware test; further identical mode/RAM trials are not a justified next step.
