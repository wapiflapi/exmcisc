#!/usr/bin/env python3

import hardware
import ustore
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("ucode", type=argparse.FileType("r"))
    parser.add_argument("-m", "--memsz", type=int, default=16*1024)
    args = parser.parse_args()

    microcode = args.ucode.read()
    microstore = ustore.build_ustore(hardware.CPU, microcode)
    print("[+] Plugged in %d microstore entries." % len(microstore))

    memory = [0] * args.memsz
    print("[+] Plugged in %d memory words." % len(memory))

    cpu = hardware.CPU(ustore=microstore, memory=memory)
    print("[+] Plugged in CPU.")


if __name__ == "__main__":
    main()
