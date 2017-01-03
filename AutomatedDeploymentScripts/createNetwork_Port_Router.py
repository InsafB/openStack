#!/usr/bin/env python
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient
import os_client_config
import os

from credentials import get_credentials
from credentials import get_nova_credentials
from credentials import get_nova_credentialv2
from utils import print_values_server

## Client
nova2_credentials = get_nova_credentials_v2()
nova2_client = os_client_config.make_client('compute',**nova2_credentials)

credentials = get_credentials()
neutron = client.Client(**credentials)


def createNetwork():
	network1_name = 'private_network1'
	try:	
		body_create_network1 = {'network': {'name': network1_name,'admin_state_up': True}}
		network1 = neutron.create_network(body=body_create_network1)
		network1_dict = network1['network']
		network1_id = network1_dict['id']
		print('Network %s has been successfuly created' % network1_id)

		body_create_subnet1 = {'subnets': [{'cidr': '192.168.0.0/24','ip_version': 4, 'network_id': network1_id}]}
		subnet1 = neutron.create_subnet(body=body_create_subnet1)
		print('SubNetwork %s has been successfuly created' % subnet1)

	finally:
		print("Create Network: Execution completed")
	return network1_id


def createRouter():
	neutron = client.Client(**credentials)
	neutron.format = 'json'
	request = {'router': {'name': 'router1','admin_state_up': True}}
	router = neutron.create_router(request)
	router1_id = router['router']['id']
	print("Create Router: Execution Completed")
	return router1_id


def createPort()
	body_create_port1 = {'port': {'admin_state_up': True,'device_id': router1_id,'name': 'port1','network_id': network1_id}}
	response = neutron.create_port(body=body_create_port1)
	print(response)
	print("Add Port to Network: Execution Completed")
