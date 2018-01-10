# Automated Installation Script
This is the README.md file for the automated installation script for ACE Direct. The installation script 
clones or pulls the necessary repositories from GitHub, and installs required packages and their dependencies.
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

* Node.js is installed on the user machine.

* Python 2.7 is installed on the user machine.

* MySQL is installed on the user machine, and the user has access to the username and password.


## Instructions for Use
1. Open the parent directory where the autoinstall repository will be placed; the home directory is suggested.

2. Clone this repository. 
 
3. Copy installer.py from the autoinstall directory to the home directory, and enter the home directory.

4. Run 
```sh
python ./installer.py -s <Git source> -b <Git branch>
```
The Git source to be used is "ssh://github.com/mitrefccace", and the recommended Git branch is "v2.0", although the user can choose any
available branch or tag from GitHub. While the script is running, follow any user prompts. Select any subset of the repositories to 
install. To install all repositories, select the quick install option.

5. For a one-click install, save the properly-configured, decoded configuration file in the /home/centos directory with the
naming convention "config_acedirect.json_TEMPLATE". Then choose the quick install option.