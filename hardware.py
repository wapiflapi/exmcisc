from collections import OrderedDict, namedtuple


class CPU:

    MicroInstructionFields = OrderedDict([
        # Next uaddr
        ("CND", 2),
        ("NXT", 5),
        # Clocks
        ("C0C", 1),
        ("IRC", 1),
        ("ACC", 1),
        ("PCC", 1),
        ("TC", 1),
        ("SPC", 1),
        ("MWR", 1),
        # Bus
        ("ACW", 1),
        ("MRE", 1),
        # Functions
        ("IRF", 1),
        ("ACF", 2),
        ("PCF", 1),
        ("SPF", 1),
        ("MAD", 2),
        ("NPI", 1),
    ])

    MicroInstruction = namedtuple(
        'MicroInstructionFields', MicroInstructionFields
    )

    @classmethod
    def ustore_from_asciirep(cls, asciirep):
        pass

    def __init__(self, memory, ustore):

        # ROM
        self.ustore = ustore
        if len(ustore) != 2 ** self.MicroInstruction['NXT']:
            raise ValueError(
                "Micro store does not contain %d entries." % (
                    2 ** self.MicroInstruction['NXT']
                ))

        # RAM
        self.memory = memory
        self.memsize = len(self.memory)
        self.memmask = self.memsize - 1
        if not self.memory or self.memsize & self.memmask:
            raise ValueError("Memory size is not a multiple of two.")

        # Registers
        self.upc = 0
        self.ir = 0
        self.acc = 0
        self.pc = 0
        self.t = 0
        self.sp = 0
        self.cr0 = 0

    def clock(self):
        self.tick()
        self.tock()

    def tick(self):
        """Rising Clock Edge"""

        udata = self.ustore[self.upc]

        self.upc = (
            (
                (
                    udata.NPI or int(self.cr0 == 0)
                ) and udata.NXT
            ) | (
                [
                    0,
                    int(self.t < 0),
                    int(self.ir != 0),
                    int(self.ir % 16),
                ][
                    (
                        udata.NPI or int(not self.cr0 == 0)
                    ) and udata.COND
                ]
            )
        )

    def tock(self):
        """Falling Clock Edge"""

        udata = self.ustore[self.upc]

        addr = (
            self.cr0 | [
                self.pc,
                self.acc,
                self.sp,
                self.t,
            ][
                udata.MAD
            ]
        )

        data = (
            (udata.ACW and self.acc) or
            (udata.MRE and self.memory[addr])
        )

        self.memory[addr] = data

        self.ir = (
            [
                data,
                self.ir / 16,
            ][udata.IRF]
        ) if udata.IRC else self.ir

        self.acc = (
            [
                2 * self.acc,
                2 * self.acc + 1,
                data,
                data - self.acc,
            ][udata.ACF]
        ) if udata.ACC else self.acc

        self.pc = (
            [
                self.pc + 1,
                self.acc,
            ][udata.PCF]
        ) if udata.PCC else self.pc

        self.t = data if udata.TC else self.t

        self.sp = (
            [
                self.sp + 1,
                self.sp - 1,
            ][udata.SPF]
        ) if udata.SPC else self.sp

        self.cr0 = (
            int(self.cr0 == 0) and data
        ) if udata.C0C else self.cr0
