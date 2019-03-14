#!/usr/bin/env python3

import ctypes
import struct
import hardware
import ustore

# XMC - Extended Minimal CISC
# The architecture is adapted from A Minimal CISC by Douglas W. Jones
# http://homepage.divms.uiowa.edu/~jones/arch/cisc/
# Modifications by @wapiflapi include:
#  - Provisioning for double the number of instructions.
#  - Adding a memory mask serving as a privilege control.
#  - Adding an interrupt system.
#
# Roadmap:
#  - Adding Interrupts for IO & Debug.
#  - Maybe adding some tests ?!

MICROCODE = """
 uaddr || next uadr  | clocks  |bus |  function   |
-------++------------+---------+----+-------------+---------
       ||            | CIAPTSM | AM | I A  P S M  |
       || COND NEXT  | 0RCCCPW | CR | R C  C P A  |
       ||            | CCCC CR | WE | F F  F F D  |
-------++------------+---------+----+-------------+---------
 00000 ||  11  10000 | 0101000 | 01 | 0 xx 0 x 00 | fetch
 00001 ||  11  10000 | 0100000 | 00 | 1 xx x x xx | decode
 00010 ||  00  00011 | 0000100 | 01 | x xx x x 10 | POP 2
 00011 ||  00  00111 | 0000011 | 10 | x xx x 1 11 | POP 3
 00100 ||  10  00000 | 0010000 | 01 | x 11 x x 10 | SUB 2
 00101 ||  01  00110 | 0000110 | 01 | x xx x 1 10 | JPOS 2
 00110 ||  00  00000 | 0011000 | 01 | x 10 1 x 10 | JPOS 3+
 00111 ||  10  00000 | 0010000 | 01 | x 10 x x 10 | JPOS 3-

 01000 ||  00  00000 | 0001000 | 00 | x x  1 x xx | INT 2
 01001 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 01010 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 01011 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 01100 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 01101 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 01110 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 01111 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |

 10000 ||  10  00000 | 0000000 | 00 | x xx x x xx | NOP
 10001 ||  10  00000 | 0000011 | 10 | x xx x 0 10 | DUP
 10010 ||  10  00000 | 0010000 | 00 | x 01 x x xx | ONE
 10011 ||  10  00000 | 0010000 | 10 | x 00 x x xx | ZERO
 10100 ||  10  00000 | 0010000 | 01 | x 10 x x 01 | LOAD
 10101 ||  00  00010 | 0000010 | 00 | x xx x 1 xx | POP 1
 10110 ||  00  00100 | 0000010 | 00 | x xx x 1 xx | SUB 1
 10111 ||  00  00101 | 0000010 | 00 | x xx x 1 xx | JPOS 1

 11000 ||  00  01000 | 1010000 | 10 | x 11 x x xx | INT 1
 11001 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx | ?? hlt
 11010 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx | ?? call
 11011 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx | ?? ret / leave
 11100 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 11101 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 11110 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |
 11111 ||  xx  xxxxx | xxxxxxx | 01 | x x  x x xx |

"""

# Let's talk about memory layout and CR0
#
# cr0 is a control register it is ORed with the ADDR bus.
# - flags in bit outside of memory range are used for other
#   purposes since they don't affect anything.
# - bits inside memory range can be used to limit memory access.
#   this includes fetching instructions.
#
# 0xfff0 - Privileged memory mapped registers.
#    0x0 - CR0 backup
#    0x1 -
# 0x0000 - kernel entry point
#
# 0x1000 - user entry point
#
#
# 0xfff0 - General memory mapped registers.
#    0x0 - Interrupt code.
#    0x1 - Return address
#    0x2 - Stack base

