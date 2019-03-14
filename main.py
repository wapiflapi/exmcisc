#!/usr/bin/env python3

import hardware
import ustore
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('ucode', type=argparse.FileType('r'))
    args = parser.parse_args()

    ucode = args.ucode.read()
    ustore.build_ustore(hardware.CPU, ucode)


if __name__ == "__main__":
    main()
