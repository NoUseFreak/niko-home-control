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
        return [Action(action, self) for action in self.list_actions_raw()]

    def list_energy(self):
        return self._command('{"cmd":"listenergy"}')

    def list_locations_raw(self):
        return self._command('{"cmd":"listlocations"}')

    def list_locations(self):
        return [Location(location) for location in self.list_locations_raw()]

    def list_thermostats_raw(self):
        return self._command('{"cmd":"listthermostat"}')

    def list_thermostats(self):
        return [Thermostat(thermostat, self) for thermostat in self.list_thermostats_raw()]

    def execute_actions(self, id, value):
        return self._command('{"cmd":"executeactions", "id": "'+str(id)+'", "value1": "'+str(value)+'"}')

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

        return data['data']


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


class Thermostat:
    """The class used for handling thermostats"""

    def __init__(self, thermostat, hub):
        """Setup a Niko Home Control thermostat"""
        self._hub = hub
        self._id = thermostat['id']
        self._name = thermostat['name']
        self._location = thermostat['location']
        self._measured = self._transform_temp(thermostat['measured'])
        self._setpoint = self._transform_temp(thermostat['setpoint'])
        self._mode = thermostat['mode']
        self._overrule = self._transform_temp(thermostat['overrule'])
        self._overruletime = thermostat['overruletime']
        self._ecosave = thermostat['ecosave']

    @staticmethod
    def _transform_temp(temp):
        """Niko returns values for temprature in 3 digits without a delimiter."""
        temp = str(temp)
        if len(temp) == 3:
            return float(temp[0] + temp[1] + "." + temp[2])
        elif len(temp) == 1:
            return float(0.0)
        else:
            raise NikoHomeControlException("ILLEGAL_TEMPERATURE_VALUE")

    @property
    def id(self):
        """Return the unique id of the thermostat"""
        return self._id

    @property
    def name(self):
        """Return the display name of this thermostat"""
        return self._name

    @property
    def location(self):
        """Return the id of the location"""
        return self._location

    @property
    def measured(self):
        """Return the (formatted) measured temprature"""
        return self._measured

    @property
    def setpoint(self):
        """Return the (formatted) temperature that has been set"""
        return self._setpoint

    @property
    def mode(self):
        """Return the id of the mode that has been selected"""
        return self._mode

    @property
    def overrule(self):
        """Return the (formatted) temperature that has been set"""
        return self._overrule

    @property
    def overruletime(self):
        """Return the time that the temperature will be overruled"""
        return self._overruletime

    @property
    def ecosave(self):
        """Return if the eco save mode has been enabled"""
        return self._ecosave

    def update(self):
        """Update all data of this thermostat via the Niko Home Control API"""
        data = next(filter(lambda a: a['id'] == self._id, self._hub.list_thermostats()))
        self._name = data['name']
        self._location = data['location']
        self._measured = self._transform_temp(data['measured'])
        self._setpoint = self._transform_temp(data['setpoint'])
        self._mode = data['mode']
        self._overrule = data['overrule']
        self._overruletime = data['overruletime']
        self._ecosave = data['ecosave']

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
    print(niko.list_actions_raw())
    print(niko.list_thermostats())

if __name__ == '__main__':
    list()
