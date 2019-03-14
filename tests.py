import pprint

import hardware
import ustore


def test_load_dump(cpu, method, before, after, strict=True):
    expected = before.copy()
    expected.update(after)

    cpu.loadstate(**before)
    method()
    state = cpu.dumpstate()

    if "mres" in expected:
        state["mres"] = cpu.memory.mres

    if "mwrs" in expected:
        state["mwrs"] = cpu.memory.mwrs

    diff = {
        k: (v, expected[k])
        for k, v in state.items()
        if v != expected[k] and (strict or k in after)
    }

    if not diff:
        return

    print("=" * 80)
    print("State:")
    print("\n".join("    %s" % l for l in pprint.pformat(before).splitlines()))
    print("Triggers CPU.%s DIFF - showing {k: (state, expected)}" % method.__name__)
    print("\n".join("    %s" % l for l in pprint.pformat(diff).splitlines()))


def test_tick(cpu, before, after, strict=True):
    test_load_dump(cpu, cpu.tick, before, after, strict=strict)


def test_tock(cpu, before, after, strict=True):
    test_load_dump(cpu, cpu.tock, before, after, strict=strict)


def test_clock(cpu, before, tick, tock, strict=True):
    test_tick(cpu, before, tick or {}, strict=strict and tick is not None)
    before = cpu.dumpstate()
    test_tock(cpu, before, tock or {}, strict=strict and tock is not None)


def test_clock_defaults(cpu, ucode, before, tick=None, tock=None,
                        strict=True, defaultui=None, defaultstate=None,
                        mval=None):

    if defaultui is None:
        defaultui = {k: 0 for k in cpu.MicroInstructionFields}
    if defaultstate is None:
        defaultstate = dict(
            udata=None,
            upc=0,
            ir=0,
            acc=0,
            pc=0,
            t=0,
            sp=0,
            cr0=0,
        )

    state = defaultstate.copy()
    state.update(before)

    cpu.memory.reset(mval=mval)  # reset logging

    if not isinstance(state["udata"], cpu.MicroInstruction):
        state["udata"] = ustore.build_ucode(cpu, defaultui, None, ucode)

    test_clock(cpu, state, tick, tock, strict=strict)


    cpu.memory.reset(mval=mval)  # reset logging


def test_npi(cpu):

    test_clock_defaults(
        cpu, "CND=11 NXT=1000",         # Attempt PRIV 0b1000
        before=dict(ir=0b0, cr0=0),     # while privileged
        tick=dict(upc=0b1000),          # should work, ir empty
        strict=True,                    # nothing else should change
    )

    test_clock_defaults(
        cpu, "CND=11 NXT=1000",         # Attempt PRIV 0b1000
        before=dict(ir=0b1, cr0=0),     # while privileged
        tick=dict(upc=0b1000),          # should work, ir full
        strict=True,                    # nothing else should change
    )

    test_clock_defaults(
        cpu, "CND=11 NXT=1000",         # Attempt PRIV 0b1000
        before=dict(ir=0, cr0=0b1000),  # while NOT privileged
        tick=dict(upc=0),               # should NOT work, ir empty
        strict=True,                    # should fail to fetch
    )

    test_clock_defaults(
        cpu, "CND=11 NXT=1000",         # Attempt PRIV 0b1000
        before=dict(ir=1, cr0=0b1000),  # while NOT privileged
        tick=dict(upc=1),               # should NOT work, ir full
        strict=True,                    # should fail to decode
    )

    test_clock_defaults(
        cpu, "NXT=1000 NPI",            # Attempt NPI 0b1000
        before=dict(ir=0b0, cr0=0),     # while privileged
        tick=dict(upc=0b1000),          # should work, ir empty
        strict=True,                    # nothing else should change
    )

    test_clock_defaults(
        cpu, "NXT=1000 NPI",            # Attempt NPI 0b1000
        before=dict(ir=0b1, cr0=0),     # while privileged
        tick=dict(upc=0b1000),          # should work, ir full
        strict=True,                    # nothing else should change
    )

    test_clock_defaults(
        cpu, "NXT=1000 NPI",            # Attempt NPI 0b1000
        before=dict(ir=0, cr0=0b1000),  # while NOT privileged
        tick=dict(upc=0b1000),          # should work, ir empty
        strict=True,                    # nothing else should change
        )

    test_clock_defaults(
        cpu, "NXT=1000 NPI",            # Attempt NPI 0b1000
        before=dict(ir=1, cr0=0b1000),  # while NOT privileged
        tick=dict(upc=0b1000),          # should NOT work, ir full
        strict=True,                    # nothing else should change
    )


