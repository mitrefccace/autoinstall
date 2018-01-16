# Automated Installation Script
This is the README.md file for the automated installation script for ACE Direct. The installation script 
clones or pulls the necessary repositories from GitHub. Then for each repository the script installs packages 
and their dependencies, sets up the configuration files, and finally starts their associated servers. The script 
includes an option to use HashConfig, an automated configuration and encoding tool, during the configuration 
process. The following diagram visually describes the installation script.

![Flowchart describing the installation script.](autoinstalldiagram.png)

## Code Structure
The script installer.py allows the user to install any of the following repositories in any order:
ACE Direct, ACR-CDR, Management Portal, Aserver, Userver, Fendesk, and Virtual Agent.

## Prerequisites
The installation scripts require the following:

* The machine operating system must be CentOS (version 7 or newer) or RedHat Linux.

* Node.js is installed on the user machine.

* Python 2.7 is installed on the user machine.

* MySQL is installed on the user machine, and the user has access to the username and password.


## Instructions for Use
1. Run
```
sudo bash  -c  'python <( curl  https://raw.githubusercontent.com/mitrefccace/autoinstall/master/installer.py)'
```
in the terminal. Follow the instructions; select any subset of the repositories to install. To install all repositories,
select the quick install option.

