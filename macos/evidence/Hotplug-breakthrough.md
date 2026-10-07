# macOS VRR recognition breakthrough — 7 October 2026

Setup: Apple M1 Pro, CAC-2505 VMM7100 Apple firmware7.02.116, LG65QNED869QA. Prior logical display setting 4K60 SDR. No firmware flashing or driver patch.

Sequence: verify original RAM08/0A; set RAM25B02 then21748; unplug only HDMI while keeping USB-C powered, wait ten seconds, reconnect; verify RAM48/02 survived; apply temporary continuous-frequency EDID with general48–120 Hz range. Base EDID changes:18 0A→0B,5F18→30,7FE5→CC; CTA unchanged.

Before: SupportsVariableRefreshRate=false,71 timing dictionaries,0 with nonzero VRR range. During: support=true,70 timing dictionaries,51 with nonzero VRR range. User confirms Variable refresh rate appeared in System Settings. On selecting it, TV lost signal. This proves host recognition, not working HDMI VRR output or dynamic refresh. Reports were taken before the user's selection; the failure link state and exact selected timing were not captured.

Cleanup: RAM21708 and25B0A readback verified. autoApplyCustomEDID off, applyFactoryEDID and clear customEDID all returned0. User confirms picture returned. Final OS EDID valid but differs from initial at13(04→03),14(85→80),7F(E5→EB). Therefore strict byte-equality recovery check failed and independent watchdog remained scheduled. Do not claim exact original EDID recovery. These fields are associated with the firmware's known interface-rewriting path; causation/timing requires additional capture.

Implication: physical HDMI hotplug plus these known changes achieved recognition where software reinitialization alone did not. Relative contribution of hotplug, RAM type, EDID feature and range is not isolated. Remaining task is safe investigation of variable-output link loss. No complete macOS VRR solution yet.
