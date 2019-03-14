import logging


logger = logging.getLogger(__name__)


MICROCODE = """
# Define default values. We use NPI=1 as default WHICH IS UNSAFE :-)
dflt:  CND=10 NXT=00000  NPI=1                                # NOP.

# Fetch & Decode: All instructions return to here when finished.
00000: CND=11 NXT=10000  IRC PCC MRE      IRF=0 PCF=0 MAD=00  # fetch
00001: CND=11 NXT=10000  IRC              IRF=1               # decode

# Start of internal functionality.
00010: CND=00 NXT=00011  MRE TC           MAD=10              # POP 2
00011: CND=00 NXT=00111  SPC MWR ACW      SPF=1 MAD=11        # POP 3
00100: CND=10 NXT=00000  ACC MRE          ACF=11 MAD=10       # SUB 2
00101: CND=01 NXT=00110  TC SPC MRE       SPF=1 MAD=10        # JPOS 2
00110: CND=00 NXT=00000  ACC PCC MRE      ACF=10 PCF=1 MAD=10 # JPOS 3+
00111: CND=10 NXT=00000  ACC MRE          ACF=10 MAD=10       # JPOS 3-
01000: CND=00 NXT=00000  PCC MRE          MAD=10 C0C=1 PCF=1  # INT 2

# Start of first micro instruction for each instruction.
10000: CND=10 NXT=00000                                       # NOP
10001: CND=10 NXT=00000  SPC MWR ACW      SPF=0 MAD=10        # DUP
10010: CND=10 NXT=00000  ACC              ACF=01              # ONE
10011: CND=10 NXT=00000  ACC ACW          ACF=00              # ZERO
10100: CND=10 NXT=00000  ACC MRE          ACF=10 MAD=01       # LOAD
10101: CND=00 NXT=00010  SPC              SPF=1               # POP 1
10110: CND=00 NXT=00100  SPC              SPF=1               # SUB 1
10111: CND=00 NXT=00101  SPC              SPF=1               # JPOS 1
11000: CND=00 NXT=01000  SPC C0C ACC ACW  SPF=1 ACF=11        # INT 1

"""


def repaddr(uaddr):
    return "None" if uaddr is None else bin(uaddr)[2:].rjust(5, "0")


def validate_ucode(uaddr, ui):
    checks = """
    not ui.IRC or ui.IRF == 1 or (ui.IRF == 0 and (ui.MRE or ui.ACW))
    not ui.ACC or ui.ACF in [0, 1] or (ui.ACF in [2, 3] and (ui.MRE or ui.ACW))
    not ui.PCC or ui.PCF in [0, 1]
    not ui.SPC or ui.SPF in [0, 1]
    not ui.C0C or ui.MRE or ui.ACW
    ui.NPI or ui.CND == 0b10
    not ui.MRE or ui.MAD in [0, 1, 2, 3]
    not ui.MWR or ui.MAD in [0, 1, 2, 3]
    ui.MAD not in [0, 1, 2, 3] or (ui.MRE or ui.MWR)
    not ui.ACW or not ui.MRE
    not ui.MWR or not ui.MRE
    """

    for check in checks.splitlines():
        check = check.strip()
        if check and check[0] != "#" and not eval(check):
            logger.warning(
                "uaddr=%s: %s is not true.",
                repaddr(uaddr), check.replace("ui.", "")
            )


def validate_ustore(defined, ustore):

    # Some basic checks and warnings.
    for uaddr, ui in enumerate(ustore):
        validate_ucode(uaddr, ui)

        if ui.NXT is None:
            logger.warning(
                "uaddr=%s: NXT should not be undefined",
                repaddr(uaddr)
            )
            continue

        if not ui.NXT and ui.CND not in [0, 2]:
            logger.warning(
                "uaddr=%s: NXT=0 expects CND=0 or CND=2 not CND=%s",
                repaddr(uaddr), ui.CND
            )

        targets = [
            [ui.NXT],
            [ui.NXT, ui.NXT + 1],
            [ui.NXT, ui.NXT + 1],
            [ui.NXT | IM16 for IM16 in range(16)],
        ][ui.CND]

        if not ui.NPI:
            if ui.CND != 0b10:
                logger.warning(
                    "uaddr=%s: NPI=0 expects CND=0b10 not CND=%s",
                    repaddr(uaddr), ui.CND
                )
            if 0 not in targets:
                targets.append(0)
            if 1 not in targets:
                targets.append(1)

        for target in targets:
            if not defined[target]:
                logger.warning(
                    "uaddr=%s: undefined possible target %s.",
                    repaddr(uaddr), repaddr(target)
                )


def build_ustore(cpu, text, default=None):

    defaultui = {k: default for k in cpu.MicroInstructionFields}
    defaultui.update(default or {})

    ustore = [
        cpu.MicroInstruction(**defaultui)
        for _ in range(2 ** cpu.MicroInstructionFields["NXT"])
    ]

    defined = [False for _ in ustore]

    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue

        ui = defaultui.copy()

        uaddr, line = line.split(":", 1)
        line, comment = line.split("#", 1)

        for pair in line.split():
            if "=" in pair:
                k, v = pair.split("=")
            else:
                k, v = pair, "1"

            if k not in ui:
                logger.warning(
                    "uaddr=%s: skipping unknown %r.",
                    uaddr, k
                )
                continue

            ui[k] = int(v, 2)

        if uaddr == "dflt":
            defaultui.update(ui)
            continue

        uaddr = int(uaddr, 2)
        if uaddr >= len(ustore):
            logger.warning(
                "uaddr=%s: skipped because it is outside of addressable ucode.",
                repaddr(uaddr)
            )
            continue

        defined[uaddr] = True
        ustore[uaddr] = cpu.MicroInstruction(**ui)

    # Use latest default to initialize everything else.
    for uaddr, _ in enumerate(ustore):
        if not defined[uaddr]:
            ustore[uaddr] = cpu.MicroInstruction(**defaultui)

    validate_ustore(defined, ustore)
    return ustore
