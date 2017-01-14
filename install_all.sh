#!/bin/bash

bash AutomatedDeploymentScripts/initial_dependencies.sh

source project9-openrc.sh

python AutomatedDeploymentScripts/scripts_installation.py
