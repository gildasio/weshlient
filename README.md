# Wshlient

Web Shell Client

## Description & Demo

`Wshlient` is a web shell client designed to be pretty simple yet versatile. One
just need to create a text file containing an HTTP request and inform where
`Wshlient` inject the commands, then you can enjoy a shell.

## Installation

Out of python's included batteries `Wshclient` only uses `requests`. Just
install it directly or using `requirements.txt`:

```
$ git clone https://github.com/gildasio/wshlient
$ cd wshlient
$ pip install -r requirements.txt
$ ./wshlient.py -h
```

Alternatively you can also create a symbolic link in your `$PATH` to use it
directly anywhere in the system:

```
$ ln -s $PWD/wshlient.py /usr/local/bin/wshlient
```

## Usage

```
$ ./wshlient.py -h
usage: wshlient.py [-h] [-d] [-i] [-ne] [-it INJECTION_TOKEN] [-st START_TOKEN] [-et END_TOKEN] req

positional arguments:
  req                   File containing raw http request

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug output
  -i, --ifs             Replaces whitespaces with $IFS
  -ne, --no-url-encode  Disable command URL encode
  -it INJECTION_TOKEN, --injection-token INJECTION_TOKEN
                        Token to be replaced by commands (default: INJECT)
  -st START_TOKEN, --start-token START_TOKEN
                        Token that marks the output beginning
  -et END_TOKEN, --end-token END_TOKEN
                        Token that marks the output ending
```

## Contributing

You can contribute to `Wshlient` by:

- Using and sharing it :)
- Firing a bug / issue
- Suggesting interesting features
- Coding

Feel free to do it, but keep in mind to keep it simple.

