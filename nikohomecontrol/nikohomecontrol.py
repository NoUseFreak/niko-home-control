#!/usr/bin/env python3

'''
.. module:: nikohomecontrol
    :platform: Unix, Windows
    :synopsis: Python API to interact with Niko Home Control
    :noindex:
'''
import json

from . import nhcconnection


class NikoHomeControlException(Exception): pass
class ActionError(NikoHomeControlException): pass


class NikoHomeControl:

    def __init__(self, config):
        self._config = config
        self.connection = nhcconnection.NikoHomeControlConnection(config['ip'], config['port'])

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
        data = json.loads(self.connection.send(cmd))
        if 'error' in data['data'] and data['data']['error'] > 0:
            error = data['data']['error']
            if error == 100:
                raise ActionError('NOT_FOUND')
            if error == 200:
                raise ActionError('SYNTAX_ERROR')
            if error == 300:
                raise ActionError('ERROR')

        return data
