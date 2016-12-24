import os_client_config
import glanceclient.v2.client as glclient
import keystoneclient.v2_0.client as ksclient
from novaclient.client import Client
import os
import paramiko


def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_PROJECT_ID']
    d['project_name']= os.environ['OS_PROJECT_NAME']
    d['domain_name']= os.environ['OS_USER_DOMAIN_NAME']
    return d

def print_values_ip(ip_list):
    ip_dict_lisl = []
    for ip in ip_list:
        print("-"*35)
        print("fixed_ip : %s" % ip.fixed_ip)
        print("id : %s" % ip.id)
        print("instance_id : %s" % ip.instance_id)
        print("ip : %s" % ip.ip)
        print("pool : %s" % ip.pool)

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

def createVM(letter,network_id):
    novaclient = getNovaClient()
    ## Initiate Vm parameters 
    image = nova_client.images.find(name="ubuntu1404")
    flavor = nova_client.flavors.find(name="m1.small")
    net = nova_client.networks.find(id=network_id)
    nics = [{'net-id': net.id}]
    ## Create Vm
    ServerName = "Server"+letter
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
    nstance , ServerName = createVM("Master")
    link_VM_FloatingIP(network_id,ServerName)

def createVM_I():
    instance , ServerName =createVM("I")
    install_mysql(ServerName)

def createVM_S():
    instance , ServerName =createVM("S")
    install_mysql(ServerName)

def createVM_B():
    nstance , ServerName = createVM("B")
    link_VM_Swift(ServerName)

def createVM_P():
    nstance , ServerName = createVM("P")
    link_VM_Swift(ServerName)

def createVM_W():
    nstance , ServerName = createVM("W")
   


## Main
router_id = createRouter()
network_id = createNetwork()

createVM_Master(network_id)
createVM_I()
createVM_S()
createVM_B()
createVM_P()
createVM_W()
