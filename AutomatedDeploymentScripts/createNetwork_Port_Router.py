#!/usr/bin/env python
from neutronclient.v2_0 import client
import novaclient.v2.client as nvclient
from credentials import get_credentials
from credentials import get_nova_credentials
from utils import print_values_server

## Client & NovaClient
credentials = get_credentials()
nova_credentials = get_nova_credentials()
client = os_client_config.make_client('compute',**credentials)
nova_client = os_client_config.make_client('compute',**nova_credentials)


## Create Network
network1_name = 'private_network1'
try:	
	body_create_network1 = {'network': {'name': network1_name,'admin_state_up': True}}
	network1 = neutron.create_network(body=body_create_network1)
	network1_dict = network1['network']
	network1_id = net_dict['id']
	print('Network %s has been successfuly created' % network1_id)

	body_create_subnet1 = {'subnets': [{'cidr': '192.168.199.0/24','ip_version': 4, 'network_id': network1_id}]}
	subnet1 = neutron.create_subnet(body=body_create_subnet1)
	print('SubNetwork %s has been successfuly created' % subnet1)

finally:
	print("Create Network: Execution completed")



## Create Port
server1_id = '0c6f61bc-b855-4f9e-aae5-83c89014d137'
server1_details = nova_client.servers.get(server1_id)

if server1_detail != None:
	body_create_port1 = {
		     "port": {
		             "admin_state_up": True,
		             "device_id": server1_id,
		             "name": "port1",
		             "network_id": network1_id
		      }
		 }
	response = neutron.create_port(body=body_create_port1)
	print(response)
	print("Create Port: Execution Completed")


## Create Router
neutron = client.Client(**credentials)
neutron.format = json
request = {'router': {'name': 'router','admin_state_up': True}}
router = neutron.create_router(request)
router_id = router['router']['id']
print("Create Router: Execution Completed")


## Add Port to Network
body_add_port1 = {'port': {'admin_state_up': True,'device_id': router_id,'name': 'port1','network_id': network1_id}}
response = neutron.create_port(body=body_add_port1)
print(response)
print("Add Port to Network: Execution Completed")
