#!/usr/bin/env python3

import hardware
import ustore


def main():
    ustore.build_ustore(hardware.CPU, ustore.MICROCODE)


if __name__ == "__main__":
    main()
