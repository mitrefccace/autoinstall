# Automated Installation Script
This is the README.md file for the automated installation script for ACE Direct. The installation script installer.py 
clones or pulls the necessary repositories from GitHub, and installs required packages and their dependencies,
including software dependencies such as Node.js, Nginx, Redis, MongoDB, Git, and pm2. The script also disables SE Linux, which is required to do in order to run ACE Direct.
After all repositories are installed, the script prompts the user for editing the global configuration file.
Finally, it starts the installed and configured servers. The script includes an option to use HashConfig, an 
automated configuration and encoding tool, during the configuration process. The following diagram visually 
describes the installation script.

![Flowchart describing the installation script.](autoinstalldiagram.png)

This repository also contains an optional helper script called nginx_configure.py to be used after running installer.py. In installer.py, the user has the option to edit the ACE Direct configuration file (typically dat/config.json), and after making edits the Nginx configuration file is automatically updated based on the ACE Direct configuration values. If the user wishes to manually make additional changes to dat/config.json after running installer.py, then they can run nginx_configure.py to update the Nginx configuration based on the latest values in dat/config.json.

If Nginx is installed on a different server than the Node server, then nginx_configure.py can be used on the Nginx server. This requires copying the 'dat' configuration directory from the Node server to the Nginx server. It also requires manually cloning the Nginx repository and installing Nginx.

## Code Structure
The script installer.py allows the user to install any of the following repositories in any order:
ACE Direct, ACR-CDR, Management Portal, Aserver, Userver, Fendesk, and Virtual Agent.

The script nginx_configure.py is an optional helper script to configure nginx if any changes were made to the ACE Direct configuration after running installer.py. 

## Prerequisites
The installation scripts require the following:

* The machine operating system must be CentOS (version 7 or newer), RedHat, Fedora, or Amazon Linux.

* Python 2.7 is installed on the user machine.


## Instructions for Use of installer.py
1. Open the parent directory where the autoinstall repository will be placed; the home directory is suggested.

2. Clone this repository as yourself but not centos
```sh
For example:
[cjliu@vasip10 ~]$ git clone ssh://git@git.codev.mitre.org/acrdemo/autoinstall.git
```
3. Copy installer.py from the autoinstall directory to the home directory, and enter the home directory.

4. Run the python installer.py script as centos 
```sh
python ./installer.py -s <Git source> -b <Git branch> -u <ACE Direct user>

For examples:
[centos@vademo ~]$ python ./installer.py -s 'ssh://github.com/mitrefccace' -b 'develop' -u '/home/centos'
or
[centos@vademo ~]$ python ./installer.py -s 'ssh://git@git.codev.mitre.org/acrdemo' -b 'develop' -u '/home/centos'
```
The Git source to be used is 'ssh://github.com/mitrefccace', and the latest version should be used for the Git branch, such as 'develop'. The ACE Direct user is the home directory where ACE Direct will be installed, such as '/home/centos'.
While the script is running, follow any user prompts. Select any subset of the repositories to 
install. To install all repositories, select the quick install option.

5. (Optional) For a one-click install, save the properly-configured, decoded configuration file in the /home/centos directory with the
naming convention "config_acedirect.json_TEMPLATE". Then choose the quick install option.

6. (Optional) To bypass cloning or pulling from Git, the optional command line argument "--ignore-git True" can be used. The Git source "-s" and branch "-b" need not be used in this case. In order for the script to run successfully with this option, the user must manually download all the needed files and directories to the given environment.

6. When installation is complete and the script has finished running, a PM2 status window will be displayed with the name of each server and its status. The servers should all have a status "online". To verify successful installation, run the command
```sh
pm2 status
```
and the servers should all have status "online" with 0 restarts. If the server crashes after multiple automatic restarts, PM2 will stop the server and return a status of "errored". In this case, check the configuration file for possible errors, and then try restarting the server with the command
```sh
pm2 restart <Name>
```

## Optional Instructions for Use of nginx_configure.py
0. Make any desired changes to the ACE Direct configuration file. This file is typically located at ~/dat/config.json. If Nginx has been installed on a different server than the Node server, then manually copy the dat directory to the home directory on the Nginx server.

1. Copy nginx_configure.py from the autoinstall directory to the home directory, and enter the home directory.

2. Run the python nginx_configure.py script with the following command: 
```sh
python ./nginx_configure.py
```
