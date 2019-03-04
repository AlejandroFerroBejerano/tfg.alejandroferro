#!/usr/bin/make -f
# -*- mode:makefile -*-

all:
	

run-server:
	./Server.py

run-server-v:
	./Server.py '-v'


run-server-to-log:
	./Server.py '-v' >> emulation_environment.log


run-client-1:
	./Client.py 'manager -t -e 1.1:tcp -h 192.168.240.250 -p 4000' alarm_z6_i6.csv '192.168.240.251'

run-client-2:
	./Client.py 'manager -t -e 1.1:tcp -h 192.168.240.250 -p 4000' alarm_z2_i6.csv '192.168.240.252'

run-clients:
	./Client.py 'manager -t -e 1.1:tcp -h 192.168.240.250 -p 4000' alarm_z6_i6.csv '192.168.240.251'&
	./Client.py 'manager -t -e 1.1:tcp -h 192.168.240.250 -p 4000' alarm_z2_i6.csv '192.168.240.252'&