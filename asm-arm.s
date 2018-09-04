    .global _start
    .text

_start:
    # write syscall
    mov     %r0, $1
    adr     %r1, msg
    mov     %r2, $len
    mov     %r7, $4
    swi     $0

    # exit syscall
    mov     %r0, $0
    mov     %r7, $1
    swi     $0

msg:
    .ascii  "Hello, ARM!\n"
    .equ len, . - msg
    .int 0x0
