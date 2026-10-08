# Short AUX observation result

Complete sampler run: exit0,262 buffer reads in8.019seconds (approximately32.7 reads/s). No observed00107 request. Captured command80 writes to02011 and HDCP addresses; command90 reads from03037,00600,0020F,03031 and000F0. This is a software-dispatch staging buffer, not a lossless physical AUX trace. ROM0xA6C2 copies controller request metadata; later requests overwrite it. Controller setup at0x8C88–0x8C94 also programs20230068=D42049C9; semantics are unresolved. Hardware-handled transactions or short-lived requests may be absent from samples. Neither sampling result establishes absence of a source00107 write.

Mac connection state: VariableRGB8SDR at the first two observation queries, then0x0 undefined/VariableNo, then FixedYCbCr4448. Config reset/EDID restoration fully verified; wrapper exit0. User confirmed picture was black during the observation and returned after the test.

This run avoids the preceding timeout but does not resolve the source/converter failure. It does not justify guessed controller register writes, forcing a runtime status bit, or firmware patching. Raw HDCP session data stays local; sanitized decoded addresses omit its payload.
