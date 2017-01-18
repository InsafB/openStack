# openStack

## Steps to execute the project

1. Download the project.  
2. Get the "sendProject.sh" file.  
3. Execute :   
`cd path_to_project`  
`bash sendProject.sh ip_bastion rsa_priv rsa_pub`  
4. Connect to Bastion :  
`ssh ubuntu@ip_bastion`  
5. Launch the installation scripts :  
`cd ~/openStack-master/`  
`bash install_all.sh openrc_file_name` ("project9-openrc.sh" in this case)    
