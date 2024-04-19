#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcmonitor.py

asyncio-based event monitor for Niko Home Control

Author: Jeroen Vaes
"""

import asyncio
import json
import inspect

class Event:
    def __init__(self, type, data):
        self.type = type
        self._state = data

    @property
    def id(self):
        return self._state['id']

    @property
    def value1(self):
        return self._state['value1']

    @property
    def value2(self):
        return self._state['value2']

class NikoHomeControlMonitor:
    def __init__(self, ip, port):
        self._callback = []
        self._ip = ip
        self._port = port

    def add_callback(self, func):
        """Add callback function for events."""
        if inspect.isfunction(func) \
                and len(inspect.signature(func).parameters) == 1:
            self._callback.append(func)
        else:
            raise Exception("Only use functions with 1 parameter as callback.")

    async def _listen(self):
        """
        Listen for events. When an event is received, call callback functions.
        """
        s = '{"cmd":"startevents"}'

        try:
            self._reader, self._writer = \
                await asyncio.open_connection(self._ip, self._port)

            self._writer.write(s.encode())
            await self._writer.drain()

            async for line in self._reader:
                message = json.loads(line.decode())
                if "event" in message \
                        and message["event"] != "startevents":
                    event = Event(message["event"], message["data"])
                    for data in message["data"]:
                        event = Event(message["event"], data)
                        for func in self._callback:
                            func(event)
        finally:
            self._writer.close()
            await self._writer.wait_closed()

    def start_listener(self):
        """Create an asyncio task for the listener."""
        self._listen_task = asyncio.create_task(self._listen())

    def stop_listener(self):
        """Stop the listener."""
        self._listen_task.cancel()

def callback(event):
    print(f"Event received! Type: {event.type}, " \
          "Id: {event.id}, Value: {event.value1}")

async def main():
    mon = NikoHomeControlMonitor(ip='192.168.4.6', port=8000)
    mon.add_callback(callback)
    mon.start_listener()

    await asyncio.sleep(60)
    mon.stop_listener()

asyncio.run(main())