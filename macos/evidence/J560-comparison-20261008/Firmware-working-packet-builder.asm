
ROM offsets 00B800–00B83C
00b800 8347e4e6 lbu          a5, -0x192(s0)
00b804 f99b     c.andi       a5, -2
00b806 2307f4e6 sb           a5, -0x192(s0)
00b80a 8347e928 lbu          a5, 0x28e(s2)
00b80e 93f7d70f andi         a5, a5, 0xfd
00b812 b1e7     c.bnez       a5, 0x4c
00b814 834774a6 lbu          a5, -0x599(s0)
00b818 37150090 lui          a0, 0x90001
00b81c 130505a6 addi         a0, a0, -0x5a0
00b820 9387670e addi         a5, a5, 0xe6
00b824 8607     c.slli       a5, 1
00b826 3e99     c.add        s2, a5
00b828 83550900 lhu          a1, 0(s2)
00b82c c205     c.slli       a1, 0x10
00b82e c181     c.srli       a1, 0x10
00b830 93b51500 seqz         a1, a1
00b834 efe01058 jal          0xed80
00b838 8147     c.li         a5, 0
00b83a 9149     c.li         s3, 4
00b83c b9be     c.j          -0x4a2

ROM offsets 01A2BA–01A316
01a2ba b7073120 lui          a5, 0x20310
01a2be 9388c740 addi         a7, a5, 0x40c
01a2c2 13830741 addi         t1, a5, 0x410
01a2c6 938e8740 addi         t4, a5, 0x408
01a2ca 4111     c.addi       sp, -0x10
01a2cc 93f5f53f andi         a1, a1, 0x3ff
01a2d0 13080602 addi         a6, a2, 0x20
01a2d4 216e     c.lui        t3, 8
01a2d6 93874741 addi         a5, a5, 0x414
01a2da 03476500 lbu          a4, 6(a0)
01a2de 032f0600 lw           t5, 0(a2)
01a2e2 2106     c.addi       a2, 8
01a2e4 4207     c.slli       a4, 0x10
01a2e6 b3061701 add          a3, a4, a7
01a2ea 23a0e601 sw           t5, 0(a3)
01a2ee 8326c6ff lw           a3, -4(a2)
01a2f2 1a97     c.add        a4, t1
01a2f4 14c3     c.sw         a3, 0(a4)
01a2f6 03476500 lbu          a4, 6(a0)
01a2fa b3e6c501 or           a3, a1, t3
01a2fe 36c2     c.swsp       a3, 4(sp)
01a300 4207     c.slli       a4, 0x10
01a302 7697     c.add        a4, t4
01a304 14c3     c.sw         a3, 0(a4)
01a306 03476500 lbu          a4, 6(a0)
01a30a 4207     c.slli       a4, 0x10
01a30c 3e97     c.add        a4, a5
01a30e 1443     c.lw         a3, 0(a4)
01a310 36c2     c.swsp       a3, 4(sp)
01a312 9246     c.lwsp       a3, 4(sp)
01a314 93f60604 andi         a3, a3, 0x40