def test_upc_select(cpu):

    test_clock_defaults(
        cpu, "NPI CND=0 NXT=1000",      # Direct next
        before=dict(ir=0b111, t=0),     #
        tick=dict(upc=0b1000),          #
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=1 NXT=1000",      # t<0 offset to next
        before=dict(ir=0b111, t=0),     # should be 0
        tick=dict(upc=0b1000),          #
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=1 NXT=1000",      # t<0 offset to next
        before=dict(ir=0b111, t=-1),    # should be 1
        tick=dict(upc=0b1001),          #
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=0 NXT=1000",      # direct next
        before=dict(ir=0b111, t=-1),    # with t<0
        tick=dict(upc=0b1000),          # should be direct
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=10 NXT=1000",     # ir empty offset
        before=dict(ir=0, t=-1),        # should be 0
        tick=dict(upc=0b1000),          #
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=10 NXT=1000",     # ir empty offset
        before=dict(ir=0b111, t=-1),    # should be 1
        tick=dict(upc=0b1001),          #
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=11 NXT=1000",     # instruction bits
        before=dict(ir=0, t=-1),        # should be 0
        tick=dict(upc=0b1000),          #
        strict=True,                    #
    )

    test_clock_defaults(
        cpu, "NPI CND=11 NXT=1000",     # instruction bits
        before=dict(ir=0b111, t=-1),    # should be 0b111
        tick=dict(upc=0b1111),          #
        strict=True,                    #
    )


def test_t(cpu):

    # Try when loading from memory.
    test_clock_defaults(
        cpu, "TC MRE",
        before=dict(t=0),
        tock=dict(t=1337),
        strict=True,
        mval=1337,
    )

    # Try A and B/16 when loading from acc.
    test_clock_defaults(
        cpu, "TC ACW",
        before=dict(acc=1337, t=0),
        tock=dict(t=1337),
        strict=True,
    )

    # Check sign
    test_clock_defaults(
        cpu, "NPI=1 CND=1 NXT=1000",
        before=dict(t=100),
        tock=dict(t=100, upc=0b1000),
        strict=True,
    )
    test_clock_defaults(
        cpu, "NPI=1 CND=1 NXT=1000",
        before=dict(t=-100),
        tock=dict(t=-100, upc=0b1001),
        strict=True,
    )


def test_ir(cpu):

    # Try A and B/16 when loading from memory.
    test_clock_defaults(
        cpu, "IRC IRF=0 MRE",
        before=dict(ir=0),
        tock=dict(ir=1337),
        strict=True,
        mval=1337,
    )

    test_clock_defaults(
        cpu, "IRC IRF=1 MRE",
        before=dict(ir=1337),
        tock=dict(ir=1337/16),
        strict=True,
        mval=4242,
    )

    # Try A and B/16 when loading from acc.
    test_clock_defaults(
        cpu, "IRC IRF=0 ACW",
        before=dict(acc=1337, ir=0),
        tock=dict(ir=1337),
        strict=True,
    )

    test_clock_defaults(
        cpu, "IRC IRF=1 ACW",
        before=dict(acc=1337, ir=128),
        tock=dict(ir=128/16),
        strict=True,
    )


