#!/usr/bin/env python3

'''
.. module:: nikohomecontrol
    :platform: Unix, Windows
    :synopsis: Python API to interact with Niko Home Control
    :noindex:
'''

import socket
import json
from io import StringIO

class NikoHomeControl:

    def __init__(self, config):
        self._config = config
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((config['ip'], config['port']))

    def __del__(self):
        self._socket.shutdown(1)
        self._socket.close()

    def system_info(self):
        return self._command('{"cmd":"systeminfo"}')

    def list_actions(self):
        return self._command('{"cmd":"listactions"}')

    def list_energy(self):
        return self._command('{"cmd":"listenergy"}')

    def list_locations(self):
        return self._command('{"cmd":"listlocations"}')

    def execute_actions(self, id, value):
        return self._command('{"cmd":"executeactions", "id": "'+id+'", "value": "'+value+'"}')

    def _command(self, cmd):
        self._socket.send(cmd.encode())
        data = json.load(StringIO(self._socket.recv(4096).decode()))

        if ('error' in data['data'] and data['data']['error'] > 0):
            error = json['data']['error']
            if (error == 100):
                raise Error('NOT_FOUND')
            if (error == 200):
                raise Error('SYNTAX_ERROR')
            if (error == 300):
                raise Error('ERROR')

        return data
