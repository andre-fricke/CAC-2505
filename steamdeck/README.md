# Steam Deck installation

## Supported setup and prerequisites

- Club 3D CAC-2505 / Synaptics VMM7100, USB HID `06CB:7100`, branch identity `90CC24/SYNAq`, already running Apple/4K120 firmware **7.02.116**.
- Tested TV: LG 65QNED869QA, EDID manufacturer/product bytes `1e 6d 01 00` (LG `1E6D:0001`). Other identities are intentionally ignored. Do not bypass this check merely to try another TV.
- An HDMI connection that already works at 4K120 HDR, and VRR enabled on the TV.
- SteamOS with Python 3, Python `hid` module, `kscreen-doctor`, `gamescopectl`, accessible DRM AUX devices and the debugfs `trigger_hotplug` interface. Tested kernel: `7.2.7-valve1-1-neptune-72-gc8730d37f9c6`, KDE Wayland.
- A sudo password for the `deck` user. Installation requires root access; normal use does not require commands.

Check these from a Deck terminal or SSH before installing:

```bash
/usr/bin/python3 -c 'import hid; print("Python HID dependency available")'
command -v kscreen-doctor gamescopectl
sudo test -e /sys/kernel/debug/dri/0/DP-1/trigger_hotplug
```

A missing dependency or debugfs interface means this setup is not ready. The service does not install packages or unlock the SteamOS system partition. If `hid` is missing, the required Python distribution is `hidapi` (import name `hid`); it must be available to **/usr/bin/python3 running as root**, not just a user virtual environment. Package installation on an otherwise different SteamOS image has not been validated here. Do not assume a successful user-level pip installation makes the root service ready.

The helper currently assumes user `deck` has UID/GID 1000 and display connector `DP-1` uses `/sys/kernel/debug/dri/0`. AUX discovery itself is dynamic. Different layouts require review before installation.

## Get the files onto the Deck

Clone this repository on the Deck, or copy the entire `steamdeck` directory there. For example, from another computer with working SSH:

```bash
scp -r steamdeck deck@STEAM_DECK_IP:/home/deck/CAC-Deck-Automatik
```

Replace `STEAM_DECK_IP` with your Deck's address. The examples below assume the resulting directory is `/home/deck/CAC-Deck-Automatik`. If you clone directly, run the scripts from your clone's `steamdeck` directory instead.

Connect HDMI to the adapter **first**, then plug USB-C into the Deck. Start with a working picture. In Gaming Mode, select 3840×2160 at 120 Hz and HDR once in Steam's display settings. The service enables VRR there; it does not force Gamescope resolution or HDR. In Desktop Mode it explicitly requests 4K120, HDR and VRR Always.

## Install once

```bash
cd /home/deck/CAC-Deck-Automatik
sha256sum -c SHA256SUMS.txt
sudo python3 install.py
```

Review the printed description and type `YES` to install. The installer enables a boot service. Wait roughly 30 seconds for the picture to settle; a brief black screen during display detection is possible.

The service installs root-owned files under `/var/lib/cac2505-vrr` and its unit under `/etc/systemd/system/cac2505-vrr.service`. It refuses to overwrite an existing installation. No firmware, kernel or graphics driver is installed or modified.

## Daily use and verification

Connect HDMI first, then USB-C; wait about 30 seconds. No terminal command is needed after plugging in or rebooting. The service handles Desktop and Gaming sessions.

On the LG Game Optimiser overlay, check **VRR ON** and varying FPS. At an idle Desktop the TV may report around 48 FPS and rise to 120 while moving the pointer. A static 120 FPS reading alone is not proof of dynamic VRR.

```bash
systemctl is-enabled cac2505-vrr.service
systemctl is-active cac2505-vrr.service
journalctl -b -u cac2505-vrr.service --no-pager
```

Successful logs include `Activated desktop session` or `Activated gaming session`, with capabilities `0x7=c1`, `0x80=0bf01afe`, `0x2214=03`. Desktop also reports `3840x2160@120`, `hdr: true`, `vrrPolicy: 1`. Capabilities alone do not prove the TV is receiving dynamic refresh; verify its overlay and picture as well.

## Recovery, stop and removal

If activation fails, inspect the logs. The service attempts to restore the original RAM configuration and blocks repeated activation for that connection/session. Do not run manual RAM-test scripts alongside it.

If the picture does not return, disconnect USB-C for at least ten seconds to power-cycle the adapter. Reconnect HDMI first, then USB-C. To prevent another activation, stop the service before reconnecting:

```bash
sudo systemctl stop cac2505-vrr.service
```

Stopping attempts to disable VRR, restore RAM and request display detection. It does not restore the previous Desktop resolution or HDR preference. A stopped service starts again on the next boot unless disabled:

```bash
sudo systemctl disable --now cac2505-vrr.service
```

Remove the service:

```bash
sudo python3 /home/deck/CAC-Deck-Automatik/install.py --remove
```

Removal retains `/var/lib/cac2505-vrr` for inspection. The installer refuses to reinstall while that directory exists; after reviewing it, move it aside before a fresh installation. The adapter RAM changes disappear when it loses power.

## Update an existing installation

Copy a complete newer package to the same staging directory, then:

```bash
sudo python3 /home/deck/CAC-Deck-Automatik/update.py
```

This checks the manifest, stops the service, backs up the previous adapter/helper scripts and restarts with the new scripts. The current updater updates those scripts only; changes to the service unit require separate review.

## Limits

Verified: reconnect in both modes, Gaming → Desktop switch, Gaming autostart after reboot, stable picture and changing TV FPS. Automatic VRR recovery after short suspend/resume was also verified in Desktop and Gaming modes. Long-term stability, other TVs and future SteamOS versions remain untested. Small refresh-related brightness changes were observed on the tested TV; their cause was not established.

The checksums detect accidental changes to package files; they are not a signature or proof of publisher authenticity. Review root-executed scripts before installing. No third-party firmware binary or redistribution permission is supplied here.

## Suspend/resume recovery

The helper detects completed suspend cycles using the kernel suspend-success counter, with a BOOTTIME/MONOTONIC fallback. After resume it waits ten seconds and makes one recovery attempt: restore the owned RAM configuration, request detection, then activate again through the normal verified path. If the same connection and session are still present after verified restoration, the second ten-second activation wait is skipped; reconnect activation keeps its full settling delay. Allow about 20–25 seconds for VRR to return. This was verified in both modes on 7 October 2026.

The tested Deck woke by itself within a few seconds while the adapter was connected. The cause of that separate wake behaviour remains unknown; this fix restores VRR after resume and does not prevent unwanted wake-ups. Prolonged sleep and repeated-cycle endurance are not yet verified.

The shortened resume path completed in 18 seconds in both Gaming (23:04:42–23:05:00) and Desktop (23:06:49–23:07:07) tests, measured from helper detection to its activation log. The user confirmed success in both modes. These are observed timings, not a guaranteed upper bound.