def test_pc(cpu):

    test_clock_defaults(
        cpu, "PCC PCF=0",
        before=dict(acc=1337, pc=100),
        tock=dict(pc=101),
        strict=True,
    )

    test_clock_defaults(
        cpu, "PCC PCF=1",
        before=dict(acc=1337, pc=100),
        tock=dict(pc=1337),
        strict=True,
    )


def test_sp(cpu):

    test_clock_defaults(
        cpu, "SPC SPF=0",
        before=dict(sp=100),
        tock=dict(sp=101),
        strict=True,
    )

    test_clock_defaults(
        cpu, "SPC SPF=1",
        before=dict(sp=100),
        tock=dict(sp=99),
        strict=True,
    )


def test_acc(cpu):

    test_clock_defaults(
        cpu, "MRE ACC ACF=00",
        before=dict(acc=1111),
        tock=dict(acc=1111*2),
        strict=True,
        mval=1212,
    )

    test_clock_defaults(
        cpu, "MRE ACC ACF=01",
        before=dict(acc=1111),
        tock=dict(acc=1111*2 + 1),
        strict=True,
        mval=1212,
    )

    test_clock_defaults(
        cpu, "MRE ACC ACF=10",
        before=dict(acc=1111),
        tock=dict(acc=1212),
        strict=True,
        mval=1212,
    )

    test_clock_defaults(
        cpu, "MRE ACC ACF=11",
        before=dict(acc=1111),
        tock=dict(acc=1212-1111),
        strict=True,
        mval=1212,
    )

    test_clock_defaults(
        cpu, "MRE ACC ACF=11",
        before=dict(acc=1212),
        tock=dict(acc=1111-1212),
        strict=True,
        mval=1111,
    )


def test_cr0(cpu):

    test_clock_defaults(
        cpu, "ACW C0C",
        before=dict(acc=1212, cr0=0),
        tock=dict(cr0=1212),
        strict=True,
    )

    test_clock_defaults(
        cpu, "ACW C0C",
        before=dict(acc=1212, cr0=1111),
        tock=dict(cr0=0),
        strict=True,
    )


def test_mad(cpu):

    for cr0 in [0, 0xfff]:

        test_clock_defaults(
            cpu, "MAD=00 MRE",
            before=dict(pc=0x1100, acc=0x1200, sp=0x1300, t=0x1400, cr0=cr0),
            tock=dict(mres=[(0x1100 | cr0, 0x4242)]),
            mval=0x4242,
        )

        test_clock_defaults(
            cpu, "MAD=01 MRE",
            before=dict(pc=0x1100, acc=0x1200, sp=0x1300, t=0x1400, cr0=cr0),
            tock=dict(mres=[(0x1200 | cr0, 0x4242)]),
            mval=0x4242,
        )

        test_clock_defaults(
            cpu, "MAD=10 MRE",
            before=dict(pc=0x1100, acc=0x1200, sp=0x1300, t=0x1400, cr0=cr0),
            tock=dict(mres=[(0x1300 | cr0, 0x4242)]),
            mval=0x4242,
        )

        test_clock_defaults(
            cpu, "MAD=11 MRE",
            before=dict(pc=0x1100, acc=0x1200, sp=0x1300, t=0x1400, cr0=cr0),
            tock=dict(mres=[(0x1400 | cr0, 0x4242)]),
            mval=0x4242,
        )



def all_tests(microstore, memsz):

    memory = hardware.DebugMemory([0] * memsz)
    print("[+] Plugged in %d memory words." % len(memory))

    cpu = hardware.CPU(ustore=microstore, memory=memory)
    print("[+] Plugged in CPU.")

    print("[+] Running tests.")

    test_npi(cpu)
    test_upc_select(cpu)
    test_t(cpu)
    test_ir(cpu)
    test_pc(cpu)
    test_sp(cpu)
    test_acc(cpu)
    test_cr0(cpu)
    test_mad(cpu)
