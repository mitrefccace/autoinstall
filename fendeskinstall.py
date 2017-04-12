#this script clones from github, installs, and configures aserver and userver.

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
            subprocess.call('git pull', shell=True, cwd = self.name)
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

#create instances of Repository
hashconfig = Repository('hashconfig','https://github.com/mitrefccace/hashconfig.git','hconfig.js')
fendesk = Repository('fendesk','ssh://git@git.codev.mitre.org/acrdemo/fendesk.git','app.js')

#set up hashconfig
hashconfig.pull()
hashconfig.install()

#install and configure fendesk
fendesk.pull()
fendesk.install()
subprocess.call(['npm','install','apidoc','-g'], cwd = fendesk.name)
subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = fendesk.name)
fendesk.configure() #comment this line out if you already have a config.json that is properly configured and encoded

#start fendesk
subprocess.call(['node', 'app.js'], cwd = fendesk.name)