#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import requests, requests.exceptions, sys, datetime, ast, json
from requests.auth import HTTPBasicAuth
import Ice
Ice.loadSlice('ochozi.ice')
import ochozi


class ListenerI(ochozi.Listener):

    default_url = 'http://127.0.0.1:8081/api/'
    hw_uri = 'hw/?address='
    device_uri = 'device/?controller='
    event_uri = '?'
    user = 'alejandro'
    password = 'ojuanisa'
    argv = 1
    warning_no_url = 'No custom server url passed, the following url will be used by default: '
    verbose = False
    if len(sys.argv) < 2:
        print ' WARNING:-> ' + warning_no_url + default_url + '\n'
        argv+=argv
        assert  warning_no_url + default_url
    elif sys.argv[len(sys.argv) - argv ] == '-v':
        verbose  = True
    else:
        default_url = sys.argv[2]

    def report(self, node, current=None):

        for node_event in self.get_state(node):
            self.print_event(node_event)
            if self.valid_url(self.default_url):
                hw = self.get_hw(node_event['id'].split(':')[0])
                if hw != False:
                    device_list = self.get_device(hw)
                    if len(device_list) > 0:
                        event = self.build_event(node_event, hw, device_list)
                        if event != False:
                            self.post_event(event)
                else:
                    pass
                    

    def print_event(self, node_event):
        now = datetime.datetime.now()
        msg = now.strftime('%d-%m-%Y %H:%M:%S') + ' -> ' + ' Nodo: ' +  node_event['id'] + ' Zona: ' + node_event['id_dev'] + ' en ' + node_event['state']
        print msg
        return msg

    def print_msg(self, msg):
        if self.verbose:
            print msg

    def valid_url(self, url):
        try:
            ret = requests.get(url, auth=(self.user, self.password))
            if (ret.status_code / 100 >= 4):
                print url
                self.print_msg('\n WARNING: Wrong url for api functionality, check it!! \n')
                return False
            elif(ret.status_code == 200):
                self.print_msg('\n SUCCESS: \''+ url + '\' url validated. \n')
                return True
        except(requests.exceptions.ConnectionError, requests.exceptions.MissingSchema) as e:
            self.print_msg('\n ERROR: No correct format or alive url was given!! \n')
            print e

    def get_hw(self, address):
        if self.valid_url(self.default_url + self.hw_uri + address):
            url = str(self.default_url + self.hw_uri + address)
            ret = requests.get(url, auth=(self.user, self.password))
            hw_list = ast.literal_eval(json.dumps(ret.json()['results']))
            if len(hw_list) > 0:
                self.print_msg('\n SUCCESS: Access to hardware achived \n')
                return hw_list[0]
            else:
                self.print_msg('\n WARNING: No Hardware whith the '+ address + 'IP address found!! \n')
        else:
            self.print_msg('\n WARNING: No Hardware whith the '+ address + 'IP address found!! \n')
        return False
        

    def get_device(self, hw):
        if self.valid_url(self.default_url + self.device_uri + str(hw['id'])):
            ret = requests.get(self.default_url + self.device_uri + str(hw['id']), auth=(self.user, self.password))
            device_list = ast.literal_eval(json.dumps(ret.json()['results']))
            if len(device_list) > 0:
                self.print_msg('\n SUCCESS: Access to devices achived \n')
        else:
            self.print_msg('\n WARNING: No Device whith '+ hw['description'] +'controller found!! \n')
        return device_list

    def build_event(self, node_event, hw, device_list):
        i_zone = int(node_event['id_dev'])
        if  i_zone + 1 <= len(device_list):
            device = device_list[i_zone]
            event = {
                'timestamp': str(datetime.datetime.now()).split('.')[0],
                'kind': device['mode'],
                'description': device['description'],
                'location': device['location'],
                'status': node_event['l_cod']
            }
            if self.new_event(event, device):
                return event
        else:
            self.print_msg('\n WARNING: Ghost event recived, the event ' + self.print_event(node_event) + ' will not be created!! \n')
        return False

    def post_event(self, event):
        if self.valid_url(self.default_url):
            ret = requests.post(self.default_url + '?format=api', event, auth=(self.user, self.password))
            if ret.status_code == 201:
                self.print_msg('\n SUCCESS: Event created \n')
            else:
                self.print_msg('\n WARNING: Something gone wrong, no event created yet \n')
                print'\n WARNING: Something gone wrong, no event created yet \n' + str(ret.status_code)
                print event

    def new_event(self, event, device):
        d_uri = 'description=' + device['description']
        retval = False
        if self.valid_url(self.default_url + self.event_uri + d_uri):
            ret = requests.get(self.default_url + self.event_uri + d_uri, auth=(self.user, self.password))
            event_list = ast.literal_eval(json.dumps(ret.json()['results']))
            if len(event_list) == 0:
                retval = True
                self.print_msg('\n SUCCESS: New event status validated \n')
            elif len(event_list) > 0:
                last_e = event_list[-1]
                self.print_msg('\n SUCCESS: Previous event obtained \n')
                if last_e['status'] != event['status']:
                    self.print_msg('\n SUCCESS: New event status validated \n')
                    retval = True
                else:
                    self.print_msg('\n SUCCESS: Existing event status validated, No new event will be recorded \n')
                    retval = False
            else:
                self.print_msg('\n WARNING: No existing event whith ' + device['description'] + ' description \n')
        else:
            self.print_msg('\n WARNING: No api aviable for event query in this url!! \n')
        return retval

    def get_state(self, node, current=None):
        retval = []
        for n in node.zones:
            retval.append(self.zone_inspector(n))
        return retval

    def zone_inspector(self, zone, current=None):
        state = ''
        retval = {}
        l_cod = 1
        if 820 <= zone.value <= 840:
            state = 'Alarma'
            l_cod = 1
        elif 400 <= zone.value <= 420:
            state = 'Reposo'
            l_cod = 2
        elif zone.value >= 841:
            state = 'Tamper'
            l_cod = 4 
        else:
            state = 'Cortocircuito'
            l_cod = 5

        retval = { 'id': zone.identifier.split(':')[0], 'state': state, 'l_cod': l_cod, 'id_dev': zone.identifier.split(':')[1]}
        return retval  

# class Callback


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ListenerI()

        adapter = broker.createObjectAdapterWithEndpoints('Adapter', 'tcp -p 4000')
        proxy = adapter.add(servant, broker.stringToIdentity('manager'))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
