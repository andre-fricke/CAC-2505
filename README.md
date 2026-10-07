# CAC-2505: Steam Deck 4K120 HDR VRR

A tested workaround for the Club 3D CAC-2505 USB-C → HDMI adapter running Apple/4K120 firmware **7.02.116**. A Steam Deck service enables VRR through two volatile adapter RAM changes, without flashing firmware or patching the graphics driver.

**Start with [the Steam Deck installation guide](steamdeck/README.md).** It includes installation, prerequisites, automatic activation, recovery and removal. [Technical findings](steamdeck/FINDINGS.md) describe the changes and evidence.

Confirmed on 7 October 2026 with an LG 65QNED869QA: 3840×2160 at 120 Hz with HDR, VRR ON, changing TV FPS and a stable picture. Automatic activation was verified after reconnecting in Desktop and Gaming modes and after rebooting into Gaming Mode.

The current helper deliberately accepts only firmware 7.02.116 and the tested LG EDID identity. It is not a universal patch for every TV or CAC-2505 firmware. macOS VRR is not solved by this package. Firmware binaries are not included: obtain the matching Apple/4K120 firmware from Club 3D support; this repository provides no flashing tool.
