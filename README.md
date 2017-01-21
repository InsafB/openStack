# openStack

## Steps to execute the project

1. Download the project.  
2. Get the "sendProject.sh" file.  
3. Execute :   
`cd path_to_project`  
`bash sendProject.sh ip_bastion rsa_priv rsa_pub` (rsa links)  
4. Connect to Bastion :  
`ssh ubuntu@ip_bastion`  
5. Launch the installation scripts :  
`cd ~/openStack-master/`  
`bash install_all.sh openrc_file_name dns_address` ("project9-openrc.sh" and "10.11.50.1" in this case)   
