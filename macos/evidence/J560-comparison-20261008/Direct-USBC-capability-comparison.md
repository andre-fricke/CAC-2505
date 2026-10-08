# Direct USB-C capability comparison

Working direct Mac/J560 control: DisplayPort sink Dp1.2; DPCD00000=12 (base revision1.2),00001=14 (HBR2),00007=C0 (MSA ignore advertised; no downstream port); active00100=14,00101=84,00107=80. Raw00100 block: `14 84 00 02 02 02 02 80 00 00 00 00 00 00 00 00`. Extended2200 begins `14 14 C4 01 01 00 01 C0`. Active mode2560x1600 YCbCr42210bit SDR Variable48–144; DSC off.

Failed Mac/CAC J560 controls: PCON/SYNAq converter, advertised base/extended DP1.4 with HBR3 maximum; Mac uses HBR3. RAM48 enables MSA-ignore advertisement, while RAMtype02 changes downstream-port descriptors. The Mac's report also indicates00107=80 when Variable is selected; adapter port bit12 remains clear and firmware-built output packet state remains at its fixed pattern.

Therefore00107 host report alone does not discriminate success. Native and converter identities, capability revision, link rate, downstream descriptors, EDID, variable timing range and potentially packet handling all differ. HBR2 versus HBR3 is a candidate confound, not an established failure cause. No supported direct link-rate setter was found in the official BetterDisplay5.0.6 CLI reference (https://betterdisplay.pro/guide/integration/cli-reference/); available connectionMode controls color/bit-depth/HDR formats rather than documenting a link-training-rate override. Do not invent such a command.

The direct report includes nonsensical LTTPR fields (for example maximum lane count21). Those high-address reports are not used as proof of physical link properties here. Core capability/configuration fields are recorded as host-side reads, not an independent wire trace. Raw local logs contain HDCP session fields; the accompanying public-fields excerpt excludes those addresses.
