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
    cprint(repr(line)[2:-1], 'green', attrs=['bold'], end='')

def showZork(reply):
    for rep_line in reply.decode("ascii", errors="replace").split('\n'):
        print()
        print(rep_line, end='')

# Start the game:
zork = process(zork_path)

# Wait for the mailbox prompt:
reply = zork.recvuntil('>', timeout=0.1)
showZork(reply)
try:
    for line in input_lines:
        showInput(line + b'\n')
        zork.sendline(line)
        reply = b''
        add_reply = b''
        while True:
            # NOTE: Need to keep reading '>' until a short timeout, because sometimes multiple commands
            #       happen in one input line, and Zork will output multiple prompts as it loops through and processes them.
            add_reply = zork.recvuntil('>', timeout=0.01)
            reply += add_reply
            if add_reply == b'':
                break
        if reply == b'':
            reply = zork.recv(timeout=0.01)
        showZork(reply)
except EOFError:
    pass
finally:
    zork.shutdown('send')
    reply = zork.recvall()
    showZork(reply)
