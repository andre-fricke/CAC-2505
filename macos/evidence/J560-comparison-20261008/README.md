# J560 control comparisons and AUX measurements — 8 October 2026

These are derived findings and small static code excerpts. Raw DPCD logs, HDCP session payloads, system dumps, Apple/vendor binaries and local hardware test runners are excluded. Static code addresses are evidence references, not instructions to modify memory.

| Source and connection | Result |
| --- | --- |
| Steam Deck → CAC → LG | Confirmed 4K120 HDR dynamic VRR, stable picture |
| Steam Deck → CAC → J560 HDMI | Dynamic VRR observed, stable picture |
| M1 Pro Mac → J560 direct USB-C | Dynamic VRR observed, stable picture |
| M1 Pro Mac → CAC → J560 HDMI | Variable mode offered after temporary configuration/EDID work; black picture, including RGB8 SDR without DSC |

The last short AUX test captured262 staging-buffer samples in8.019seconds and exited0. It did not capture a00107 request. The staging buffer is overwritten and is not a complete physical AUX trace: absence of a sample does not establish absence of a source write. The user observed a black picture during the Variable test and a restored picture afterwards. RAM08/0A, factory OS EDID and cleared host override were verified restored.

No functioning macOS VRR workaround or new firmware has been produced. Repeating the same configurations or guessing additional RAM/MMIO writes is not justified by these findings. Further work needs a concrete new code finding, documented chip information or a supported trace that distinguishes the source/API path from actual receiver processing.

The J560 results do not broaden the installed Steam Deck helper's accepted display identity: it remains restricted to the documented LG setup. Application submission rates58/80/105 are not measurements of physical scanout, and exact observed J560 Hz values were not recorded.

Start with Comparison-summary-English.md; use Mac-AUX-short-result.md for the latest completed measurement. Other files document intermediate tests and must be interpreted chronologically.
