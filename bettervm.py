#!/usr/bin/env python3

import ctypes
import struct


MICROCODE = """
uaddr || next uadr | clocks |bus |  function   |
------++-----------+--------+----+-------------+---------
      ||           | IAPTSM | AM | I A  P S M  |
      || COND NEXT | RCCCPW | CR | R C  C P A  |
      ||           | CCC CR | WE | F F  F F D  |
------++-----------+--------+----+-------------+---------
 0000 ||  11  1000 | 101000 | 01 | 0 xx 0 x 00 | fetch
 0001 ||  11  1000 | 100000 | 00 | 1 xx x x xx | decode
 0010 ||  00  0011 | 000100 | 01 | x xx x x 10 | POP 2
 0011 ||  00  0111 | 000011 | 10 | x xx x 1 11 | POP 3
 0100 ||  10  0000 | 010000 | 01 | x 11 x x 10 | SUB 2
 0101 ||  01  0110 | 000110 | 01 | x xx x 1 10 | JPOS 2
 0110 ||  00  0000 | 011000 | 01 | x 10 1 x 10 | JPOS 3+
 0111 ||  10  0000 | 010000 | 01 | x 10 x x 10 | JPOS 3-
 1000 ||  10  0000 | 000000 | 00 | x xx x x xx | NOP
 1001 ||  10  0000 | 000011 | 10 | x xx x 0 10 | DUP
 1010 ||  10  0000 | 010000 | 00 | x 01 x x xx | ONE
 1011 ||  10  0000 | 010000 | 10 | x 00 x x xx | ZERO
 1100 ||  10  0000 | 010000 | 01 | x 10 x x 01 | LOAD
 1101 ||  00  0010 | 000010 | 00 | x xx x 1 xx | POP 1
 1110 ||  00  0100 | 000010 | 00 | x xx x 1 xx | SUB 1
 1111 ||  00  0101 | 000010 | 00 | x xx x 1 xx | JPOS 1
"""


class VM:

    class StateBitField(ctypes.BigEndianStructure):
        _fields_ = [
            ('CND', ctypes.c_uint32, 2),
            ('NXT', ctypes.c_uint32, 4),
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
            if len(line) < 16:
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
        # MICROCODE
        self.ucode = self.load_ucode_from_ascii(MICROCODE)

        # BUSES
        self.data = 0
        self.addr = 0

        # REGISTERS
        self.upc = 0
        self.ir = 0     # Instruction
        self.acc = 0    # Accumulator
        self.t = 0      # Data
        self.sp = 0     # Stack pointer
        self.pc = 0     # Program counter

        # LEVELS, those are just wires.
        self.state = self.StateBitField()

        # MEMORY
        self.memory = [0] * 0x10000

    def clock(self):
        self.tick()
        self.tock()

    def tick(self):

        TLZ = 1 if self.t < 0 else 0
        INZ = 1 if self.ir != 0 else 0
        IMA = self.ir & 0x7

        mux = [0, TLZ, INZ, IMA]
        upc = mux[self.state.CND] | self.state.NXT

        self.upc = upc

        # Output micro instruction.
        self.state = self.ucode[self.upc]

    def tock(self):

        # Instruction register: IRF, IRC
        A = self.data
        B = self.ir
        IRF = self.state.IRF
        # 00:: A
        # 01:: B/8
        ir = A - IRF * A + IRF * (B >> 3)

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

        # Memory: MAD, MRE, MWR
        mux = [self.pc, self.acc, self.sp, self.t]
        self.addr = mux[self.state.MAD]

        # Trigger copies.
        if self.state.IRC:
            self.ir = ir
        if self.state.ACC:
            self.acc = acc
        if self.state.ACW:
            self.data = acc
        if self.state.TC:
            self.t = t
        if self.state.SPC:
            self.sp = sp
        if self.state.PCC:
            self.pc = pc
        if self.state.MWR:
            self.memory[self.addr] = self.data
        if self.state.MRE:
            self.data = self.memory[self.addr]


def main():
    vm = VM()
    while True:
        vm.clock()


if __name__ == "__main__":
    main()
