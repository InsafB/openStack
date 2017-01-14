def sendObject(path, dest, path_dest):
	command = "scp -r " + path + " ubuntu@"  + dest + ":" + path_dest
	commands = [command]
	exec_commands(commands,dest)

def sendAndExecuteDependencies(path_dependencies, dest, path_dest):
	command1 = "scp " + path_dependencies + dest + path_dest
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

Objects = ['b', 'i', 's', 'w', 'p']
for Object in Objects:	
	sendObject(path_services + Object, ServerB, path_dest + Object)

Servers = ['ServerB', 'ServerI', 'ServerS', 'ServerW', 'ServerP']
for Server in Servers:
	sendAndExecuteDependencies(path_dependencies, Server, path_dest)

ServicesAndServers = [["b/b.py", ServerB],["i/i.py", ServerI],["s/s.py", ServerS],["w/w.py", ServerW],["p/p.py", ServerP]]

For SS in ServicesAndServers:
	executeService(path_dest + SS[0], SS[1])
