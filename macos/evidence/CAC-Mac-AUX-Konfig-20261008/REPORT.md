# Matched volatile-configuration AUX control

User reports unchanged, stable picture. Log ends with exit0 and verified restoration of RAM0x90000217=08 and RAM0x9000025B=0A; independent recovery stopped.

The Mac was tested first at08/0A, then at the known Steam Deck configuration48/02. In both phases, source107/1 and100/16 left receiver request header500/16 in RAM90000820. Source0FF/16 produced matching header0FF/16 and payload. Source107 returned00, globalRAM80D remained0B and port0 MSA-ignore mirror bit12 remainedclear. Thus changing these two RAM bytes alone, without re-enumeration, does not remove the observed Mac access-path difference. This does not exclude an enumeration-time effect or prove where AUX interception occurs.

No display-mode, EDID, DPCD, MMIO or flash write was requested. Only the two established volatile configuration bytes were changed and restored.

Additional static check of the remaining flags difference: RAM0x9000080E bit3 (Mac89 vs Deck81) is set in ROM0x88AC–0x88B4 when masked hardware interrupt status includes0x20 (reads20210140 and20210100 at0x888C/0x8890). It is consumed and cleared in0x8A3C–0x8A66 by a wait/completion path. This is not a demonstrated VRR-enable flag; direct modification is unjustified.
