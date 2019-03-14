#!/usr/bin/env python3

import argparse
import logging

import hardware
import ustore
import tests


logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("ucode", type=argparse.FileType("r"))
    parser.add_argument("-m", "--memsz", type=int, default=16*1024)
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    microcode = args.ucode.read()
    microstore = ustore.build_ustore(hardware.CPU, microcode)
    print("[+] Loaded %d microstore entries." % len(microstore))

    tests.all_tests(microstore, args.memsz)


if __name__ == "__main__":
    main()
