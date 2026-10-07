# Post-hotplug current state — 7 October 2026, 23:52 Europe/Berlin

Fresh read-only capture verifies RAM217=08 and25B=0A. autoApplyCustomEDID=off, customEDID query returnsFailed as it did for the empty slot before testing; clear command had previously succeeded.

OS and I2C EDID are identical: SHA256fcb048faa03baf2d3c106f2b0b1cd191df1557322022c94ab8c48b39488a57b0,256 bytes, header version/input010380, both checksums0. Compared with initial snapshot, only revision13:04→03, input14:85→80 and base checksum7F:E5→EB differ. Current factory EDID is a newly confirmed valid baseline, not byte-identical to initial adapter-rewritten EDID.

macOS STILL reports SupportsVariableRefreshRate=true and range48–120, despite original RAM values and no continuous-frequency feature (None). Current output is fixed4K60, SDR,8-bit YCbCr444 limited, DSCNo, VariableRefreshRateNo. Recognition persists across RAM/EDID cleanup; persistence across USB power-cycle or full reconnect is not tested.

This strengthens the need to separate host recognition from live capability state. It does not prove a particular cache implementation or that VRR can operate with original RAM. User previously selected variable rate only during the hotplug test and observedNoSignal; fixed-mode picture subsequently returned.

Next: preserve this baseline and prepare a bounded output-activation diagnostic. Capture exact variable timing and live capabilities after selection, explicitly restore verified fixed mode FIRST, then restore RAM/EDID. Do not repeat the old strict-initial-EDID script unchanged. Do not ask user to select variable rate manually without the recovery/capture runner.
