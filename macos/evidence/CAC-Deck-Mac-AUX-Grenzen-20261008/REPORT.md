# DPCD request-shape comparison: Steam Deck and Mac

All six Deck source reads completed and matched the receiver software request header and returned payload: 0x403/16, 0xFE/16, 0xFF/9, 0x100/8, 0x101/7, 0x107/1. DPCD107 returned10. Receiver flags remained00 89 81 4B. RC enable and final disable succeeded. No RAM/DPCD/flash write was requested.

Mac controls: 0x403/16, 0xFE/16 and0xFF/9 matched receiver headers; 0x100/8,0x101/7 and0x107/1 retained the identity preflight header0x500/16. Mac107 returned00. Four selected AUX control registers are equal across hosts.

This establishes different observed software-buffer paths between these tested states. It does not locate the interception on the physical wire. Deck RAM configuration48/02 differs from Mac08/0A; a matched-configuration Mac control remains necessary. Historical Mac48/02 plus DPCD90 write did not update the receiver mirror, but did not include the complete matched request-shape control used here.
