
REFERENCE 000f9a50
000f9a38 mov        w1, #3
000f9a3c movk       x16, #0x47a, lsl #48
000f9a40 blraa      x8, x16
000f9a44 cbnz       w0, #0xf9a58
000f9a48 ldrb       w8, [x19, #0x529]
000f9a4c tbnz       w8, #0, #0xf9a58
000f9a50 ldrb       w8, [x19, #0x525]
000f9a54 tbz        w8, #0, #0xf9a6c
000f9a58 mov        w8, #1
000f9a5c and        w0, w8, #1
000f9a60 ldp        x29, x30, [sp, #0x10]
000f9a64 ldp        x20, x19, [sp], #0x20
000f9a68 retab
000f9a6c ldrb       w8, [x19, #0x52b]
000f9a70 b          #0xf9a5c
000f9a74 ldr        x0, [x0, #0x1c8]
000f9a78 ldr        x16, [x0]
000f9a7c mov        x17, x0
000f9a80 movk       x17, #0x4a9f, lsl #48
000f9a84 autda      x16, x17

REFERENCE 000fb0d4
000fb0bc mov        x17, #0x628
000fb0c0 add        x16, x16, x17
000fb0c4 ldr        x2, [x16]
000fb0c8 movk       x16, #0x89aa, lsl #48
000fb0cc braa       x2, x16
000fb0d0 and        w8, w1, #1
000fb0d4 strb       w8, [x0, #0x525]
000fb0d8 ret
000fb0dc ldr        x0, [x0, #0x1c8]
000fb0e0 ldr        x16, [x0]
000fb0e4 mov        x17, x0
000fb0e8 movk       x17, #0x4a9f, lsl #48
000fb0ec autda      x16, x17
000fb0f0 mov        x17, #0x618
000fb0f4 add        x16, x16, x17
000fb0f8 ldr        x3, [x16]
000fb0fc movk       x16, #0x5575, lsl #48
000fb100 braa       x3, x16
000fb104 ldrb       w0, [x0, #0x525]
000fb108 ret

REFERENCE 000fb104
000fb0ec autda      x16, x17
000fb0f0 mov        x17, #0x618
000fb0f4 add        x16, x16, x17
000fb0f8 ldr        x3, [x16]
000fb0fc movk       x16, #0x5575, lsl #48
000fb100 braa       x3, x16
000fb104 ldrb       w0, [x0, #0x525]
000fb108 ret
000fb10c mov        x2, x1
000fb110 mov        x1, x0
000fb114 ldr        x0, [x0, #0x1c8]
000fb118 ldr        x16, [x0]
000fb11c mov        x17, x0
000fb120 movk       x17, #0x4a9f, lsl #48
000fb124 autda      x16, x17
000fb128 mov        x17, #0x600
000fb12c add        x16, x16, x17
000fb130 ldr        x3, [x16]
000fb134 movk       x16, #0x2938, lsl #48
000fb138 braa       x3, x16

REFERENCE 00104cf8
00104ce0 mov        w4, #0x1f4
00104ce4 movk       x16, #0x6f56, lsl #48
00104ce8 blraa      x8, x16
00104cec cbnz       w0, #0x104460
00104cf0 ldrb       w8, [sp, #0x20]
00104cf4 and        w8, w8, #1
00104cf8 strb       w8, [x19, #0x525]
00104cfc ldr        x16, [x19]
00104d00 autda      x16, x22
00104d04 mov        x17, #0x4a8
00104d08 add        x16, x16, x17
00104d0c ldr        x8, [x16]
00104d10 mov        x0, x19
00104d14 movk       x16, #0x755d, lsl #48
00104d18 blraa      x8, x16
00104d1c cbnz       w0, #0x104d4c
00104d20 mov        x8, #0xa211
00104d24 movk       x8, #0x2050, lsl #16
00104d28 movk       x8, #0x5654, lsl #32
00104d2c str        x8, [sp, #0x20]
