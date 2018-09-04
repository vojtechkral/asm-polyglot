
CC = gcc
AS = as
LD = ld
OBJCOPY = objcopy
PYTHON = python3

ARM = arm-linux-gnueabihf
ARM_CC = $(ARM)-gcc
ARM_AS = $(ARM)-as
ARM_LD = $(ARM)-ld
ARM_OBJCOPY = $(ARM)-objcopy
ARM_GDB = arm-none-eabi-gdb


all: hello-x86-64 hello-arm jmps.txt jmps-x86-64.o

.PHONY: all clean


# Compile ARM assembly and extract it as raw data:

asm-arm.o: asm-arm.s
	$(ARM_AS) -o $@ $<

asm-arm.text: asm-arm.o
	$(ARM_OBJCOPY) --dump-section .text=$@ $<

# Generate x86-64 assemmbly containing the ARM code as raw integers:

asm-x86-64.s: asm-arm.text asm-x86-64.s.py
	$(PYTHON) asm-x86-64.s.py $@ < $<

# Compile the composite assembly and extract is as raw data:

asm-x86-64.o: asm-x86-64.s
	$(AS) --64 -o $@ $<

asm-x86-64.text: asm-x86-64.o
	$(OBJCOPY) --dump-section .text=$@ $<

# Generate the C source file:

hello.c: asm-x86-64.text hello.c.py
	$(PYTHON) hello.c.py < $< $@

# Compile the C source for x86-64 and ARM:

hello-x86-64: hello.c
	$(CC) -static -nostdlib -o $@ $<

hello-arm: hello.c
	$(ARM_CC) -static -nostdlib -o $@ $<

# Generate the jmps.txt comparison table:

jmps-arm.o jmps.txt: jmps.py
	$(PYTHON) jmps.py jmps-annot.txt | $(ARM_AS) -o jmps-arm.o
	$(ARM_GDB) -ex 'disas jmps' -batch jmps-arm.o | sed -e 's/^ .*>://' \
		| paste jmps-annot.txt - | dd of=$@ 2>/dev/null
	rm jmps-annot.txt

jmps-x86-64.o: jmps.py
	$(PYTHON) jmps.py /dev/null | $(AS) --64 -o $@

clean:
	rm -f *.o asm-arm.text asm-x86-64.s asm-x86-64.text hello.c hello-x86-64 hello-arm \
		jmps-arm.o jmps.txt jmps-x86-64.o
