import logging


logger = logging.getLogger(__name__)


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
            if defined[uaddr]:
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


def build_ucode(cpu, defaults, uaddr, line):

    for pair in line.split():
        k, _, v = pair.partition("=")
        if not v:
            v = "1"

        if k not in defaults:
            logger.warning(
                "uaddr=%s: skipping unknown %r.",
                uaddr, k
            )
            continue

        defaults[k] = int(v, 2)

    return cpu.MicroInstruction(**defaults)


def build_ustore(cpu, text, default=None):

    defaultui = {k: default for k in cpu.MicroInstructionFields}
    defaultui.update(default or {})

    ustore = [
        cpu.MicroInstruction(**defaultui)
        for _ in range(2 ** cpu.MicroInstructionFields["NXT"])
    ]

    defined = [False for _ in ustore]

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        dui = defaultui.copy()

        uaddr, _, line = line.partition(":")
        line, _, comment = line.partition("#")

        ui = build_ucode(cpu, dui, uaddr, line)

        if uaddr == "dflt":
            defaultui.update(dui)
            continue

        uaddr = int(uaddr, 2)
        if uaddr >= len(ustore):
            logger.warning(
                "uaddr=%s: skipped because it is outside of addressable ucode.",
                repaddr(uaddr)
            )
            return None

        if defined[uaddr]:
            logger.warning(
                "uaddr=%s: over writing previous definition.",
                repaddr(uaddr)
            )

        defined[uaddr] = True
        ustore[uaddr] = ui

    # Use latest default to initialize everything else.
    for uaddr, _ in enumerate(ustore):
        if not defined[uaddr]:
            ustore[uaddr] = cpu.MicroInstruction(**defaultui)

    validate_ustore(defined, ustore)
    return ustore
