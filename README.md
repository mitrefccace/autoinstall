# Automated Installation Scripts
This is the README.md file for the automated installation scripts for ACE Direct. The installation scripts 
clone or pull the necessary repositories from GitHub. Then for each repository the scripts install packages 
and their dependencies, set up the configuration files, and finally start their associated servers. The scripts 
include an option to use HashConfig, an automated configuration and encoding tool, during the configuration 
process. The following diagram visually describes the installation script.
<p align="left">
	<img src="autoinstalldiagram.png" width="700" alt="Flowchart describing the installation scripts."/>
</p>

## Code Structure
The adinstall directory contains the adinstall.py installation script for the acedirect, acr-cdr, 
and managementportal repositories. It also contains a process.json file that specifies the servers 
corresponding to each repository, to be started after installation and configuration.

The auserverinstall directory contains the auserverinstall.py installation script for the aserver and 
userver repositories. It also contains a process.json file that specifies the servers corresponding 
to each repository, to be started after installation and configuration.

## Prerequisites
The installation scripts require the following:

* The machine operating system must be CentOS (version 7 or newer) or RedHat Linux.

* Node.js is installed on the user machine.

* Python 2.7 is installed on the user machine.


## Instructions for Use
1. Open the parent directory where the autoinstall repository will be placed.

2. Clone this repository and open the autoinstall folder by running "cd 
autoinstall" in the command prompt.  

3. To run the adinstall.py script, open the adinstall directory and then run the script using the 
command "python ./adinstall.py".

4. To run the auserverinstall.py script, open the auserverinstall directory and then run the script 
using the command "python ./auserverinstall.py".