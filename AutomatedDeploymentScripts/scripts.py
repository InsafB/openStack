import os_client_config
import os
import paramiko
import credentials
import glanceclient.v2.client as glclient
import keystoneclient.v2_0.client as ksclient
import novaclient.v2.client as nvclient
from novaclient.client import Client
from neutronclient.v2_0 import client
from swiftclient.client import Connection, ClientException
from credentials import get_credentials
from credentials import get_nova_credentials
from credentials import get_nova_credentials_v2
from utils import print_values_server

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

def appendHost(ip,ServerName):
    command = "echo '"+ip+"    "+ServerName+"' >> /etc/hosts"
    commands = [command]
    exec_commands(commands,ServerName)

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

def createVM(name,network_id):
    novaclient = getNovaClient()
    ## Initiate VM parameters 
    image = nova_client.images.find(name="ubuntu1404")
    flavor = nova_client.flavors.find(name="m1.small")
    net = nova_client.networks.find(id=network_id)
    nics = [{'net-id': net.id}]
    ## Create VM
    ServerName = "Server"+name
    instance = nova_client.servers.create(name=ServerName, image=image,flavor=flavor, key_name="key_mac", nics=nics)
    appendHost(instance.to_dict()['addresses']['private'][0]['addr'],ServerName)
    return instance,ServerName

def link_VM_FloatingIP(network_id,ServerName):
    nova_client = getNovaClient()
    ##Ask for a floating IP
    #floating_ip = nova_client.floating_ips.create(nova_client.floating_ip_pools.list()[0].name)
    #link with an existing ip ( already created)
    floating_ip = nova_client.floating_ips.find(id=network_id)
    instance = nova_client.servers.find(name=ServerName)
    instance.add_floating_ip(floating_ip)

def createVM_Master(network_id):
    instance , ServerName = createVM("Master")
    link_VM_FloatingIP(network_id,ServerName)

def createVM_I():
    instance , ServerName =createVM("I")
    install_mysql(ServerName)

def createVM_S():
    instance , ServerName =createVM("S")
    install_mysql(ServerName)

def createVM_B():
    instance , ServerName = createVM("B")
    link_VM_Swift(ServerName)

def createVM_P():
    instance , ServerName = createVM("P")
    link_VM_Swift(ServerName)

def createVM_W():
    instance , ServerName = createVM("W")
    
def createNetwork():
    credentials = get_credentials()
    neutron = client.Client(**credentials)
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

## Main 
router_id = createRouter()
network_id = createNetwork()

createVM_Master(network_id)
createVM_I()
createVM_S()
createVM_B()
createVM_P()
createVM_W()

createSwift_store()
