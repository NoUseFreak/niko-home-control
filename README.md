# Niko Home Control

A Python tool to communicate with a Niko Home Control system via the Netcat TCP socket.

## Installation

````bash
pip install niko-home-control
````

## Dependencies

Niko Home Control requires the python modules `setuptools` and `nclib`. In order to install them:

```bash
pip install -r requirements.txt
```

## Modules and commands

`nhcmonitor.py` will listen to your Niko Home Control installation and will print the communication
it receives from the system.
`nikohomecontrol.py` is the main module you can use to interact with your Niko Home Control system.
`nhcconnection.py` makes the TCP connection towards your Niko Home Control system.

## Quickstart

### Basic commands

For every basic command, you will need to setup the `NikoHomeControl` class:

```python
niko = NikoHomeControl({
	'ip': '192.168.22.105',
	'port': 8000,
	'timeout': 20000,
	'events': True
})
```

Now you will be able to interact with your Niko Home Control system:

```python
print(niko.system_info())
print(niko.list_locations())
print(niko.list_energy())
print(niko.list_actions())
print(niko.list_thermostats())
```

### Niko Home Control Monitor

Setting up a monitor to listening to your Niko Home Control system is easy as:

````python
monitor = NikoHomeControlMonitor(ip: '192.168.22.105', port:8000)
monitor.listen()
````

# License

(https://opensource.org/licenses/MIT)[MIT] Author: Dries De Peuter

# Contributors

* (https://github.com/legovaer)[Levi Govaerts]
