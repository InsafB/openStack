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
        client_stdin, client_stdout, client_stderr = client.exec_command(cmd);
        exit_status = client_stdout.channel.recv_exit_status()
        print "exit status for commande '",cmd," is : ",exit_status


## Nova Client
credentials = get_nova_credentials_v2()
#First way (don't know why it doesn't work) 
#nova_client = Client(**credentials)
#Second way
nova_client = os_client_config.make_client('compute',**credentials)


## Initiate Vm parameters 
image = nova_client.images.find(name="ubuntu1404")
flavor = nova_client.flavors.find(name="m1.small")
net = nova_client.networks.find(id="473a05e9-f592-4c73-923f-b1127a007043")
nics = [{'net-id': net.id}]
## Create Vm
ServerName = "Server"+str(1)
instance = nova_client.servers.create(name=ServerName, image=image,flavor=flavor, key_name="key_mac", nics=nics)

##Ask for a floating IP
#floating_ip = nova_client.floating_ips.create(nova_client.floating_ip_pools.list()[0].name)

#link with an existing ip ( already created)
floating_ip = nova_client.floating_ips.find(id='c62cc884-f9ca-4748-be68-347afcf6ab87')
instance = nova_client.servers.find(name=ServerName)
instance.add_floating_ip(floating_ip)




## Install Mysql Example 
import paramiko
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.11.50.71')
#trove create mysql_instance_1 2 --size 5 --databases myDB --users othmane:othmane --datastore_version mysql-5.5 --datastore mysql
cmds=["sudo apt-get update","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password othmane'","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password othmane'","sudo apt-get -y install mysql-server"]
for cmd in cmds:
    client_stdin, client_stdout, client_stderr = client.exec_command(cmd);
    exit_status = client_stdout.channel.recv_exit_status()
    print("exit status for commande '",cmd," is : ",exit_status)

