# AUX path investigation — 8 October 2026

Current confirmed user state: fixed4K120HDR, visible stable picture, after a full USB-C disconnect/reconnect. Adapter runs unmodified Apple7.02.116. No macOS VRR solution has been achieved.

## Evidence

- Steam Deck: all tested source reads403/16,FE/16,FF/9,100/8,101/7,107/1 match the adapter software request header and reply payload.107 reads10; internal MSA-ignore mirror bit12 is set.
- Mac:403/16,FE/16 andFF/9 match the software request header; requests100/8,101/7,107/1 leave the worker identity preflight500/16 header in the observed buffer.107 reads00. This is not a wire trace; absence of a header is not proof that no physical AUX transaction occurred.
- A bounded software-read-shadow marker changed RAM9000080D0B→8B→0B. For the matchingFF/16 request, adapter software payload reports107=10 but Mac API still reports00. This establishes a data-path discrepancy; it does not locate the override.
- The four observed AUX controls20230000/1C/68/74 have equal values on both hosts:0018000F/00000000/D42049C9/00000030. Register semantics are not documented.
- Mac matching configuration48/02 at fixed4K120HDR does not alter the observed read path. Repeat after HDMI reconnect also does not change it; that reconnect changes the display state to60Hz, so it is not an unchanged4K120HDR comparison.
- All temporary writes in these experiments were verified restored. After the HDMI reconnect control, OS still offeredVariable48–60 and no120Hz until a full USB-C power cycle. User then verified stable4K120 and HDR on. RAM restoration alone does not restore the OS mode list.

## Static analysis limits

The installed DCP firmware contains native AUX routines and a virtual-device dictionary path. Native header emitter VM5DD88–5DDEC emits address and length without a special100–107 branch. Virtual read1417D4 uses starting-address lookup in dictionary+540 when mode+560=1. The controller loads a possible`virtual-dpcd`property into dictionary+2C0 at58280–582E8; runtime use for the connected adapter remains unproven. No matching property appeared in host IORegistry searches.

The adapter's normal DPCD107 write handler at ROM9EEA–9F18 updates a software flag and invokes183D2, which updates the MSA-ignore mirror and, conditionally, undocumented HDMI hardware. Direct RAM mirrors would not reproduce the full handler. USB memory-write21 does not call that handler; no supported USB bypass has been found.

RAM9000080E bit3, differing between tested hosts, is set by a masked hardware interrupt and cleared in a wait/completion path. It is not established as a VRR-enable flag. Do not alter it or undocumented MMIO based on this comparison.

## Next work

Localize the source/API versus receiver-software discrepancy using a supported runtime trace or a fully verified alternative AUX access path. No new guessed USB command, firmware image, private setter, interrupt-flag write or MMIO write is justified. Do not repeat already failed identical configurations.

Detailed derived reports are under evidence/CAC-*-20261008. Raw Apple binaries, full registry captures and local crash reports were not copied into this repository.