ROM offsets 01A5B4–01A762
01a5b4 ef12015c jal          t0, 0x115c0
01a5b8 2a84     c.mv         s0, a0
01a5ba 37150090 lui          a0, 0x90001
01a5be 7971     c.addi16sp   sp, -0x30
01a5c0 ae84     c.mv         s1, a1
01a5c2 13064002 addi         a2, zero, 0x24
01a5c6 8145     c.li         a1, 0
01a5c8 1305c51d addi         a0, a0, 0x1dc
01a5cc efc02ebc jal          -0x13c3e
01a5d0 83476441 lbu          a5, 0x416(s0)
01a5d4 ede3     c.bnez       a5, 0xe2
01a5d6 b7172220 lui          a5, 0x20221
01a5da 13874784 addi         a4, a5, -0x7bc
01a5de 3ac6     c.swsp       a4, 0xc(sp)
01a5e0 83a64784 lw           a3, -0x7bc(a5)
01a5e4 93074002 addi         a5, zero, 0x24
01a5e8 a307f100 sb           a5, 0xf(sp)
01a5ec 13078002 addi         a4, zero, 0x28
01a5f0 b247     c.lwsp       a5, 0xc(sp)
01a5f2 a307e100 sb           a4, 0xf(sp)
01a5f6 3247     c.lwsp       a4, 0xc(sp)
01a5f8 9c43     c.lw         a5, 0(a5)
01a5fa c182     c.srli       a3, 0x10
01a5fc 1843     c.lw         a4, 0(a4)
01a5fe c183     c.srli       a5, 0x10
01a600 1305f00f addi         a0, zero, 0xff
01a604 4183     c.srli       a4, 0x10
01a606 ba97     c.add        a5, a4
01a608 9d8e     c.sub        a3, a5
01a60a 8357243f lhu          a5, 0x3f2(s0)
01a60e c206     c.slli       a3, 0x10
01a610 1307f03f addi         a4, zero, 0x3ff
01a614 c182     c.srli       a3, 0x10
01a616 636bf700 bltu         a4, a5, 0x16
01a61a 13072003 addi         a4, zero, 0x32
01a61e 3e85     c.mv         a0, a5
01a620 63f4e700 bgeu         a5, a4, 8
01a624 13052003 addi         a0, zero, 0x32
01a628 1375f50f andi         a0, a0, 0xff
01a62c 1c48     c.lw         a5, 0x10(s0)
01a62e 13978700 slli         a4, a5, 8
01a632 b7172220 lui          a5, 0x20221
01a636 635a0706 bgez         a4, 0x74
01a63a 138787b6 addi         a4, a5, -0x498
01a63e 3ac6     c.swsp       a4, 0xc(sp)
01a640 83a787b6 lw           a5, -0x498(a5)
01a644 13078002 addi         a4, zero, 0x28
01a648 a307e100 sb           a4, 0xf(sp)
01a64c 3247     c.lwsp       a4, 0xc(sp)
01a64e 1843     c.lw         a4, 0(a4)
01a650 998f     c.sub        a5, a4
01a652 c207     c.slli       a5, 0x10
01a654 c183     c.srli       a5, 0x10
01a656 93b7170a sltiu        a5, a5, 0xa1
01a65a 03588401 lhu          a6, 0x18(s0)
01a65e b7050090 lui          a1, 0x90000
01a662 13860500 mv           a2, a1
01a666 0567     c.lui        a4, 1
01a668 3297     c.add        a4, a2
01a66a 3166     c.lui        a2, 0xc
01a66c 1306f607 addi         a2, a2, 0x7f
01a670 13588800 srli         a6, a6, 8
01a674 b7a80480 lui          a7, 0x8004a
01a678 232ec71e sw           a2, 0x1fc(a4)
01a67c 13781800 andi         a6, a6, 1
01a680 0146     c.li         a2, 0
01a682 938e0500 mv           t4, a1
01a686 a942     c.li         t0, 0xa
01a688 9388488d addi         a7, a7, -0x72c
01a68c 1143     c.li         t1, 4
01a68e 054e     c.li         t3, 1
01a690 930340f8 addi         t2, zero, -0x7c
01a694 856f     c.lui        t6, 1
01a696 714f     c.li         t5, 0x1c
01a698 9375f60f andi         a1, a2, 0xff
01a69c 63efb20a bltu         t0, a1, 0xbe
01a6a0 13972500 slli         a4, a1, 2
01a6a4 4697     c.add        a4, a7
01a6a6 1843     c.lw         a4, 0(a4)
01a6a8 0287     c.jr         a4
01a6aa 13874784 addi         a4, a5, -0x7bc
01a6ae 3ac6     c.swsp       a4, 0xc(sp)
01a6b0 83a74784 lw           a5, -0x7bc(a5)
01a6b4 41bf     c.j          -0x70
01a6b6 8146     c.li         a3, 0
01a6b8 8147     c.li         a5, 0
01a6ba 0145     c.li         a0, 0
01a6bc 79bf     c.j          -0x62
01a6be a5c0     c.beqz       s1, 0x60
01a6c0 230a6100 sb           t1, 0x14(sp)
01a6c4 13f7c50f andi         a4, a1, 0xfc
01a6c8 1107     c.addi       a4, 4
01a6ca 8d89     c.andi       a1, 3
01a6cc 7697     c.add        a4, t4
01a6ce 2e97     c.add        a4, a1
01a6d0 4c08     c.addi4spn   a1, sp, 0x14
01a6d2 b295     c.add        a1, a2
01a6d4 83c50500 lbu          a1, 0(a1)
01a6d8 7e97     c.add        a4, t6
01a6da 0506     c.addi       a2, 1
01a6dc 230eb71c sb           a1, 0x1dc(a4)
01a6e0 e31ce6fb bne          a2, t5, -0x48
01a6e4 37160090 lui          a2, 0x90001
01a6e8 1306061e addi         a2, a2, 0x1e0
01a6ec 93050012 addi         a1, zero, 0x120
01a6f0 2285     c.mv         a0, s0
01a6f2 eff09fbc jal          -0x438
01a6f6 83476400 lbu          a5, 6(s0)
01a6fa 37073120 lui          a4, 0x20310
01a6fe 13074740 addi         a4, a4, 0x404
01a702 c207     c.slli       a5, 0x10
01a704 ba97     c.add        a5, a4
01a706 9843     c.lw         a4, 0(a5)
01a708 9316b700 slli         a3, a4, 0xb
01a70c 63c60600 bltz         a3, 0xc
01a710 b7061000 lui          a3, 0x100
01a714 558f     c.or         a4, a3
01a716 98c3     c.sw         a4, 0(a5)
01a718 4561     c.addi16sp   sp, 0x30
01a71a 6f10e147 j            0x1147e
01a71e 230a7100 sb           t2, 0x14(sp)
01a722 4db7     c.j          -0x5e
01a724 230bc101 sb           t3, 0x16(sp)
01a728 71bf     c.j          -0x64
01a72a a30b0100 sb           zero, 0x17(sp)
01a72e 59bf     c.j          -0x6a
01a730 230cc101 sb           t3, 0x18(sp)
01a734 41bf     c.j          -0x70
01a736 a30c0100 sb           zero, 0x19(sp)
01a73a 69b7     c.j          -0x76
01a73c 230d6100 sb           t1, 0x1a(sp)
01a740 51b7     c.j          -0x7c
01a742 a30d0101 sb           a6, 0x1b(sp)
01a746 bdbf     c.j          -0x82
01a748 230ed100 sb           a3, 0x1c(sp)
01a74c a5bf     c.j          -0x88
01a74e a30ef100 sb           a5, 0x1d(sp)
01a752 8dbf     c.j          -0x8e
01a754 230fa100 sb           a0, 0x1e(sp)
01a758 b5b7     c.j          -0x94
01a75a 5808     c.addi4spn   a4, sp, 0x14
01a75c 3297     c.add        a4, a2
01a75e 23000700 sb           zero, 0(a4)
01a762 8db7     c.j          -0x9e

