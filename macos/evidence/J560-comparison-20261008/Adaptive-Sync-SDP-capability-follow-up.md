# Adaptive-Sync SDP capability follow-up

Offline analysis; no hardware writes or setting changes.

Apple firmware 7.02.116: ROM 0x92B8–0x930C handles DPCD 0x2214. RAM 0x90000217 bit 6 (0x40), together with another per-port capability gate, permits a nonzero answer. The ordinary branch at 0x92F8–0x9302 returns 0x01 when RAM217 bit 5 is set, otherwise 0x03. Another branch at 0x92DA–0x92F6 can force 0x03; therefore setting bit 5 does not universally guarantee 0x01.

Linux definitions identify bit 0 as Adaptive-Sync SDP support and bit 1 as lack of support for the first-half-line / 3840-pixel-cycle window:
https://github.com/torvalds/linux/blob/master/include/drm/display/drm_dp.h

Mac DCP binary: VM 0x104CD8 reads DPCD 0x2214; 0x104CF4 masks bit 0 and 0x104CF8 stores it at object offset 0x525. Getter 0xFB104 returns this cached byte. A decision path at 0xF9A50–0xF9A70 uses it with other conditions; the full meaning of that decision has not been established. A separate path at 0x13A084 also reads 0x2214 and forwards the whole byte through a virtual call.

Inference: the existing RAM48 workaround changes both MSA-ignore capability and SDP advertisement, so the failed Mac tests cannot isolate these effects. Changing the advertisement from 0x03 to 0x01 would leave the verified cached bit unchanged. This is not currently sufficient justification for another RAM mutation. No proof yet that SDP advertisement causes the Mac failure or that disabling it would solve it. Native direct-USB-C dynamic VRR is already positive; successful Deck/CAC HDMI VRR remains positive.

Binary offsets above are static evidence, not runtime execution traces. VM addresses for the DCP binary use file offset minus 0x1000.

## Additional static interpretation and new baseline

Fresh Mac/CAC/J560 baseline at 2026-10-08 20:07:32: fixed 120 Hz, HBR3, RAM217=08, RAM25B=0A; packet RAM11FC=84 01 0A 00. No RAM or flash mutations were performed for this capture.

The aggregate function at VM 0xF9A08 includes cached SDP support (+0x525), Panel Replay capability (+0x529, populated from DPCD 0xB0 bit 0 at 0x1043F8–0x104420), and Autonomous FRL (+0x52B, populated from DPCD 0x303C bit 7 at 0x1042AC–0x1042CC), plus another virtual predicate whose meaning is unresolved. Its vtable entry has signature 0x5A6B and slot 0x820 in the identified device tables. Slot reuse in unrelated classes is not evidence of a call to this function.

A matching-signature caller at 0x13A5B4–0x13A654 logs “version: %x : dp 2.x %s” and can produce a version value of 0x14. Another matching caller at 0x13A1B0–0x13A1D0 participates in selecting device references after capability reads. Thus the aggregate is related to a broader DP feature/version/device path; it must not be described as a proven VRR activation switch. This static finding does not establish that the path ran during the failing hardware test, nor that its behavior caused black output.

No new RAM bit test is justified by this finding alone. In particular, 0x48→0x68 would still advertise SDP support bit 0 and would not isolate SDP support from MSA-ignore support. No such write was made.
