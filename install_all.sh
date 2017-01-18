#!/bin/bash

bash AutomatedDeploymentScripts/initial_dependencies.sh

source $1

python AutomatedDeploymentScripts/scripts_installation.py
