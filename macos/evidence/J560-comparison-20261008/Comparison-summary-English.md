# J560 VRR comparison: current evidence

| Source and connection | Result | Evidence limit |
|---|---|---|
| Steam Deck → CAC-2505 → J560 HDMI | Stable picture; user observed changing monitor Hz during58/80/105FPS animation | Exact monitor values not recorded; application submission rates are not scanout measurements |
| M1 Pro Mac → J560 direct USB-C/DisplayPort | Stable picture; user reports working VRR during same requested-rate animation | Native Variable remains active before/after; exact monitor values not recorded |
| M1 Pro Mac → CAC-2505 → J560 HDMI, RAM48/02 | Black picture during observed Variable RGB8 SDR/noDSC interval | Mac reports Variable at0/5/10/15seconds, while adapter port bit12 and packet scratch remain fixed-state patterns |

Direct Mac positive control uses YCbCr42210bit, also seen in an earlier failed Mac/CAC control. That color format alone does not explain the failure. A separate explicit RGB8/noDSC control also fails. This strengthens source/converter interoperability as the problem area without establishing its exact cause.

Adapter firmware: supplied Apple7.02.116, flash version bytes07027400. Working Deck activation changes RAM90000A74 from0080042C to0080142C and packet-control RAM900011FC from84010A00 to7FC00000. Mac failure samples do not show these changes. Firmware locally builds the observed packet pattern; it is not a source wire capture.

No firmware patch has been validated for macOS. No flash write, new driver or blind hardware-register write was performed. Positive source and sink controls justify investigating the AUX activation/hardware-event path, not declaring the exact request missing or copying state bytes as a fix.
