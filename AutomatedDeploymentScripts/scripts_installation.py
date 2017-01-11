import os_client_config
import os
import paramiko
import credentials
from neutronclient.v2_0 import client
from swiftclient.client import Connection, ClientException
from credentials import *
from utils import *
import time

DNS = {} 


def createNetwork(network_name):
	credentials = get_credentials()
	neutron = client.Client(**credentials)
	try:	
		body_create_network = {'network': {'name': network_name,'admin_state_up': True}}
		network = neutron.create_network(body=body_create_network)
		network_dict = network['network']
		network_id = network_dict['id']
		print('Network %s has been successfuly created' % network_id)
		body_create_subnet = {'subnets': [{'cidr': '10.0.1.0/24','ip_version': 4,'gateway_ip': '10.0.1.254', 'dns_nameservers': ['10.11.50.1'], 'network_id': network_id}]}
		subnet = neutron.create_subnet(body=body_create_subnet)
		print('SubNetwork %s has been successfuly created' % subnet)
	finally:
		print("Create Network: Execution completed")
	return network_id, subnet['id']

def createRouter(router_name,subnet_id):
	credentials = get_credentials()
	neutron = client.Client(**credentials)
	neutron.format = 'json'
	external_network=neutron.list_networks(name='external-network')
	request = {'router': {'name': router_name,'admin_state_up': True,'subnet_id':subnet_id, 'external_gateway_info':{"network_id":external_network['networks'][0]['id']}}}
	router = neutron.create_router(request)
	router_id = router['router']['id']
	print("Create Router: Execution Completed")
	return router_id

def createPort(port_name,router_id,network_id):
	credentials = get_credentials()
	neutron = client.Client(**credentials)
	body_create_port = {'port': {'admin_state_up': True,'device_id': router_id,'name': port_name,'network_id': network_id}}
	response = neutron.create_port(body=body_create_port)
	print(response)
	print("Add Port to Network: Execution Completed")
	

def exec_commands(commands,server):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(server)    
	for cmd in commands:
		print "executing command : ",cmd
		client_stdin, client_stdout, client_stderr = client.exec_command(cmd);
		exit_status = client_stdout.channel.recv_exit_status()
		print "exit status for command '",cmd," is : ",exit_status

def appendHost(ip,ServerName,dest):
	command = "echo '"+ip+"    "+ServerName+"' >> /etc/hosts"
	commands = [command]
	exec_commands(commands,dest)

def appendHostLocal(ip,ServerName):
	command = "echo '"+ip+"    "+ServerName+"' | sudo tee -a /etc/hosts"
	os.system(command)

def set_dns():
	dests = list(DNS.keys())

	for dest in dests:

		for keydsn, value in DNS.items():

			appendHost(keydsn,value,dest)

def install_mysql(server):
	commands=["sudo apt-get update","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password othmane'","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password othmane'","sudo apt-get -y install mysql-server"]
	exec_commands(commands,server)

def getNovaClient():
	## Nova Client
	credentials = get_nova_credentials_v2()
	nova_client = os_client_config.make_client('compute',**credentials)
	return nova_client

def getSwiftConn():
	return Connection(**get_session_credentials())

def createSwiftContainers(Containers):
	conn = getSwiftConn()
	for Container in Containers:
		conn.put_container(Container)
	print("Create Containers: Execution completed")	

def putPicture(pictureToPut,pictureNewName,containerName):
	conn = getSwiftConn()
	with open(pictureToPut, 'rb') as f:
		file_data = f.read()
	conn.put_object(containerName, pictureNewName, file_data)
	print("Put Picture: Execution completed")	

def getPicture(pictureToGet,containerName):
	conn = getSwiftConn()
	picture = conn.get_object(containerName, pictureToGet)
	return picture

def createVM(name,network_id):
	nova_client = getNovaClient()
	## Initiate VM parameters 
	image = nova_client.images.find(name="ubuntu1404")
	flavor = nova_client.flavors.find(name="m1.small")
	net = nova_client.networks.find(id=network_id)
	nics = [{'net-id': net.id}]
	## Create VM
	ServerName = "Server"+name
	nova_client.servers.create(name=ServerName, image=image,flavor=flavor, key_name="key_mac", nics=nics)
	print("VM ",ServerName," created , waiting for running state")
	instance = nova_client.servers.find(name=ServerName)
	while instance.to_dict()['OS-EXT-STS:power_state'] != 1:
		time.sleep(1)
		instance = nova_client.servers.find(name=ServerName)
	
	#appendHostLocal(instance.to_dict()['addresses']['private_network_project_1'][0]['addr'],ServerName)
	DNS[instance.to_dict()['addresses']['private_network_project_F'][0]['addr']] = ServerName
	return instance,ServerName

def link_VM_FloatingIP(network_id,ServerName):
	nova_client = getNovaClient()
	##Ask for a floating IP
	floating_ip = nova_client.floating_ips.create(nova_client.floating_ip_pools.list()[0].name)
	#link with an existing ip ( already created)
	#floating_ip = nova_client.floating_ips.find(id=network_id)
	instance = nova_client.servers.find(name=ServerName)
	time.sleep(10)
	instance.add_floating_ip(floating_ip)

def createVM_Master(network_id):
	instance , ServerName = createVM("Master",network_id)
	link_VM_FloatingIP(network_id,ServerName)
	appendHostLocal(instance.to_dict()['addresses']['private_network_project_F'][0]['addr'],ServerName)

def createVM_I():
	instance , ServerName =createVM("I",network_id)
	install_mysql(ServerName)

def createVM_S():
	instance , ServerName =createVM("S",network_id)
	install_mysql(ServerName)

def createVM_B():
	instance , ServerName = createVM("B",network_id)

def createVM_P():
	instance , ServerName = createVM("P",network_id)

def createVM_W():
	instance , ServerName = createVM("W",network_id)
	   
## Main 
print("Creation of network")
network_id, subnet_id = createNetwork('private_network_project_F')
print("Creation of router")
router_id = createRouter('router_project',subnet_id)
print("Creation of port")
createPort('port_project',router_id, network_id)
#network_id = "9e6b3047-e5b8-4be8-ad64-b5b6155328cf"

print("Creation of VMs")
print("Creation of Master")
createVM_Master(network_id)
print("Creation of I")
createVM_I()
print("Creation of S")
createVM_S()
print("Creation of B")
createVM_B()
print("Creation of P")
createVM_P()
print("Creation of W")
createVM_W()

print("Set-up of DNS")
#set_dns()

print("Creation of Containers")
#createSwiftContainers(['containerPrices'])


# set a list of sending commands
#print("Sending the Master")
