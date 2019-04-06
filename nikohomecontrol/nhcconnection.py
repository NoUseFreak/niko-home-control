#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcconnection.py

This is a tool to communicate with Niko Home Control.

You will have to provide an IP address and a port number.

License: MIT https://opensource.org/licenses/MIT
Source: https://github.com/NoUseFreak/niko-home-control
Author: Dries De Peuter
"""

__version__ = '0.1'

import nclib

NHC_TCP_PORT = 8000
NHC_TIMEOUT = 20000


# version-access:
def get_version():
    return __version__


class NikoHomeControlConnection:

    def __init__(self, ip, port=NHC_TCP_PORT):
        self._socket = nclib.Netcat((ip, port), udp=False)

    def __del__(self):
        self._socket.shutdown(1)
        self._socket.close()

    def receive(self):
        """
        Receives information from the Netcat socket.
        """
        return self._socket.recv().decode()

    def read(self):
        return self._receive_until(b'\r')

    def _receive_until(self, s):
        """
        Recieve data from the socket until the given substring is observed.
        Data in the same datagram as the substring, following the substring,
        will not be returned and will be cached for future receives.
        """
        return self._socket.recv_until(s)

    def send(self, s):
        """
        Sends the given command to Niko Home Control and returns the output of
        the system.

        Aliases: write, put, sendall, send_all
        """
        self._socket.send(s.encode())
        return self.read()
