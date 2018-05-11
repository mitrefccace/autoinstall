# Automated Installation Script
This is the README.md file for the automated installation script for ACE Direct.
 The installation script installer.py clones or pulls the necessary repositories
 from GitHub, and installs required packages and their dependencies, including s
 oftware dependencies such as Node.js, Nginx, Redis, MongoDB, Git, and pm2. The 
 script also disables SE Linux, which is required to do in order to run ACE Dire
 ct.
 
After all repositories are installed, the script prompts the user for editing th
e global configuration file. Finally, it starts the installed and configured ser
vers. The script includes an option to use HashConfig, an automated configuratio
n and encoding tool, during the configuration process. The following diagram vis
ually describes the installation script.

![Flowchart describing the installation script.](autoinstalldiagram.png)

This repository also contains an optional helper script called nginx_configure.p
y to be used after running installer.py. In installer.py, the user has the optio
n to edit the ACE Direct configuration file (typically dat/config.json), and aft
er making edits the Nginx configuration file is automatically updated based on t
he ACE Direct configuration values. If the user wishes to manually make addition
al changes to dat/config.json after running installer.py, then they can run ngin
x_configure.py to update the Nginx configuration based on the latest values in d
at/config.json.

If Nginx is installed on a different server than the Node server, then nginx_con
figure.py can be used on the Nginx server. This requires copying the 'dat' confi
guration directory from the Node server to the Nginx server. It also requires ma
nually cloning the Nginx repository and installing Nginx.

## Code Structure
The script installer.py allows the user to install any of the following reposito
ries in any order:
ACE Direct, ACR-CDR, Management Portal, Aserver, Userver, Fendesk, and Virtual A
gent.

The script nginx_configure.py is an optional helper script to configure nginx if
 any changes were made to the ACE Direct configuration after running installer.p
y. 

## Prerequisites
The installation scripts require the following:

* The machine operating system must be CentOS (version 7 or newer), RedHat, Fedo
ra, or Amazon Linux.

* Python 2.7 is installed on the user machine.


## Instructions for Use of installer.py
1. Open the parent directory where the autoinstall repository will be placed; th
e home directory is suggested.

2. Clone this repository as yourself but not centos
```sh
For example:
[user@aceserver ~]$ git clone ssh://github.com/mitrefccace/autoinstall.git
```
3. Copy installer.py from the autoinstall directory to the home directory, and e
nter the home directory.

4. Run the python installer.py script as centos 
```sh
python ./installer.py -s <Git source> -b <Git branch> -u <ACE Direct user>

For example:
[centos@aceserver ~]$ python ./installer.py -s 'ssh://github.com/mitrefccace' -b
 'develop' -u '/home/centos'
```
The Git source to be used is 'ssh://github.com/mitrefccace', and the latest vers
ion should be used for the Git branch, such as 'develop'. The ACE Direct user is
 the home directory where ACE Direct will be installed, such as '/home/centos'.
While the script is running, follow any user prompts. Select any subset of the r
epositories to install. To install all repositories, select the quick install op
tion.

5. (Optional) For a one-click install, save the properly-configured, decoded con
figuration file in the /home/centos directory with the naming convention "config
_acedirect.json_TEMPLATE". Then choose the quick install option.

6. (Optional) To bypass cloning or pulling from Git, the optional command line a
rgument "--ignore-git True" can be used. The Git source "-s" and branch "-b" nee
d not be used in this case. In order for the script to run successfully with thi
s option, the user must manually download all the needed files and directories t
o the given environment.

6. When installation is complete and the script has finished running, a PM2 stat
us window will be displayed with the name of each server and its status. The ser
vers should all have a status "online". To verify successful installation, run t
he command
```sh
pm2 status
```
and the servers should all have status "online" with 0 restarts. If the server c
rashes after multiple automatic restarts, PM2 will stop the server and return a 
status of "errored". In this case, check the configuration file for possible err
ors, and then try restarting the server with the command
```sh
pm2 restart <Name>
```

## Optional Instructions for Use of nginx_configure.py
0. Make any desired changes to the ACE Direct configuration file. This file is t
ypically located at ~/dat/config.json. If Nginx has been installed on a differen
t server than the Node server, then manually copy the dat directory to the home 
directory on the Nginx server.

1. Copy nginx_configure.py from the autoinstall directory to the home directory,
 and enter the home directory.

2. Run the python nginx_configure.py script with the following command: 
```sh
python ./nginx_configure.py
```
