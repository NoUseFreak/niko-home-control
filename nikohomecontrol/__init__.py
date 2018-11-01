#!/usr/bin/env python3

'''
.. module:: nikohomecontrol
    :platform: Unix, Windows
    :synopsis: Python API to interact with Niko Home Control
    :noindex:
'''
import json
import nclib

class NikoHomeControl:

    def __init__(self, config):
        self._config = config
        self._socket = nclib.Netcat((config['ip'], config['port']), udp=False)

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

    def item_state(self, id):
        data = self.list_actions()['data']
        for index, item in enumerate(data):
            if 'id' in item and str(item['id']) == str(id):
                return item
        return False

    def _command(self, cmd):
        self._socket.send(cmd.encode())
        data = json.loads(self._socket.recv_until(b'\r'))
        if ('error' in data['data'] and data['data']['error'] > 0):
            error = json['data']['error']
            if (error == 100):
                raise Error('NOT_FOUND')
            if (error == 200):
                raise Error('SYNTAX_ERROR')
            if (error == 300):
                raise Error('ERROR')

        return data
