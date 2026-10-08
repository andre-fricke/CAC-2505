00a65e ef126251 jal          t0, 0x21516
00a662 b7040090 lui          s1, 0x90000
00a666 13870400 mv           a4, s1
00a66a 8567     c.lui        a5, 1
00a66c ba97     c.add        a5, a4
00a66e 37178813 lui          a4, 0x13881
00a672 13078738 addi         a4, a4, 0x388
00a676 23a0e720 sw           a4, 0x200(a5)
00a67a 83c74720 lbu          a5, 0x204(a5)
00a67e 37140090 lui          s0, 0x90001
00a682 4111     c.addi       sp, -0x10
00a684 93840400 mv           s1, s1
00a688 13040400 mv           s0, s0
00a68c 99c3     c.beqz       a5, 6
00a68e 23020420 sb           zero, 0x204(s0)
00a692 b7072320 lui          a5, 0x20230
00a696 d843     c.lw         a4, 4(a5)
00a698 4167     c.lui        a4, 0x10
00a69a d8c3     c.sw         a4, 4(a5)
00a69c bc4f     c.lw         a5, 0x58(a5)
00a69e 37570090 lui          a4, 0x90005
00a6a2 9396e700 slli         a3, a5, 0xe
00a6a6 63d4060c bgez         a3, 0xc8
00a6aa 8347d7b8 lbu          a5, -0x473(a4)
00a6ae 8507     c.addi       a5, 1
00a6b0 93f7f70f andi         a5, a5, 0xff
00a6b4 a306f7b8 sb           a5, -0x473(a4)
00a6b8 0547     c.li         a4, 1
00a6ba 636df70a bltu         a4, a5, 0xba
00a6be b7072320 lui          a5, 0x20230
00a6c2 bc53     c.lw         a5, 0x60(a5)
00a6c4 37580090 lui          a6, 0x90005
00a6c8 93d58701 srli         a1, a5, 0x18
00a6cc bd89     c.andi       a1, 0xf
00a6ce 93d60701 srli         a3, a5, 0x10
00a6d2 93f6f60f andi         a3, a3, 0xff
00a6d6 a300b482 sb           a1, -0x7df(s0)
00a6da a205     c.slli       a1, 8
00a6dc 13d68700 srli         a2, a5, 8
00a6e0 2301d482 sb           a3, -0x7de(s0)
00a6e4 cd8e     c.or         a3, a1
00a6e6 1376f60f andi         a2, a2, 0xff
00a6ea a206     c.slli       a3, 8
00a6ec b7550090 lui          a1, 0x90005
00a6f0 a301c482 sb           a2, -0x7dd(s0)
00a6f4 d18e     c.or         a3, a2
00a6f6 37560090 lui          a2, 0x90005
00a6fa 13d7c701 srli         a4, a5, 0x1c
00a6fe 83a885b8 lw           a7, -0x478(a1)
00a702 03230623 lw           t1, 0x230(a2)
00a706 13f5f70f andi         a0, a5, 0xff
00a70a 1207     c.slli       a4, 4
00a70c 3ec2     c.swsp       a5, 4(sp)
00a70e 2302a482 sb           a0, -0x7dc(s0)
00a712 2300e482 sb           a4, -0x7e0(s0)
00a716 b7550090 lui          a1, 0x90005
00a71a 63161303 bne          t1, a7, 0x2c
00a71e b7580090 lui          a7, 0x90005
00a722 0343e8b8 lbu          t1, -0x472(a6)
00a726 83c818a8 lbu          a7, -0x57f(a7)
00a72a 631e1301 bne          t1, a7, 0x1c
00a72e b7580090 lui          a7, 0x90005
00a732 03c34523 lbu          t1, 0x234(a1)
00a736 83c86823 lbu          a7, 0x236(a7)
00a73a 63161301 bne          t1, a7, 0xc
00a73e b7580090 lui          a7, 0x90005
00a742 238a0828 sb           zero, 0x294(a7)
00a746 2328d622 sw           a3, 0x230(a2)
00a74a 2307a8b8 sb           a0, -0x472(a6)
00a74e 238ae522 sb           a4, 0x234(a1)
00a752 b7062320 lui          a3, 0x20230
00a756 f452     c.lw         a3, 0x64(a3)
00a758 1396f600 slli         a2, a3, 0xf
00a75c 63570602 bgez         a2, 0x2e
00a760 93060009 addi         a3, zero, 0x90
00a764 6313d702 bne          a4, a3, 0x26
00a768 efe00f90 jal          -0x1f00
00a76c 65a8     c.j          0xb8
00a76e a30607b8 sb           zero, -0x473(a4)
00a772 b1b7     c.j          -0xb4
00a774 93070002 addi         a5, zero, 0x20
00a778 230be482 sb           a4, -0x7ca(s0)
00a77c a30af482 sb           a5, -0x7cb(s0)
00a780 a3020482 sb           zero, -0x7db(s0)
00a784 efe02fd5 jal          -0x1aae
00a788 1dbf     c.j          -0xca
00a78a b7062320 lui          a3, 0x20230
00a78e 83a6460a lw           a3, 0xa4(a3)
00a792 13770703 andi         a4, a4, 0x30
00a796 31cf     c.beqz       a4, 0x5c
00a798 83c7042b lbu          a5, 0x2b0(s1)
00a79c 858b     c.andi       a5, 1
00a79e 89cb     c.beqz       a5, 0x12
00a7a0 b7150090 lui          a1, 0x90001
00a7a4 0546     c.li         a2, 1
00a7a6 93850582 addi         a1, a1, -0x7e0
00a7aa 0145     c.li         a0, 0
00a7ac efd0714d jal          0x1dcd6
00a7b0 efe06f8c jal          -0x1f3a
00a7b4 83470482 lbu          a5, -0x7e0(s0)
00a7b8 13978701 slli         a4, a5, 0x18
00a7bc 6187     c.srai       a4, 0x18
00a7be 63580714 bgez         a4, 0x150
00a7c2 03464482 lbu          a2, -0x7dc(s0)
00a7c6 1307f00f addi         a4, zero, 0xff
00a7ca 6317e608 bne          a2, a4, 0x8e
00a7ce c147     c.li         a5, 0x10
00a7d0 a30af482 sb           a5, -0x7cb(s0)
00a7d4 230b0482 sb           zero, -0x7ca(s0)
00a7d8 efe0efcf jal          -0x1b02
00a7dc 37072320 lui          a4, 0x20230
00a7e0 5c43     c.lw         a5, 4(a4)
00a7e2 9396f700 slli         a3, a5, 0xf
00a7e6 63df0602 bgez         a3, 0x3e
00a7ea c167     c.lui        a5, 0x10
00a7ec a107     c.addi       a5, 8
00a7ee 5cc3     c.sw         a5, 4(a4)
00a7f0 a5bf     c.j          -0x88
00a7f2 93f7f70f andi         a5, a5, 0xff
00a7f6 13d78600 srli         a4, a3, 8
00a7fa 8507     c.addi       a5, 1
00a7fc 1377f70f andi         a4, a4, 0xff
00a800 6385e702 beq          a5, a4, 0x2a
00a804 9307f00f addi         a5, zero, 0xff
00a808 e308f5f8 beq          a0, a5, -0x70
00a80c 8547     c.li         a5, 1
00a80e 230bf482 sb           a5, -0x7ca(s0)
00a812 c147     c.li         a5, 0x10
00a814 a30af482 sb           a5, -0x7cb(s0)
00a818 a3020482 sb           zero, -0x7db(s0)
00a81c efe0cf84 jal          -0x1fb4
00a820 efe06fcb jal          -0x1b4a
00a824 4101     c.addi       sp, 0x10
00a826 6f102237 j            0x21372
00a82a 9307f00f addi         a5, zero, 0xff
00a82e e305f5f6 beq          a0, a5, -0x96
00a832 8566     c.lui        a3, 1
00a834 8147     c.li         a5, 0
00a836 b7052320 lui          a1, 0x20230
00a83a 93865682 addi         a3, a3, -0x7db
00a83e 03a6850a lw           a2, 0xa8(a1)
00a842 3387d700 add          a4, a5, a3
00a846 2697     c.add        a4, s1
00a848 8507     c.addi       a5, 1
00a84a 2300c700 sb           a2, 0(a4)
00a84e 13f7f70f andi         a4, a5, 0xff
00a852 e376e5fe bgeu         a0, a4, -0x14
00a856 89b7     c.j          -0xbe
00a858 13070009 addi         a4, zero, 0x90
00a85c 639ce70a bne          a5, a4, 0xb8
00a860 83477421 lbu          a5, 0x217(s0)
00a864 91c7     c.beqz       a5, 0xc
00a866 83471482 lbu          a5, -0x7df(s0)
00a86a 13f78700 andi         a4, a5, 8
00a86e 01e7     c.bnez       a4, 8
00a870 eff07fd7 jal          -0x28a
00a874 95b7     c.j          -0x9c
00a876 03c76420 lbu          a4, 0x206(s1)
00a87a 418b     c.andi       a4, 0x10
00a87c 31ff     c.bnez       a4, -0xa4
00a87e 83452482 lbu          a1, -0x7de(s0)
00a882 9d8b     c.andi       a5, 7
00a884 a207     c.slli       a5, 8
00a886 cd8f     c.or         a5, a1
00a888 83453482 lbu          a1, -0x7dd(s0)
00a88c a207     c.slli       a5, 8
00a88e dd8d     c.or         a1, a5
00a890 8967     c.lui        a5, 2
00a892 a697     c.add        a5, s1
00a894 03c73759 lbu          a4, 0x593(a5)
00a898 8547     c.li         a5, 1
00a89a 6305f700 beq          a4, a5, 0xa
00a89e b7070a00 lui          a5, 0xa0
00a8a2 be95     c.add        a1, a5
00a8a4 03c50440 lbu          a0, 0x400(s1)
00a8a8 b7160090 lui          a3, 0x90001
00a8ac 93865682 addi         a3, a3, -0x7db
00a8b0 0506     c.addi       a2, 1
00a8b2 ef10902f jal          0x1af8
00a8b6 83474482 lbu          a5, -0x7dc(s0)
00a8ba 8507     c.addi       a5, 1
00a8bc 230bf482 sb           a5, -0x7ca(s0)
00a8c0 a30a0482 sb           zero, -0x7cb(s0)
00a8c4 11bf     c.j          -0xec
00a8c6 03c76420 lbu          a4, 0x206(s1)
00a8ca 418b     c.andi       a4, 0x10
00a8cc e31607f0 bnez         a4, -0xf4
00a8d0 83452482 lbu          a1, -0x7de(s0)
00a8d4 9d8b     c.andi       a5, 7
00a8d6 a207     c.slli       a5, 8
00a8d8 cd8f     c.or         a5, a1
00a8da 83453482 lbu          a1, -0x7dd(s0)
00a8de a207     c.slli       a5, 8
00a8e0 dd8d     c.or         a1, a5
00a8e2 8967     c.lui        a5, 2
00a8e4 a697     c.add        a5, s1
00a8e6 03c73759 lbu          a4, 0x593(a5)
00a8ea 8547     c.li         a5, 1
00a8ec 6305f700 beq          a4, a5, 0xa
00a8f0 b7070a00 lui          a5, 0xa0
00a8f4 be95     c.add        a1, a5
00a8f6 03464482 lbu          a2, -0x7dc(s0)
00a8fa 03c50440 lbu          a0, 0x400(s1)
00a8fe b7160090 lui          a3, 0x90001
00a902 93865682 addi         a3, a3, -0x7db
00a906 0506     c.addi       a2, 1
00a908 ef10d02e jal          0x1aec
00a90c 55bf     c.j          -0x4c
00a90e efa0e032 jal          0xa32e
00a912 d9b5     c.j          -0x13a
00a914 13070008 addi         a4, zero, 0x80
00a918 e390e7ec bne          a5, a4, -0x140
00a91c 83477421 lbu          a5, 0x217(s0)
00a920 91c7     c.beqz       a5, 0xc
00a922 83471482 lbu          a5, -0x7df(s0)
00a926 13f78700 andi         a4, a5, 8
00a92a 51ff     c.bnez       a4, -0x64
00a92c eff07fcf jal          -0x30a
00a930 65b5     c.j          -0x158
