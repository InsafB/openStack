import os
import paramiko
import time
import socket
import sys
from threadingFunc import FuncThread

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

def async_exec_commands(commands,server):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(server)    
	for cmd in commands:
		print "executing command : ",cmd
		client_stdin, client_stdout, client_stderr = client.exec_command(cmd);
		
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
	commands = ["sudo -s", "source "+sys.argv[1], "python3 " + fileName]
	async_exec_commands(commands,dest)	
	
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
	
#install_mysql("ServerI")
tSQL1 = FuncThread(install_mysql,"ServerI")
tSQL1.start()
#install_mysql("ServerS")
tSQL2 = FuncThread(install_mysql,"ServerS")
tSQL2.start()

tSQL1.join()
tSQL2.join()

dependencies = "scripts_dependencies.sh"
path_services = "~/openStack-master/Services/"
path_scripts = "~/openStack-master/AutomatedDeploymentScripts/"
path_dependencies = "~/openStack-master/AutomatedDeploymentScripts/" + dependencies
path_dest = "~/"

ObjectsAndServers = [["b", "ServerB"],["i", "ServerI"],["s", "ServerS"],["w", "ServerW"],["p", "ServerP"]]
for OaS in ObjectsAndServers:	
	sendObject(path_services + OaS[0], OaS[1], path_dest + OaS[0])
	sendObject("~/openStack-master/"+sys.argv[1], OaS[1], path_dest)
	sendObject(path_scripts+"credentials.py", OaS[1], path_dest + OaS[0])

t1 = FuncThread(sendAndExecuteDependencies,path_dependencies, "ServerB", path_dest)
t1.start()
t2 = FuncThread(sendAndExecuteDependencies,path_dependencies, "ServerI", path_dest)
t2.start()
t3 = FuncThread(sendAndExecuteDependencies,path_dependencies, "ServerS", path_dest)
t3.start()
t4 = FuncThread(sendAndExecuteDependencies,path_dependencies, "ServerW", path_dest)
t4.start()
t5 = FuncThread(sendAndExecuteDependencies,path_dependencies, "ServerP", path_dest)
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

Servers = ["ServerB", "ServerI", "ServerS", "ServerW", "ServerP"]
for Server1 in Servers:
	for Server2 in Servers:
		sendIPs(Server2,Server1)

ServicesAndServers = [["b/b.py", "ServerB"],["i/i.py", "ServerI"],["s/s.py", "ServerS"],["w/w.py", "ServerW"],["p/p.py", "ServerP"]]
for SaS in ServicesAndServers:
	executeService(path_dest + SaS[0], SaS[1])
	
commandsM = ["sudo -s", "source ~/openStack-master/"+sys.argv[1], "python3 ~/openStack-master/TemplateServerM/serverM.py"]
async_exec_commands(commandsM,"ServerM")
