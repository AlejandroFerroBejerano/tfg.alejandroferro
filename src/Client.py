#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, csv, time
import socket
import Ice
Ice.loadSlice('ochozi.ice')
import ochozi


class Client(Ice.Application):
    node_id = '127.0.0.2'
    time_between_messages = 4
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        manager = ochozi.ListenerPrx.checkedCast(proxy)
        
        if len(sys.argv) == 2:
            assert "An fixture file is required!"
        fixture_file = argv[2]

        if len(sys.argv) == 3:
         assert  "An Ip address are required"
        ipaddres = argv[3]

        if self.check_ip_format(ipaddres):
            self.node_id = ipaddres
        else:
            print 'Invalid IP address' + self.node_id
            raise RuntimeError('Invalid IP address')

        if not manager:
            raise RuntimeError('Invalid proxy')

        with open(fixture_file, 'rb') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):

                zones = self.create_zones(row[:6])
                outputs = [bool(int(i)) for i in row[6:]]
                manager.report(ochozi.NodeStatus(zones, outputs))
                time.sleep(self.time_between_messages)

        return 0

    def create_zones(self, values):
        retval = []
        for i, value in enumerate(values):
            identity = "{}:{}".format(self.node_id, i)
            retval.append(ochozi.Zone(identity, int(value)))
        return retval

    def check_ip_format(self, ipaddres):
        try:
            socket.inet_aton(ipaddres)
            return True
        except socket.error:
            return False


sys.exit(Client().main(sys.argv))
