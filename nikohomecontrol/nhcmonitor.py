#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcmonitor.py

Implement a tkinter-based grafic interface to view basic status- and
traffic-informations.

License: MIT https://opensource.org/licenses/MIT
Source: https://github.com/NoUseFreak/niko-home-control
Author: Levi Govaerts <legovaer@me.com>
"""

import logging
import json
import argparse

from . import nhcconnection


class NikoHomeControlMonitor:
    def __init__(self, ip, port=nhcconnection.NHC_TCP_PORT):
        self.connection = nhcconnection.NikoHomeControlConnection(ip, port)

    def listen(self):
        logging.info('Now listening for incoming TCP traffic ...')
        self.connection.send('{"cmd":"startevents"}')
        while True:
            data = self.connection.receive()
            if not data:
                break
            elif not data.isspace():
                print(json.loads(json.dumps(data)))

    def callback(self, cb):
        logging.info('Now listening for incoming TCP traffic ...')
        self.connection.send('{"cmd":"startevents"}')
        while True:
            data = self.connection.receive()
            if not data:
                break
            elif not data.isspace():
                d = json.loads(data)
                for item in d['data']:
                    cb(item)


# ---------------------------------------------------------
# terminal-output:
# ---------------------------------------------------------
def listen(ip, port=nhcconnection.NHC_TCP_PORT):
    print('\nNiko Home Control monitor:')
    NikoHomeControlMonitor(ip, port).listen()


# ---------------------------------------------------------
# cli-section:
# ---------------------------------------------------------
def _get_cli_arguments():
    parser = argparse.ArgumentParser(description='Niko Home Control Monitor')
    parser.add_argument('-i', '--ip-address',
                        nargs='?',
                        dest='ip',
                        help='ip-address of the Niko Home Control system to connect to. ')
    parser.add_argument('--port',
                        nargs='?', default=nhcconnection.NHC_TCP_PORT,
                        dest='port',
                        help='port of the Niko Home Control system to connect to. '
                             'Default: %s' % nhcconnection.NHC_TCP_PORT)
    args = parser.parse_args()
    return args


def _listen(arguments):
    listen(ip=arguments.ip, port=arguments.port)


def main():
    _listen(_get_cli_arguments())


if __name__ == '__main__':
    main()
