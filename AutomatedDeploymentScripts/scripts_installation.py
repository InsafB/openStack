import os_client_config
import os
import paramiko
import credentials
from neutronclient.v2_0 import client
from swiftclient.client import Connection, ClientException
from credentials import *
import time
import sys
from threadingFunc import FuncThread

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
		body_create_subnet = {'subnets': [{'name':'private_subnet_project','cidr': '10.0.2.0/24','ip_version': 4,'gateway_ip': '10.0.2.254', 'dns_nameservers': [sys.argv[2]], 'network_id': network_id}]}
		subnet = neutron.create_subnet(body=body_create_subnet)
		print('SubNetwork %s has been successfuly created' % subnet)
	finally:
		print("Create Network: Execution completed")
	return network_id, subnet['subnets'][0]['id']

def createRouter(router_name):
	credentials = get_credentials()
	neutron = client.Client(**credentials)
	neutron.format = 'json'
	external_network=neutron.list_networks(name='external-network')
	print("external network-id",external_network['networks'][0]['id'])
	request = {'router': {'name': router_name,'admin_state_up': True,'external_gateway_info':{"network_id":external_network['networks'][0]['id']}}}
	 #'external_gateway_info':{"network_id":external_network['networks'][0]['id']}
	router = neutron.create_router(request)
	router_id = router['router']['id']
	print("Create Router: Execution Completed")
	return router_id

def createPort(router_id,subnet_id):
	print("Adding the interface\n")
	os.system('neutron router-interface-add '+router_id+' '+subnet_id)
	print("Adding interface: Execution Completed")
	
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
	command = "echo '"+ip+"    "+ServerName+"' | sudo tee -a /etc/hosts"
	commands = [command]
	exec_commands(commands,dest)

def appendHostLocal(ip,ServerName):
	command = "echo '"+ip+"    "+ServerName+"' | sudo tee -a /etc/hosts"
	os.system(command)

def set_dns():
	dests = list(DNS.keys())
	for keydns, value in DNS.items():
		appendHost(keydns,value,"ServerMaster")

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
	
	DNS[instance.to_dict()['addresses']['private_network'][0]['addr']] = ServerName
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
	nova_client = getNovaClient()
	instance = nova_client.servers.find(name=ServerName)
	while len(instance.to_dict()['addresses']['private_network']) < 2:
		time.sleep(1)
		instance = nova_client.servers.find(name=ServerName)	
	appendHostLocal(instance.to_dict()['addresses']['private_network'][1]['addr'],ServerName)
	print("Creation of ",ServerName," is done\n")

def createVM_I(network_id):
	instance , ServerName =createVM("I",network_id)
	print("Creation of ",ServerName," is done\n")
	
def createVM_S(network_id):
	instance , ServerName =createVM("S",network_id)
	print("Creation of ",ServerName," is done\n")
	
def createVM_B(network_id):
	instance , ServerName = createVM("B",network_id)
	print("Creation of ",ServerName," is done\n")

def createVM_P(network_id):
	instance , ServerName = createVM("P",network_id)
	print("Creation of ",ServerName," is done\n")

def createVM_W(network_id):
	instance , ServerName = createVM("W",network_id)
	print("Creation of ",ServerName," is done\n")

def sendObject(path, dest, path_dest):
	command = "scp -r " + path + " ubuntu@"  + dest + ":" + path_dest
	os.system(command)
	   
## Main 
print("Creation of network")
network_id, subnet_id = createNetwork('private_network')
print("Creation of router")
router_id = createRouter('router_project')
print("Creation of port")
createPort(router_id,subnet_id)
#network_id = "02538e2f-52d4-4a0d-8252-0c09edb95a35"

print("Creation of VMs")
print("Creation of Master")
#createVM_Master(network_id)
t1 = FuncThread(createVM_Master,network_id)
t1.start()
print("Creation of I")
#createVM_I(network_id)
t2 = FuncThread(createVM_I,network_id)
t2.start()
print("Creation of S")
#createVM_S(network_id)
t3 = FuncThread(createVM_S,network_id)
t3.start()
print("Creation of B")
#createVM_B(network_id)
t4 = FuncThread(createVM_B,network_id)
t4.start()
print("Creation of P")
#createVM_P(network_id)
t5 = FuncThread(createVM_P,network_id)
t5.start()
print("Creation of W")
#createVM_W(network_id)
t6 = FuncThread(createVM_W,network_id)
t6.start()


t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()

time.sleep(2)
print("Set-up of DNS")

while True:
	try:
		set_dns()
		break
	except:    
		time.sleep(1)


print("Creation of Containers")
createSwiftContainers(['ContainerPrices'])

# set a list of sending commands
print("Sending the Master")

# Sending the project and the needed files to the Master
path = '~/openStack-master/'
path_dest = '~/'
path_ssh = "~/.ssh/"

sendObject(path, "ServerMaster", path_dest)
sendObject(path_ssh+"id_rsa", "ServerMaster", path_ssh)
sendObject(path_ssh+"id_rsa.pub", "ServerMaster", path_ssh)
sendObject(path+"config", "ServerMaster", path_ssh)
sendObject(path+sys.argv[1], "ServerMaster", path_dest)

print("Execution of dependencies and scripts_master on the ServerMaster")
commands = ["bash ~/openStack-master/AutomatedDeploymentScripts/scripts_dependencies.sh ServerMaster "+sys.argv[1],"python ~/openStack-master/AutomatedDeploymentScripts/scripts_master.py "+sys.argv[1]]
exec_commands(commands,"ServerMaster")
