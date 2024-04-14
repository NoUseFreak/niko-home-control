#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcmonitor.py

asyncio-based event monitor for Niko Home Control

Author: Jeroen Vaes
"""

import asyncio
import json

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
    @classmethod
    async def create(cls, ip, port):
        self = NikoHomeControlMonitor()
        self._callback = []
        self._reader, self._writer = await asyncio.open_connection(ip, port)

        return self

    def add_callback(self, func):
        self._callback.append(func)

    async def _listen(self):
        """Listen for events."""
        s = '{"cmd":"startevents"}'

        self._writer.write(s.encode())
        await self._writer.drain()

        async for line in self._reader:
            try:
                message = json.loads(line.decode())
                if "event" in message and message["event"] == "listactions":
                    event = Event(message["event"], message["data"])
                    for data in message["data"]:
                        event = Event(message["event"], data)
                        for func in self._callback:
                            await func(event)
            except Exception as e:
                print(e)
    
    def start_listener(self):
        self._listen_task = asyncio.create_task(self._listen())

    def stop_listener(self):
        self._listen_task.cancel()

async def callback(event):
    print(event.type)
    print(event.id)
    print(event.value1)

async def main():
    mon = await NikoHomeControlMonitor.create(ip='192.168.4.6', port=8000)
    mon.add_callback(callback)
    mon.start_listener()

    await asyncio.sleep(10)
    mon.stop_listener()

asyncio.run(main())