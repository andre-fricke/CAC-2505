# Mac versus Steam Deck AUX control snapshot

Both register captures succeeded, with reply status and end addresses validated. No memory/DPCD/flash write was sent. The Deck capture ran over SSH without sudo.

| Register | Mac | Steam Deck |
|---|---|---|
| 0x20230000 | 0x0018000F | 0x0018000F |
| 0x2023001C | 0x00000000 | 0x00000000 |
| 0x20230068 | 0xD42049C9 | 0xD42049C9 |
| 0x20230074 | 0x00000030 | 0x00000030 |
| RAM0x90000217 | 08 | 48 |
| RAM0x9000025B | 0A | 02 |
| RAM0x9000080D | 0B | 89 |
| Port0 status at RAM0x90000A74 | 0x06600444 | 0x04601444 |

All four selected AUX registers are identical. No causality is inferred for undocumented fields. The internal MSA-ignore mirror (port bit12) is set only in the Deck snapshot, consistent with prior working-state observations. This capture did not independently observe the TV or dynamic scanout.

The subsequent Deck read-only address-boundary comparison failed before its AUX reads: /dev/drm_dp_aux1 requires additional OS access. Its first version attempted RC disable during error cleanup although RC had not been enabled; disable returned status04. No register write occurred. Cleanup has been corrected to issue disable only after a confirmed RC enable. Root execution of the read-only script is required for the pending comparison.
