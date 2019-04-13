#!/usr/bin/env python3

'''
.. module:: nikohomecontrol
    :platform: Unix, Windows
    :synopsis: Python API to interact with Niko Home Control
    :noindex:
'''
import json

from . import nhcconnection


class NikoHomeControlException(Exception):
    pass


class ActionError(NikoHomeControlException):
    pass


class NikoHomeControl:

    def __init__(self, config):
        self._config = config
        self.connection = nhcconnection.NikoHomeControlConnection(
            config['ip'], config['port'])

    def system_info(self):
        return self._command('{"cmd":"systeminfo"}')

    def list_actions_raw(self):
        return self._command('{"cmd":"listactions"}')

    def list_actions(self):
        return [Action(action, self) for action in self.list_actions_raw()])

    def list_energy(self):
        return self._command('{"cmd":"listenergy"}')

    def list_locations_raw(self):
        return self._command('{"cmd":"listlocations"}')

    def list_locations(self):
        return [Location(location) for location in self.list_locations_raw()]

    def execute_actions(self, id, value):
        return self._command('{"cmd":"executeactions", "id": "'+id+'", "value1": "'+value+'"}')

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

class Location:
    def __init__(self, location):
        self._state = location

    @property
    def id(self):
        return self._state['id']

    @property
    def name(self):
        return self._state['name']

class Action:
    def __init__(self, action, hub):
        self._id = action['id']
        self._state = action
        self._hub = hub

    @property
    def name(self):
        return self._state['name']

    @property
    def id(self):
        return self._state['id']

    @property
    def is_on(self):
        return self._state['value1'] != 0

    def turn_on(self, brightness=255):
        return self._hub.execute_actions(self._id, brightness)

    def turn_off(self):
        return self._hub.execute_actions(self._id, 0)

    def toggle(self):
        if (self.is_on):
            return self.turn_off()
        else:
            return self.turn_on()

    def update(self):
        self._state = next(filter(lambda a: a['id'] == self._id, self._hub.list_actions_raw()))



def list():
    niko = NikoHomeControl({
        'ip': '192.168.22.60',
        'port': 8000,
        'timeout': 2000,
        'events': True
    })
    print(niko.system_info())
    print(niko.list_locations())
    print(niko.list_energy())
    print(niko.list_actions())

if __name__ == '__main__':
    list()

