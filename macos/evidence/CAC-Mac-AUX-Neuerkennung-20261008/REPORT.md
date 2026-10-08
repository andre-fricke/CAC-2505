# Matched configuration after HDMI reconnect

User reports picture returned after HDMI reconnect, TV60FPS/VRROff. Capture completed with exit0. RAM21748/type25B02 were verified after reconnect and restored to08/0A at completion; independent watchdog stopped. The script did not restore the macOS selected display mode.

The same request-path pattern persists:107/1 and100/16 retain the preceding500/16 identity header in receiver RAM820;0FF/16 produces a matching software request header and data. DPCD107 returns00; port MSA-ignore mirror bit12 remainsclear. Receiver flags change from00 0B 89 4B to00 0A A9 4B after reconnect; port status from06600444 to02600424. This is consistent with a mode change and cannot be compared as an unchanged4K120HDR physical link.

Combined with the prior fixed4K120HDR matched-RAM control, neither changing the two known RAM bytes alone nor the tested HDMI reconnect produces the Deck's observed software-buffer path. HDMI reconnect is not equivalent to full USB-C device reconstruction, so host runtime virtualization remains unproven. No additional write to interrupt flags or undocumented MMIO is justified.

Next user action: restore the desired fixed4K120HDR selection in macOS Displays. No additional hardware test is bundled with that action.
