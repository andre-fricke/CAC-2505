# DPCD107 control-path consistency audit

Source data: supplied Apple7.02.116 fullrom and existing instrumented J560 Deck/Mac runs. Offline analysis only; no adapter changes.

RAM9000080D is88 on the working Deck and0A on the Mac. Bit7 can be set/cleared by the software DPCD107 write handler at ROM9EF2–9F04: it copies input bit4 into RAM bit7. This is distinct from input bit7, which is passed to the port-bit12 helper at9F0E–9F18 if RAM bit4 is clear. Both observed RAM bytes have bit4 clear. Therefore that specific gate does not account for failure to set port bit12 on Mac.

If this exact software handler executed with input107=80 while sampled state/gates stayed unchanged, the helper would receive1 and set the port bit. The observed unchanged bit therefore conflicts with that complete assumed path, not necessarily with the host configuration report. Possible gaps include a hardware auto-AUX path bypassing the handler, another path resetting state, or host reports not representing the final request delivered to this handler. No physical AUX capture has established which.

RAM80D bit3 is set by the DPCD206 read branch at9604–9610; it is therefore at least partly a history/status flag rather than a simple VRR flag. RAM bit0 is updated by the DPCD160 handler atA00A–A01A and reset elsewhere. RAM bit1 is updated in function2025E at202F6–20300 from its input bit0, with call sites setting input0 at20986–20988 and input1 at209C4–209C6; it also controls hardware setup. Its full functional identity remains unresolved. Do not copy the entire Deck byte88 into the Mac byte0A.

Engineering implication: simply patching the software107 handler or copying observed packet bytes is not yet a justified solution. If the Mac bypasses the handler, such a patch could have no effect. If another path resets state, forcing the bit could create incoherent source timing. A useful next independent control is direct USB-C dynamic refresh on the same J560/Mac, observed with its live Hz counter, since the earlier direct-USB-C result established stable Variable selection but did not independently record changing monitor Hz.
