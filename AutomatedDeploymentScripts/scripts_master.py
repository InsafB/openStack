import os
import paramiko
import time

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
	commands = [command]
	exec_commands(commands,dest)

def sendAndExecuteDependencies(path_dependencies, dest, path_dest):
	command1 = "scp -r " + path_dependencies + " ubuntu@" + dest + ":" + path_dest
	command2 = "bash " + dependencies
	commands = [command1, command2]
	exec_commands(commands,dest)

def executeService(file, dest):
	command = "python " + file
	commands = [command]
	exec_commands(commands,dest)

path_services = "~/openStack/Services/"
dependencies = "scripts_dependencies.sh"
path_dependencies = "~/openStack/AutomatedDeploymentScripts/" + dependencies
path_dest = "~/"

ObjectsAndServers = [["b", "ServerB"],["i", "ServerI"],["s", "ServerS"],["w", "ServerW"],["p", "ServerP"]]
for OS in ObjectsAndServers:	
	sendObject(path_services + OS[0], OS[1], path_dest + OS[0])

Servers = ["ServerB", "ServerI", "ServerS", "ServerW", "ServerP"]
for Server in Servers:
	sendAndExecuteDependencies(path_dependencies, Server, path_dest)

ServicesAndServers = [["b/b.py", "ServerB"],["i/i.py", "ServerI"],["s/s.py", "ServerS"],["w/w.py", "ServerW"],["p/p.py", "ServerP"]]

For SS in ServicesAndServers:
	executeService(path_dest + SS[0], SS[1])
