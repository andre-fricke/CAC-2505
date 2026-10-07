# Technical findings and test evidence

## Volatile configuration

Firmware: Apple/4K120 7.02.116. The helper writes only the following whitelisted bytes and verifies readback:

| RAM address | Original | Enabled | Observed effect |
|---|---|---|---|
| `0x90000217` | `08` | `48` | DPCD `0x00007` and `0x02207`: `81` → `C1`; `0x02214`: `00` → `03` |
| `0x9000025B` | `0A` | `02` | DPCD `0x00080..83`: `08 08 08 08` → `0B F0 1A FE`; HDMI converter presentation |

Changing only the first byte advertised capabilities but left DRM `vrr_capable=0`. With both changes and software detection, DRM `vrr_capable` and `passive_vrr_capable` became 1. KDE VRR Always or Gamescope `adaptive_sync 1` then resulted in the TV showing VRR ON.

The HID protocol is restricted to remote-control enable/disable, RAM read and the two RAM writes above. No flash-write command is allowed. AUX accesses read identity and capabilities. Debugfs writes request source-side display detection.

## Confirmed on 7 October 2026

- Steam Deck → CAC-2505 → LG 65QNED869QA, 4K120 HDR.
- Bounded 20-second operating test: VRR ON and stable picture.
- Animation submitted 58, 80 and 105 FPS in three six-second stages. User observed changing TV FPS, VRR remaining ON and a stable animation. Submission rates are not scanout measurements; exact TV readings were not recorded.
- Automatic Gaming activation after service update, reconnection and reboot.
- Automatic Desktop activation after reconnection, with KDE 4K120/HDR confirmed.
- Original configuration read as 08/0A on fresh connections before applying 48/02.

Sanitized service excerpts are in `evidence/`. They document this setup; they do not guarantee another firmware or display will behave identically.

## Implementation notes

The service polls for the exact adapter/TV identity, waits ten seconds for the connection to settle, applies the two bytes, requests software detection and enables session VRR. HID response polling is bounded to roughly one second; child workers also have execution timeouts. Transient AUX/EDID unavailability does not immediately discard ownership while USB HID remains present. Three polls with no HID device mark a disconnect.

Gamescope's process name on the tested image is `gamescope-wl`; session ownership is determined from its real UID. `gamescopectl help` writes its controls to stderr, and unknown commands can return exit status zero. Both output streams are checked, including the known `Command not found.` error.

Firmware binaries are intentionally excluded. The tested Apple fullrom SHA-256 was `8d4eb2e8473c1b3e88d18cfefaf5db6165ca20347bb4d676c043bc13e15fb73b`; the vendor supplied it directly. RAM offsets must not be treated as universally valid across other firmware versions.

## Suspend/resume follow-up

A short suspend initially disabled VRR while the helper still considered the connection active. The kernel logged a warning in `amdgpu_dm_handle_vrr_transition`. A duration-only detector with a one-second threshold missed a short sleep; the kernel suspend-success counter subsequently detected it. Recovery restored 08/0A, reapplied 02/48 and re-enabled session VRR. Desktop recovery completed at 22:58:14 and Gaming recovery at 23:00:27. The user observed VRR returning automatically in both tests. See the two suspend evidence logs. The warning does not establish why the Deck woke automatically.

## Shorter resume path

After successful restoration, the helper skips the second ten-second settling delay only when adapter/connector and session still match. Initial connection keeps the delay. Both Desktop and Gaming recovered in 18 seconds from logged resume detection to activation; evidence is in the two `Suspend-Kurz` logs. The user confirmed both tests succeeded.
