#!/usr/bin/env python3

import sys


TEMPLATE = """\
# WARN: This file is auto-generated from asm-x86-64.s.py

    .global _start
    .text

_start:
    # These 3 instructions encode as a harmless ALU instruction on ARM
    jmp x86
    nop
    nop

arm:{}

x86:
    # create a hello message on the stack
    sub     $24, %rsp
    movq    msg(%rip), %rax
    mov     %rax, (%rsp)
    xor     %rax, %rax
    cpuid
    mov     %ebx, 8(%rsp)
    mov     %edx, 12(%rsp)
    mov     %ecx, 16(%rsp)
    movl    $0x0a21, 20(%rsp)    # 0x0a21 = "!\\n"

    # write syscall
    mov     $1, %rax
    mov     $1, %rdi
    lea     1(%rsp), %rsi
    mov     $21, %rdx
    syscall

    # exit syscall
    mov     $60, %rax
    xor     %rdi, %rdi
    syscall

msg:
    .ascii  " Hello, "
    .int 0x0
"""


def main(outfile):
    stdin = sys.stdin.buffer

    arm_code = ""

    instr = stdin.read(4)
    while len(instr) == 4:
        instr = int.from_bytes(instr, "little")
        arm_code += "\n    .int 0x{:x}".format(instr)
        instr = stdin.read(4)

    print(TEMPLATE.format(arm_code), file=outfile)


if __name__ == '__main__':
    with open(sys.argv[1], "w") as outfile:
        main(outfile)
