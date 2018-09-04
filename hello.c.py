#!/usr/bin/env python3

import sys


TEMPLATE = """\
/* WARN: This file is auto-generated from hello.c.py */

#include <stdint.h>

const uint64_t _start[] __attribute__((section(".text"))) = {{{}
}};"""


def main(outfile):
    stdin = sys.stdin.buffer.read()

    current = ""
    array = ""

    for (i, byte) in enumerate(stdin):
        current = "{:02x}".format(byte) + current
        if len(current) == 16:
            if (i + 1) % 16 == 0:
                array += "0x{},".format(current)
            else:
                array += "\n    0x{}, ".format(current)
            current = ""

    print(TEMPLATE.format(array), file=outfile)


if __name__ == '__main__':
    with open(sys.argv[1], "w") as outfile:
        main(outfile)
