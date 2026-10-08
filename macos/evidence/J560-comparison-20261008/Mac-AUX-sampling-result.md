# Mac AUX staging sampling result

Instrumented RGB8/SDR Variable test completed with wrapper exit 0. Original adapter RAM217=08/RAM25B=0A, original OS EDID, cleared custom EDID and disabled auto-apply were verified after restoration. User confirmed picture returned. Behavior during the observation was not explicitly reported by the user.

71 complete AUX staging samples were captured over approximately 16 seconds; intended duration was 28 seconds. The sampler exited 3 following timeouts; no claim of complete capture. Native reads and writes were captured, including cmd80 at address02011 with payload07 and HDCP traffic. No sampled request targeted DPCD00107. This is not evidence that no such request occurred: staging is overwritten between roughly 0.2-second samples.

RAM80D remained0A in all 71 reads. Port word RAMA74 was0080042C in48 reads,0080002C in21 reads and00000000 in1 read; bit12 was never observed set. Packet scratch RAM11FC was000A0184 in62 reads,001A0187 in7 reads,00000000 in1 read. These are CPU scratch observations, not wire packet captures.

Mac connection reports during observation showed Variable RGB8 SDR at0/5/10 seconds, then Fixed YCbCr4448 at15 seconds. Sampling may have affected timing; its RC timeout and partial capture limit interpretation. Unlike the earlier non-sampling RGB8 repeat, this run did not remain Variable for the entire observation.

No new configuration-write target or firmware patch is justified from this result. The next diagnostic must improve temporal capture or independently establish what reaches the DPCD00107 handler, rather than interpreting a missing sample as a missing write. Raw logs remain local and include HDCP session traffic; the decoded excerpt redacts HDCP payloads.