class VM:

    class StateBitField(ctypes.BigEndianStructure):
        _fields_ = [
            ('CND', ctypes.c_uint32, 2),
            ('NXT', ctypes.c_uint32, 5),
            ('IRC', ctypes.c_uint32, 3),
            ('ACC', ctypes.c_uint32, 1),
            ('PCC', ctypes.c_uint32, 1),
            ('TC',  ctypes.c_uint32, 1),
            ('SPC', ctypes.c_uint32, 1),
            ('MWR', ctypes.c_uint32, 1),
            ('ACW', ctypes.c_uint32, 1),
            ('MRE', ctypes.c_uint32, 1),
            ('IRF', ctypes.c_uint32, 1),
            ('ACF', ctypes.c_uint32, 2),
            ('PCF', ctypes.c_uint32, 1),
            ('SPF', ctypes.c_uint32, 1),
            ('MAD', ctypes.c_uint32, 1),
        ]

        def __str__(self):
            return ", ".join(
                "%s=%d" % (field[0], getattr(self, field[0]))
                for field in self._fields_
            )

    @classmethod
    def load_ucode_from_ascii(cls, asciiucode):
        ucode = []
        print("Loading microcde from ASCII...")
        print("Lulz, here's to hoping this goes well. :cheers:")

        for line in asciiucode.splitlines():
            _, _, line = line.rpartition("||")
            line = "".join(c for c in line if c in "01x")
            # Could activate debug mode and randomize this.
            line = line.replace("x", "0")
            if len(line) < 23:
                continue
            ui = cls.StateBitField.from_buffer_copy(
                struct.pack(">I", int(line, 2))
            )
            print("%.2x: %s" % (len(ucode), ui))
            ucode.append(ui)

        if not len(ucode) == 16:
            raise ValueError("Couldn't extract 16 micro instructions.")
        print("Well, I hope that looks okay to you.")

        return ucode

    def __init__(self):
        # Do we have power?
        self.running = 0

        # MICROCODE
        self.ucode = self.load_ucode_from_ascii(MICROCODE)

        # BUSES
        self.data = 0
        self.addr = 0

        # REGISTERS
        self.cr0 = 0    # Control 0
        self.ir = 0     # Instruction
        self.acc = 0    # Accumulator
        self.t = 0      # Data
        self.sp = 0     # Stack pointer
        self.pc = 0     # Program counter
        self.upc = 0    # Microprogram counter

        # STATE, this is just wires basically.
        self.state = self.StateBitField()

        # MEMORY
        self.memmask = 0x3fff
        self.memory = [0] * (self.memmask + 1)

    def start(self):
        self.running = 1
        while self.running:
            self.clock()

    def clock(self):
        self.tick()
        self.tock()

    def tick(self):
        """Rising Clock Edge"""

        TLZ = 1 if self.t < 0 else 0
        INZ = 1 if self.ir != 0 else 0
        IMA = self.ir & 0xf

        # Output micro instruction.
        mux = [0, TLZ, INZ, IMA]
        upc = mux[self.state.CND] | self.state.NXT
        self.state = self.ucode[upc]

    def tock(self):
        """Falling Clock Edge"""

        # Update ADDR bus.
        mux = [self.pc, self.acc, self.sp, self.t]
        addr = mux[self.state.MAD] | self.cr0
        self.addr = addr & self.memmask

        # Update DATA bus.
        if self.state.ACW:
            self.data = self.acc
        if self.state.MRE:
            self.data = self.memory[self.addr]

        # Instruction register: IRF, IRC
        A = self.data
        B = self.ir
        IRF = self.state.IRF
        # 00:: A
        # 01:: B/8
        ir = A - IRF * A + IRF * (B >> 4)

        # Accumulator register: ACF, ACC, ACW
        A = self.data
        B = self.acc
        ACFh = (self.state.ACF >> 1) & 1
        ACFl = (self.state.ACF >> 0) & 1
        # 00:: 2B
        # 01:: 2B + 1
        # 10:: A
        # 11:: A - B
        acc = (
            2 * B - ACFh * 2 * B
            + ACFh * A
            - ACFh * ACFl * B
            + ACFl - ACFh * ACFl
        )

        # Data register: TC
        t = self.data

        # Stack pointer register: SPF, SPC
        A = self.sp
        SPF = self.state.SPF
        # 0: A + 1
        # 1: A - 1
        sp = 2 * SPF - 1 + A

        # Program counter register: PCF, PCC
        A = self.pc
        B = self.acc
        PCF = self.state.PCF
        # 0: A + 1
        # 1: B
        pc = A + 1 - PCF * A - PCF + PCF * B

        # Trigger loads.
        if self.state.IRC:
            self.ir = ir
        if self.state.ACC:
            self.acc = acc
        if self.state.TC:
            self.t = t
        if self.state.SPC:
            self.sp = sp
        if self.state.PCC:
            self.pc = pc
        if self.state.MWR:
            self.memory[self.addr] = self.data


def main():
    ustore.build_ustore(hardware.CPU, ustore.MICROCODE)


if __name__ == "__main__":
    main()
