import os
import paramiko
import time
import socket

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
		
def sendObject(path, dest, path_dest):
	command = "scp -r " + path + " ubuntu@"  + dest + ":" + path_dest
	os.system(command)

def sendAndExecuteDependencies(path_dependencies, dest, path_dest):
	command1 = "scp -r " + path_dependencies + " ubuntu@" + dest + ":" + path_dest
	command2 = "bash " + dependencies + " " + dest
	os.system(command1)
	commands = [command2]
	exec_commands(commands,dest)

def executeService(fileName, dest):
	command = "python " + fileName
	commands = [command]
	exec_commands(commands,dest)	
	
def install_mysql(server):
	commands=["sudo apt-get update","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password othmane'","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password othmane'","sudo apt-get -y install mysql-server"]
	exec_commands(commands,server)

def appendHost(ip,ServerName,dest):
	command = "echo '"+ip+"    "+ServerName+"' | sudo tee -a /etc/hosts"
	commands = [command]
	exec_commands(commands,dest)
	
def sendIPs(ServerName,dest):
	ip = socket.gethostbyname(ServerName)
	appendHost(ip,ServerName,dest)
	
install_mysql("ServerI")
install_mysql("ServerS")

dependencies = "scripts_dependencies.sh"
path_services = "~/openStack-master/Services/"
path_scripts = "~/openStack-master/AutomatedDeploymentScripts/"
path_dependencies = "~/openStack-master/AutomatedDeploymentScripts/" + dependencies
path_dest = "~/"

ObjectsAndServers = [["b", "ServerB"],["i", "ServerI"],["s", "ServerS"],["w", "ServerW"],["p", "ServerP"]]
for OaS in ObjectsAndServers:	
	sendObject(path_services + OaS[0], OaS[1], path_dest + OaS[0])
	sendObject("~/openStack-master/project9-openrc.sh", OaS[1], path_dest + OaS[0])
	sendObject(path_scripts+"credentials.py", OaS[1], path_dest + OaS[0])

Servers = ["ServerB", "ServerI", "ServerS", "ServerW", "ServerP"]
for Server in Servers:
	sendAndExecuteDependencies(path_dependencies, Server, path_dest)
	for ServerName in Servers:
		sendIPs(ServerName,Server)

ServicesAndServers = [["b/b.py", "ServerB"],["i/i.py", "ServerI"],["s/s.py", "ServerS"],["w/w.py", "ServerW"],["p/p.py", "ServerP"]]
for SaS in ServicesAndServers:
	exec_commands(['source project9-openrc.sh'],SaS[1])
	executeService(path_dest + SaS[0], SaS[1])
	
executeService(path_dest + "openStack-master/TemplateServerM/serverM.py", "ServerM")
