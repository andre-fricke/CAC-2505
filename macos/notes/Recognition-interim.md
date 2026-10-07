# Mac VRR recognition: verified state

RAM217=48 alone with original RAM25B=0A (detailed DP presentation) plus EDID continuous-frequency bit and general 48–120 Hz range did not produce macOS VRR capability. 4K60 SDR was uncompressed (DSC No). User reports no VRR and stable picture. Restore verified RAM08/0A and original OS EDID.

Earlier two-byte HDMI presentation plus same EDID also failed, both 4K120 HDR with DSC and verified 4K60 SDR 8-bit without DSC. These tests exclude missing continuous-frequency bit, broad 24-Hz lower range, active HDR or active DSC as individually sufficient explanations. They do not prove all host capability caches were refreshed.

## Coarse vs detailed downstream type

Apple DPCD reply code at ROM 0x8F7E–0x8F86 matches low capability offset 5 and loads constant 0x1D at 0x8F84. Stock also uses 0x1D (matching code location 0x8BA8; nearby control flow still needs mapping). This is not unique to Apple firmware.

IMPORTANT decoder correction: BetterDisplay labels coarse DPCD5 type reserved in its report, but Linux drm_dp.h defines port type mask 0x06. 0x1D & 0x06 = 0x04 = TMDS; bit0 present, bit3 conversion and bit4 detailed info are set. This is not evidence of an invalid or reserved capability. Original detailed DPCD80=08 announces DP; the two-byte test makes DPCD80=0B (HDMI). Whether macOS VRR recognition depends on coarse TMDS type is unknown. Do not conclude an Apple block from this alone or flash a patch.

Reference: https://raw.githubusercontent.com/torvalds/linux/master/include/drm/display/drm_dp.h

No new device changes made after this comparison. Display remains at test setting 4K60 SDR; restore preferred 4K120 HDR via System Settings if desired. Further work should examine host recognition/cache and firmware response paths instead of repeating equivalent EDID toggles.