ROM offsets 009EEA–009F1C
009eea 93077010 addi         a5, zero, 0x107
009eee 6398fd02 bne          s11, a5, 0x30
009ef2 93973500 slli         a5, a1, 3
009ef6 13f70708 andi         a4, a5, 0x80
009efa 83c7d480 lbu          a5, -0x7f3(s1)
009efe 93f7f707 andi         a5, a5, 0x7f
009f02 d98f     c.or         a5, a4
009f04 a386f480 sb           a5, -0x7f3(s1)
009f08 c18b     c.andi       a5, 0x10
009f0a e39407ee bnez         a5, -0x118
009f0e 37150090 lui          a0, 0x90001
009f12 9d81     c.srli       a1, 7
009f14 130505a6 addi         a0, a0, -0x5a0
009f18 efe0a04b jal          0xe4ba
009f1c d9bd     c.j          -0x12a

ROM offsets 0183D2–01843C
0183d2 5c49     c.lw         a5, 0x14(a0)
0183d4 b183     c.srli       a5, 0xc
0183d6 858b     c.andi       a5, 1
0183d8 638cb700 beq          a5, a1, 0x18
0183dc 03477500 lbu          a4, 7(a0)
0183e0 b7070090 lui          a5, 0x90000
0183e4 93870700 mv           a5, a5
0183e8 ba97     c.add        a5, a4
0183ea 0547     c.li         a4, 1
0183ec a380e740 sb           a4, 0x401(a5)
0183f0 93f71500 andi         a5, a1, 1
0183f4 1397c700 slli         a4, a5, 0xc
0183f8 5c49     c.lw         a5, 0x14(a0)
0183fa fd76     c.lui        a3, 0xfffff
0183fc fd16     c.addi       a3, -1
0183fe f58f     c.and        a5, a3
018400 d98f     c.or         a5, a4
018402 5cc9     c.sw         a5, 0x14(a0)
018404 1397a700 slli         a4, a5, 0xa
018408 635a0702 bgez         a4, 0x34
01840c 83476500 lbu          a5, 6(a0)
018410 37073120 lui          a4, 0x20310
018414 13078741 addi         a4, a4, 0x418
018418 c207     c.slli       a5, 0x10
01841a ba97     c.add        a5, a4
01841c 9843     c.lw         a4, 0(a5)
01841e 4111     c.addi       sp, -0x10
018420 89c9     c.beqz       a1, 0x12
018422 b7060010 lui          a3, 0x10000
018426 558f     c.or         a4, a3
018428 3ac2     c.swsp       a4, 4(sp)
01842a 1247     c.lwsp       a4, 4(sp)
01842c 98c3     c.sw         a4, 0(a5)
01842e 4101     c.addi       sp, 0x10
018430 8280     c.jr         ra
018432 b70600f0 lui          a3, 0xf0000
018436 fd16     c.addi       a3, -1
018438 758f     c.and        a4, a3
01843a fdb7     c.j          -0x12
01843c 8280     c.jr         ra
