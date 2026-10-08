00104c60 cmp        w0, #0x12
00104c64 b.lo       #0x104cfc
00104c68 ldrb       w8, [x19, #0x200]
00104c6c cmp        w8, #1
00104c70 b.ne       #0x104cfc
00104c74 ldr        x16, [x19]
00104c78 autda      x16, x22
00104c7c mov        x17, #0x540
00104c80 add        x16, x16, x17
00104c84 ldr        x8, [x16]
00104c88 add        x2, sp, #0x20
00104c8c mov        x0, x19
00104c90 mov        w1, #0x2210
00104c94 mov        w3, #1
00104c98 mov        w4, #0x1f4
00104c9c movk       x16, #0x6f56, lsl #48
00104ca0 blraa      x8, x16
00104ca4 cbnz       w0, #0x104460
00104ca8 ldrb       w8, [sp, #0x20]
00104cac ubfx       w9, w8, #3, #1
00104cb0 strb       w9, [x19, #0x526]
00104cb4 ubfx       w8, w8, #1, #1
00104cb8 strb       w8, [x19, #0x527]
00104cbc ldr        x16, [x19]
00104cc0 autda      x16, x22
00104cc4 mov        x17, #0x540
00104cc8 add        x16, x16, x17
00104ccc ldr        x8, [x16]
00104cd0 add        x2, sp, #0x20
00104cd4 mov        x0, x19
00104cd8 mov        w1, #0x2214
00104cdc mov        w3, #1
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
00104d30 add        x0, x19, #0x1d8
00104d34 add        x1, sp, #0x20
00104d38 bl         #0x12adc
00104d3c cbnz       w0, #0x104d4c
00104d40 adrp       x8, #0x302000
00104d44 ldr        d0, [x8, #0x608]
00104d48 str        d0, [x19, #0x358]
00104d4c mov        w20, #0
00104d50 b          #0x104464
00104d54 bl         #0xdb64
00104d58 mov        x20, x0
00104d5c ldr        x16, [x19]
00104d60 autda      x16, x22
00104d64 ldr        x8, [x16, #0x10]!
00104d68 mov        x0, x19
00104d6c movk       x16, #0x9eca, lsl #48
0013a040 mov        w1, #0x60
0013a044 mov        w3, #0x10
0013a048 bl         #0x13ab40
0013a04c cbnz       w0, #0x13a2b4
0013a050 ldr        x0, [x19, #0x8d8]
0013a054 ldr        x16, [x0]
0013a058 mov        x17, x0
0013a05c movk       x17, #0x4a9f, lsl #48
0013a060 autda      x16, x17
0013a064 mov        x17, #0x520
0013a068 add        x16, x16, x17
0013a06c ldr        x8, [x16]
0013a070 add        x1, sp, #0x30
0013a074 movk       x16, #0x2ee1, lsl #48
0013a078 blraa      x8, x16
0013a07c ldr        x0, [x19, #0x8e8]
0013a080 add        x2, sp, #0x30
0013a084 mov        w1, #0x2214
0013a088 mov        w3, #1
0013a08c bl         #0x13ab40
0013a090 cbnz       w0, #0x13a2b4
0013a094 ldr        x0, [x19, #0x8d8]
0013a098 ldrb       w1, [sp, #0x30]
0013a09c ldr        x16, [x0]
0013a0a0 mov        x17, x0
0013a0a4 movk       x17, #0x4a9f, lsl #48
0013a0a8 autda      x16, x17
0013a0ac mov        x17, #0x7a0
0013a0b0 add        x16, x16, x17
0013a0b4 ldr        x8, [x16]
0013a0b8 movk       x16, #0x43de, lsl #48
0013a0bc blraa      x8, x16
0013a0c0 ldr        x0, [x19, #0x8e8]
0013a0c4 add        x2, sp, #0x30
0013a0c8 mov        w1, #0x303c
0013a0cc mov        w3, #1
0013a0d0 bl         #0x13ab40
0013a0d4 cbnz       w0, #0x13a2b4
0013a0d8 ldr        x0, [x19, #0x8d8]
0013a0dc ldrb       w1, [sp, #0x30]
