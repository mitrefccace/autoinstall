# Automated Installation Script
This is the README.md file for the automated installation script for ACE Direct. The installation script 
clones or pulls the necessary repositories from GitHub, and installs required packages and their dependencies,
including software dependencies such as Node.js, MongoDB, Git, and pm2.
After all repositories are installed, the script prompts the user for editing the global configuration file.
Finally, it starts the installed and configured servers. The script includes an option to use HashConfig, an 
automated configuration and encoding tool, during the configuration process. The following diagram visually 
describes the installation script.

![Flowchart describing the installation script.](autoinstalldiagram.png)

## Code Structure
The script installer.py allows the user to install any of the following repositories in any order:
ACE Direct, ACR-CDR, Management Portal, Aserver, Userver, Fendesk, and Virtual Agent.

## Prerequisites
The installation scripts require the following:

* The machine operating system must be CentOS (version 7 or newer) or RedHat Linux.

* Python 2.7 is installed on the user machine.


## Instructions for Use
1. Open the parent directory where the autoinstall repository will be placed; the home directory is suggested.

2. Clone this repository. 
 
3. Copy installer.py from the autoinstall directory to the home directory, and enter the home directory.

4. Run 
```sh
python ./installer.py -s <Git source> -b <Git branch>
```
The Git source to be used is "ssh://github.com/mitrefccace", and the recommended Git branch is "v3.0", although the user can choose any
available branch or tag from GitHub. While the script is running, follow any user prompts. Select any subset of the repositories to 
install. To install all repositories, select the quick install option.

5. For a one-click install, save the properly-configured, decoded configuration file in the /home/centos directory with the
naming convention "config_acedirect.json_TEMPLATE". Then choose the quick install option.

6. When installation is complete and the script has finished running, a PM2 status window will be displayed with the name of each server and its status. The servers should all have a status "online". To verify successful installation, run the command
```sh
pm2 status
```
and the servers should all have status "online" with 0 restarts. If the server crashes after multiple automatic restarts, PM2 will stop the server and return a status of "errored". In this case, check the configuration file for possible errors, and then try restarting the server with the command
```sh
pm2 restart <Name>
```