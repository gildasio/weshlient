#!/usr/bin/env python3

import os
import readline

def command_clear(null=''):
    os.system("clear")

def command_exit(null=''):
    print("\nExiting...")
    exit()

COMMANDS = {
    'clear': command_clear,
    'exit': command_exit
}

def special_commands(command):
    COMMANDS[command.split()[0]](command)

def execute_command(command):
    if command == '':
        pass
    elif command.split()[0] in COMMANDS:
        special_commands(command)
    else:
        print("TBD")

if __name__ == "__main__":
    while True:
        try:
            PS1 = '$ '
            command = input(PS1)
            execute_command(command)
        except (KeyboardInterrupt, EOFError) as e:
            command_exit()

