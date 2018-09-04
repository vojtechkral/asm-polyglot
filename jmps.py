#!/usr/bin/env python3

import sys


TEMPLATE = """\
# WARN: This file is auto-generated from jmps.py

    .global _start
    .text

jmps:
{}
"""


def main(annotfile):
    """
    Generates a .s file with all possible permutations of 2 nops and a short jump
    with all possible jump values.
    This file is to be compiled with an ARM as and disassembled again with gdb
    to generate ARM instructions.
    A secondary file is written at `annotfile` containing x86-64 equivalents
    to be paste-merged with the resulting ARM disassembly file.
    """

    jmps = ""
    annot = "\n"

    for i in range(2, -1, -1):
        # Always jump at least over the following ARM instruction,
        # which boils down to i + 4 here:
        for j in range(i + 4, 256):
            jmps += "    .int 0x{}{:02x}eb{}\n".format("90" * i, j, "90" * (2 - i))
            annot += "{}jmp {:02x} {}\n".format("nop " * (2 - i), j, "nop " * i)

    print(TEMPLATE.format(jmps))
    annotfile.write(annot)

if __name__ == '__main__':
    with open(sys.argv[1], "w") as annotfile:
        main(annotfile)
