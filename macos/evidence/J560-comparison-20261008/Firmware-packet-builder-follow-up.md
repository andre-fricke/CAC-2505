# Firmware packet-builder follow-up

Analysis uses the supplied Apple 7.02.116 firmware and saved Deck/Mac snapshots. No device commands or writes were executed for this analysis.

The Deck-only RAM900011FC value 7F C0 00 00 has a direct code counterpart: at ROM offsets 0x1A66A–0x1A678, the firmware constructs 0xC07F and writes it to RAM900011FC. Function entry 0x1A5B4 clears 36 bytes at RAM900011DC (0x1A5C2–0x1A5CC), builds a payload byte-by-byte (0x1A698–0x1A6E0, individual cases through0x1A762), and passes RAM900011E0 with argument0x120 to function0x1A2BA at0x1A6E4–0x1A6F2.

Function0x1A2BA transfers buffer words into port-indexed hardware registers based at0x2031040C/0x20310410 and controls0x20310408/0x20310414. This establishes a connection between the observed scratch buffer and an output hardware submission path, not physical transmission, exact HDMI packet identity, or full correct timing.

A direct caller is at0xB834. Before it, 0xB80A–0xB812 checks global RAM9000028E masked with0xFD (s2 is reset to RAM90000000 at0xB56C–0xB588); it then derives the function's second argument from a per-port halfword using seqz (0xB814–0xB830). The full upstream event/state and all indirect callers have not been resolved. These gates should not be bypassed by guessed RAM or MMIO writes.

Important correction in interpretation: the Deck's changed RAM packet pattern is firmware-built. Its presence cannot establish that Linux sends an identical packet over DisplayPort, and its absence on Mac cannot by itself establish missing source packets. The observed source-dependent activation difference remains real; its exact causal trigger remains open.

The port bit12 activation path through the DPCD107 handler and helper183D2 remains independently supported by static code. Correlation between that bit and the builder is observed at runtime, but a complete causal call chain between the two has not yet been established.

Further gating: builder1A5B4 loads port+416 (RAM90000E76 for port0) and switches paths based on whether it is zero (1A5D0–1A5D4). That field is assigned from function1AA04 by16BA6–16BAE, which performs a timing-table lookup, so it must not be labeled a simple VRR-enable flag. A matched capture of RAM9000028E,90000E2C,90000E76,900001CC is prepared. Current fixed-mode values may exclude static configuration differences, but cannot alone resolve the prior active transition.

Mac fixed-mode read-only gate capture completed at19:27:10 with exit0: RAM9000028E=00, RAM900001CC=00000000, RAM90000E2C=00000000 and RAM90000E76=00. The global28E masked check therefore passes in this sampled baseline. The zero E76 value selects the builder's zero-field branch if the builder is invoked. No invocation is proven by these baseline values; the hardware-event path or the active-transition state may still differ. A matching read-only Deck baseline capture is prepared.

Deck baseline matching read exits0: RAM28E=00,E76=00,1CC=00000000 match Mac; RAME2C=00010080 little-endian0x80000100 differs from Mac zero. This word is port+3CC, set from a timing/input structure (ROM16C58–16C5E and16D70–16D86; the latter explicitly sets a high-byte bit). It must not be treated as a pure VRR capability or a raw packet capture. These baseline gate reads do not establish the missing event.

Connection-format correction: the matched Mac48/02 operation log's connection-level mode is2560x1600 YCbCr422LimitedRange10bit, both fixed and initially selected Variable. The settled fallback isYCbCr444LimitedRange8bit. Thus prior generic descriptions of the matched Mac operation as RGB10 are incorrect, and source-format equivalence to the Deck has not yet been verified. The logical display-mode bit depth/encoding is not a substitute for connection-level format. A read-only enumeration of available Mac connection modes is prepared before considering a targeted RGB test.
