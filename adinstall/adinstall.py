#this script clones from github, installs, configures, and runs the servers for
#acedirect, acr-cdr, and managementportal.

import subprocess
import os.path
from time import sleep
import platform

class Repository:

    #constructor
    def __init__(self, name, giturl, server):
        self.name = name
        self.giturl = giturl
        self.server = server
        
    #pull method -- git clone if the repo doesn't exist locally; error message if it does exist locally
    def pull(self):
        out = subprocess.check_output('test -e %s && echo -n True || echo -n False' % self.name, shell=True)
        out_bool = out.lower() in ("true")
        if out_bool:
            print 'Directory already exists. Running "git pull"...'
            subprocess.call('git pull', shell=True, cwd=self.name)
        else:
            subprocess.call('git clone %s' % self.giturl, shell=True)

    #install method -- run npm install
    def install(self):
        subprocess.call(['npm','install'], cwd=self.name)

    #configure method -- use HashConfig
    def configure(self, configfile = 'config.json_TEMPLATE'):
        conf = True
        while conf == True:
            ans = raw_input('Do you want to edit the configuration file for %s? (y/n)' % self.name)
            if ans == 'y':
                print 'Please follow prompts to generate the configuration file...'
                if configfile == 'config.json_TEMPLATE':
                    subprocess.call(['rm', 'config.json_TEMPLATE'], cwd = hashconfig.name)
                    subprocess.call(['cp', self.name + '/config.json_TEMPLATE', 'hashconfig/config.json_TEMPLATE'])
                    subprocess.call(['node','hconfig.js'], cwd= hashconfig.name)
                    subprocess.call(['mv','config_new.json','config.json'], cwd = hashconfig.name)
                    subprocess.call(['cp', 'hashconfig/config.json', self.name + '/config.json'])
                else:
                    filename = os.path.splitext(configfile)[0]
                    subprocess.call(['rm', 'config.json_TEMPLATE'], cwd = hashconfig.name)
                    subprocess.call(['cp', self.name + '/' + configfile, 'hashconfig/config.json_TEMPLATE'])
                    subprocess.call(['node','hconfig.js'],cwd=hashconfig.name)
                    subprocess.call(['cp', 'hashconfig/config_new.json', self.name+'/'+filename+'.json'])
                conf = False
            elif ans == 'n':
                print 'Skipping configuration editing process...'
                conf = False
            else:
                print 'Invalid input. Must enter "y" or "n".'


#check operating system
if platform.system() != 'Linux':
    print 'Installation script can only be run on Linux. Terminating...'
    quit()

#check distribution    
dist = platform.dist()[0]
if dist != 'centos' and dist != 'redhat':
    print 'Installation script can only be run on CentOS or RedHat. Terminating...'
    quit()
            
#create instances of Repository (i.e. the submodules that will be installed)
hashconfig = Repository('hashconfig','https://github.com/mitrefccace/hashconfig.git','hconfig.js')
acedirect = Repository('acedirect','https://github.com/mitrefccace/acedirect.git','adserver.js')
acrcdr = Repository('acr-cdr', 'https://github.com/mitrefccace/acr-cdr.git','app.js')
mgmt = Repository('managementportal','https://github.com/mitrefccace/managementportal.git','server-db.js')

#update software; stop the servers
#subprocess.call(['sudo', 'apt-get','update'])
#subprocess.call(['sudo', 'apt-get','upgrade'])
subprocess.call(['pm2','kill'])

#set up hashconfig
hashconfig.pull()
hashconfig.install()

#clone acedirect repo; perform installation and configuration
acedirect.pull()
subprocess.call(['npm', 'install', '-g', 'bower'])
subprocess.call(['npm','install','pm2','-g'])
subprocess.call(['bower', 'install', '--allow-root'], cwd = acedirect.name)
acedirect.install()
acedirect.configure() #comment this line out if you already have a config.json that is properly configured and encoded

#repeat the process for acr-cdr
acrcdr.pull()
acrcdr.install()
acrcdr.configure() #comment this line out if you already have a config.json that is properly configured and encoded

#repeat the process for managementportal
mgmt.pull()
mgmt.install()
subprocess.call(['bower', 'install', '--allow-root'], cwd = mgmt.name)
mgmt.configure() #comment this line out if you already have a config.json that is properly configured and encoded

#start all servers listed in process.json
subprocess.call(['pm2','start','process.json'])

sleep(1.5)

#print information about URLs to access
print 'Servers started. To access the management portal, open https://hostname:12345/dashboard. To access \
the ACE Direct customer complaint, open https://hostname:12345/complaint.html. To access the ACE Direct \
agent login, open https://hostname:12345/login.html.'                                                                                                                                                                          

#uncomment the following section to automate the launching of URLs
#print 'Servers started, and ready to access webpages. Please answer y/n for each of the following:'
#sleep(2)
#ans1 = raw_input('Do you want to open the CSR Portal? (y/n)')
#ans2 = raw_input('Do you want to open the Customer Portal? (y/n)')
#ans3 = raw_input('Do you want to open the Management Portal? (y/n)')
#print 'Opening selected portals. Edit the hostname and port for access in the browser.'
#sleep(5)
#if ans1 == 'y':
#    subprocess.call(['xdg-open', 'https://hostname:12345/login.html'])
#if ans2 == 'y':
#    subprocess.call(['xdg-open', 'https://hostname:12345/complaint.html'])
#if ans3 == 'y':
#    subprocess.call(['xdg-open', 'https://hostname:12345/dashboard'])

    
#command for testing a relevant URL; e.g. for acedirect
#subprocess.call(['wget', url, '--no-check-certificate'])

