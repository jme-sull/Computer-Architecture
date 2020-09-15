#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def main(argv):

    if len(argv) != 2:
        print(f'usageL {argv[0]} filename', file=sys.stderr)
        return 1

    cpu = CPU()

    cpu.load(argv[1])
    cpu.run()

    return 0