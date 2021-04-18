#!/usr/bin/env python3
# Use python3 -m pip install pwntools colorama

from pathlib import Path
import sys

import colorama
from pwnlib.tubes.process import process
from termcolor import cprint

zork_path = sys.argv[1]
input_lines = Path(sys.argv[2]).read_bytes().split(b'\n')

colorama.init(strip=False) # This will make termcolor work on Windows too!

def showInput(line):
    cprint(repr(line)[2:-1], 'blue', end='')

def showZork(reply):
    for rep_line in reply.decode().split('\n'):
        print()
        cprint(rep_line, 'green', end='')


zork = process(zork_path)
reply = zork.recv(timeout=0.1)
showZork(reply)
for line in input_lines:
    showInput(line)
    zork.sendline(line)
    reply = zork.recv(timeout=0.1)
    showZork(reply)

zork.shutdown('send')
reply = zork.recvall()
showZork(reply)
