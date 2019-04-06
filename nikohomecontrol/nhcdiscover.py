#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nhcdiscover.py

License: MIT https://opensource.org/licenses/MIT
Source: https://github.com/NoUseFreak/niko-home-control
Author: Dries De Peuter <dries@nousefreak.be>
"""

import netaddr
import netifaces
from contextlib import closing
import socket

from . import nhcconnection
from . import nikohomecontrol


class NikoHomeControlDiscover:
    def find(self, port=nhcconnection.NHC_TCP_PORT):
        for ip in self._get_ip_set():
            if self._has_open_port(str(ip), int(port)):
                conn = nikohomecontrol.NikoHomeControl({
                    'ip': str(ip),
                    'port': int(port)
                })
                try:
                    conn.system_info()
                    return str(ip)
                except:
                    pass
        return None

    def _get_ip_set(self) -> str:
        IPSet = netaddr.IPSet()
        for ifaceName in netifaces.interfaces():
            for key, info in netifaces.ifaddresses(ifaceName).items():
                if self._valid_network(info):
                    network = netaddr.IPNetwork(
                        "%s/%s" % (info[0]['addr'], info[0]['netmask']))
                    IPSet.add(netaddr.IPRange(network.first, network.last))
        return IPSet

    def _valid_network(self, info: list) -> bool:
        if 'netmask' in info[0]:
            ip = netaddr.IPAddress(info[0]['addr'])
            return (ip.version == 4 and not ip.is_loopback())
        return False

    def _has_open_port(self, ip: str, port: int) -> bool:
        result = True
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.1)
            if not sock.connect_ex((ip, port)) == 0:
                result = False
        return result


def main():
    print(NikoHomeControlDiscover().find())

if __name__ == '__main__':
    main()
