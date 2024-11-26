#!/usr/bin/env python3

import argparse
import os
import readline
import requests

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

def request_parser(fd):
    method, path, version = fd.readline().split()
    headers = {}
    request = {}

    lines = fd.readlines()
    for line in lines:
        if line in (b'\n', b'\r\n'):
            break

        headers[line.split(b': ')[0]] = line.split(b': ')[1].strip()

    request['path'] = path
    request['method'] = method
    request['version'] = version
    request['headers'] = headers

    request['path'], *request['params'] = request['path'].split(b'?')
    request['params'] = request['params'][0] or b''

    request['body'] = ''
    if method == b'POST':
        request['body'] = lines[-1]

    if request['path'].startswith(b'http'):
        request['url'] = request['path']
    else:
        request['url'] = b'http://' + request['headers'][b'host'] + request['path']

    return request

def execute_command(request, command):
    if command == '':
        pass
    elif command.split()[0] in COMMANDS:
        special_commands(command)
    else:
        print(request)
        print("TBD")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("req", help="File containing raw http request", type=str)
    args = parser.parse_args()

    with open(args.req, 'rb') as fd:
        request = request_parser(fd)

    while True:
        try:
            PS1 = '$ '
            command = input(PS1)
            execute_command(request, command)
        except (KeyboardInterrupt, EOFError) as e:
            command_exit()

