# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:33:17 2017

@author: AJANETT
"""

# Import the modules needed to run the script.
import sys, os
import subprocess
import os.path
from time import sleep
import platform
import json

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
        subprocess.call('git checkout v2.0', shell=True, cwd=self.name)

    #install method -- run npm install
    def install(self):
        subprocess.call(['npm','install'], cwd=self.name)

    #configure method -- use HashConfig
    def configure(self):
        if os.path.isfile('/home/centos/config_' + self.name + '.json_TEMPLATE'):
            subprocess.call(['node','hconfig.js', '-fn', '/home/centos/config_' + self.name + '.json_TEMPLATE'], cwd = hashconfig.name)
            subprocess.call(['mv','config_new.json','config.json'], cwd = hashconfig.name)
            subprocess.call(['cp', 'hashconfig/config.json', self.name + '/config.json'])
        else:
            template = raw_input('Please enter the full path to the configuration template file for ' + self.name +', or press enter to use the default file: ')
            if template == '':
                template = 'config.json_TEMPLATE'
            ans = raw_input('Do you want to edit the configuration file for %s? (y/n)' % self.name)
            if ans == 'y':
                print 'Please follow prompts to generate the configuration file...'
                subprocess.call(['node','hconfig.js', '-n', template], cwd = hashconfig.name)
                subprocess.call(['mv','config_new.json','config.json'], cwd = hashconfig.name)
                subprocess.call(['cp', 'hashconfig/config.json', self.name + '/config.json'])
            elif ans == 'n':
                subprocess.call(['node','hconfig.js', '-fn', template], cwd = hashconfig.name)
                subprocess.call(['mv','config_new.json','config.json'], cwd = hashconfig.name)
                subprocess.call(['cp', 'hashconfig/config.json', self.name + '/config.json'])
            else:
                print 'Invalid input. Must enter "y" or "n".'
 
# Initialize menu options and process.json
menu_actions  = {} 
out = subprocess.check_output('test -e process.json && echo -n True || echo -n False', shell=True)
out_bool = out.lower() in ("true")
if out_bool:
    with open('process.json') as data_file:    
        process = json.load(data_file)
    if 'apps' not in process:
        print 'Warning: existing process.json file improperly formatted.'
else:
    process = {}
    process['apps'] = []
 
 
# =======================
#     MENUS FUNCTIONS
# =======================
 
# Main menu
def main_menu():   
    print "Please choose one of the following options:"
    print "1. Install ACE Direct"
    print "2. Install ACR-CDR"
    print "3. Install Management Portal"
    print "4. Install Aserver"
    print "5. Install Userver"
    print "6. Install Fendesk"
    print "7. Quick install (all servers)"
    print "\n0. Finish installation process"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return
 
# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return
 
# Menu 1
def acedirectinstall():
    acedirect = Repository('acedirect','https://github.com/mitrefccace/acedirect.git','adserver.js')
    print "Installing ACE Direct \n"
    acedirect.pull()
    acedirect.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = acedirect.name)
    acedirect.configure()
    #update process.json: replace existing ACE Direct entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'ACE Direct':
            process['apps'][i]['script'] = './acedirect/adserver.js'
            process['apps'][i]['cwd'] = './acedirect'
            process['apps'][i]['out_file'] = './logs/pm2-adserver.log'
            process['apps'][i]['error_file'] = './logs/pm2-adserver-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'ACE Direct',
            'script': './acedirect/adserver.js',
            'cwd': './acedirect',
            'out_file': './logs/pm2-adserver.log',
            'error_file': './logs/pm2-adserver-error.log'
        })
    print "ACE Direct installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
 
 
# Menu 2
def acrcdrinstall():
    acrcdr = Repository('acr-cdr', 'https://github.com/mitrefccace/acr-cdr.git','app.js')
    print "Installing ACR-CDR \n"
    acrcdr.pull()
    acrcdr.install()
    acrcdr.configure()
    #update process.json: replace existing CDR entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'CDR':
            process['apps'][i]['script'] = './acr-cdr/app.js'
            process['apps'][i]['cwd'] = './acr-cdr'
            process['apps'][i]['out_file'] = './logs/pm2-app.log'
            process['apps'][i]['error_file'] = './logs/pm2-app-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'CDR',
            'script': './acr-cdr/app.js',
            'cwd': './acr-cdr',
            'out_file': './logs/pm2-app.log',
            'error_file': './logs/pm2-app-error.log'
        })
    print "ACR-CDR installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
 
# Menu 3
def mgmtinstall():
    mgmt = Repository('managementportal','https://github.com/mitrefccace/managementportal.git','server-db.js')
    print "Installing Management Portal \n"
    mgmt.pull()
    mgmt.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = mgmt.name)
    mgmt.configure()
    #update process.json: replace existing Management entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Management Dashboard':
            process['apps'][i]['script'] = './managementportal/server-db.js'
            process['apps'][i]['cwd'] = './managementportal'
            process['apps'][i]['out_file'] = './logs/pm2-server-db.log'
            process['apps'][i]['error_file'] = './logs/pm2-server-db-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Management Dashboard',
            'script': './managementportal/server-db.js',
            'cwd': './managementportal',
            'out_file': './logs/pm2-server-db.log',
            'error_file': './logs/pm2-server-db-error.log'
        })
    print "Management portal installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return

# Menu 4
def aserverinstall():
    aserver = Repository('aserver','https://github.com/mitrefccace/aserver.git','app.js')
    print "Installing Aserver \n"
    aserver.pull()
    aserver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = aserver.name)
    aserver.configure()
    #update process.json: replace existing Aserver entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Aserver':
            process['apps'][i]['script'] = './aserver/app.js'
            process['apps'][i]['cwd'] = './aserver'
            process['apps'][i]['out_file'] = './logs/pm2-aserver.log'
            process['apps'][i]['error_file'] = './logs/pm2-aserver-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Aserver',
            'script': './aserver/app.js',
            'cwd': './aserver',
            'out_file': './logs/pm2-aserver.log',
            'error_file': './logs/pm2-aserver-error.log'
        })
    print "Aserver installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
    
# Menu 5
def userverinstall():
    userver = Repository('userver','https://github.com/mitrefccace/userver.git','app.js')
    print "Installing Userver \n"
    userver.pull()
    userver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = userver.name)
    userver.configure()
    #update process.json: replace existing Userver entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Userver':
            process['apps'][i]['script'] = './userver/app.js'
            process['apps'][i]['cwd'] = './userver'
            process['apps'][i]['out_file'] = './logs/pm2-userver.log'
            process['apps'][i]['error_file'] = './logs/pm2-userver-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Userver',
            'script': './userver/app.js',
            'cwd': './userver',
            'out_file': './logs/pm2-userver.log',
            'error_file': './logs/pm2-userver-error.log'
        })
    print "Userver installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return


#     Menu 6 - Fendesk currently not part of github
def fendeskinstall():
    fendesk = Repository('fendesk','https://github.com/mitrefccace/fendesk.git','app.js')
    print "Installing Fendesk \n"
    fendesk.pull()
    fendesk.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = fendesk.name)
    fendesk.configure()
    #update process.json: replace existing Fendesk entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Fendesk':
            process['apps'][i]['script'] = './fendesk/app.js'
            process['apps'][i]['cwd'] = './fendesk'
            process['apps'][i]['out_file'] = './logs/pm2-fendesk.log'
            process['apps'][i]['error_file'] = './logs/pm2-fendesk-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Fendesk',
            'script': './fendesk/app.js',
            'cwd': './fendesk',
            'out_file': './logs/pm2-fendesk.log',
            'error_file': './logs/pm2-fendesk-error.log'
        })
    print "Fendesk installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
 
# Menu 7
def quickinstall():
    #gather all repos
    acedirect = Repository('acedirect','https://github.com/mitrefccace/acedirect.git','adserver.js')
    acrcdr = Repository('acr-cdr', 'https://github.com/mitrefccace/acr-cdr.git','app.js')
    mgmt = Repository('managementportal','https://github.com/mitrefccace/managementportal.git','server-db.js')
    aserver = Repository('aserver','https://github.com/mitrefccace/aserver.git','app.js')
    userver = Repository('userver','https://github.com/mitrefccace/userver.git','app.js')
    fendesk = Repository('fendesk','https://github.com/mitrefccace/fendesk.git','app.js')
    #installation process for ACE Direct
    print "Installing ACE Direct \n"
    acedirect.pull()
    acedirect.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = acedirect.name)
    acedirect.configure()
    #update process.json: replace existing ACE Direct entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'ACE Direct':
            process['apps'][i]['script'] = './acedirect/adserver.js'
            process['apps'][i]['cwd'] = './acedirect'
            process['apps'][i]['out_file'] = './logs/pm2-adserver.log'
            process['apps'][i]['error_file'] = './logs/pm2-adserver-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'ACE Direct',
            'script': './acedirect/adserver.js',
            'cwd': './acedirect',
            'out_file': './logs/pm2-adserver.log',
            'error_file': './logs/pm2-adserver-error.log'
        })
    print "ACE Direct installation complete."
    #installation process for ACR-CDR
    print "Installing ACR-CDR \n"
    acrcdr.pull()
    acrcdr.install()
    acrcdr.configure()
    #update process.json: replace existing CDR entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'CDR':
            process['apps'][i]['script'] = './acr-cdr/app.js'
            process['apps'][i]['cwd'] = './acr-cdr'
            process['apps'][i]['out_file'] = './logs/pm2-app.log'
            process['apps'][i]['error_file'] = './logs/pm2-app-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'CDR',
            'script': './acr-cdr/app.js',
            'cwd': './acr-cdr',
            'out_file': './logs/pm2-app.log',
            'error_file': './logs/pm2-app-error.log'
        })
    print "ACR-CDR installation complete."
    #installation process for Management Portal
    print "Installing Management Portal \n"
    mgmt.pull()
    mgmt.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = mgmt.name)
    mgmt.configure()
    #update process.json: replace existing Management entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Management Dashboard':
            process['apps'][i]['script'] = './managementportal/server-db.js'
            process['apps'][i]['cwd'] = './managementportal'
            process['apps'][i]['out_file'] = './logs/pm2-server-db.log'
            process['apps'][i]['error_file'] = './logs/pm2-server-db-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Management Dashboard',
            'script': './managementportal/server-db.js',
            'cwd': './managementportal',
            'out_file': './logs/pm2-server-db.log',
            'error_file': './logs/pm2-server-db-error.log'
        })
    print "Management portal installation complete."
    #installation process for Aserver
    print "Installing Aserver \n"
    aserver.pull()
    aserver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = aserver.name)
    aserver.configure()
    #update process.json: replace existing Aserver entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Aserver':
            process['apps'][i]['script'] = './aserver/app.js'
            process['apps'][i]['cwd'] = './aserver'
            process['apps'][i]['out_file'] = './logs/pm2-aserver.log'
            process['apps'][i]['error_file'] = './logs/pm2-aserver-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Aserver',
            'script': './aserver/app.js',
            'cwd': './aserver',
            'out_file': './logs/pm2-aserver.log',
            'error_file': './logs/pm2-aserver-error.log'
        })
    print "Aserver installation complete."
    #installation process for Userver
    print "Installing Userver \n"
    userver.pull()
    userver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = userver.name)
    userver.configure()
    #update process.json: replace existing Userver entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Userver':
            process['apps'][i]['script'] = './userver/app.js'
            process['apps'][i]['cwd'] = './userver'
            process['apps'][i]['out_file'] = './logs/pm2-userver.log'
            process['apps'][i]['error_file'] = './logs/pm2-userver-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Userver',
            'script': './userver/app.js',
            'cwd': './userver',
            'out_file': './logs/pm2-userver.log',
            'error_file': './logs/pm2-userver-error.log'
        })
    print "Userver installation complete."
    #installation process for Fendesk
    print "Installing Fendesk \n"
    fendesk.pull()
    fendesk.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = fendesk.name)
    fendesk.configure()
    #update process.json: replace existing Fendesk entry or create new entry
    updated = False
    for i in len(process['apps']):
        if process['apps'][i]['name'] == 'Fendesk':
            process['apps'][i]['script'] = './fendesk/app.js'
            process['apps'][i]['cwd'] = './fendesk'
            process['apps'][i]['out_file'] = './logs/pm2-fendesk.log'
            process['apps'][i]['error_file'] = './logs/pm2-fendesk-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Fendesk',
            'script': './fendesk/app.js',
            'cwd': './fendesk',
            'out_file': './logs/pm2-fendesk.log',
            'error_file': './logs/pm2-fendesk-error.log'
        })
    print "Fendesk installation complete."
    finish()
    return
        
    
# Exit program
def finish():
    print 'Writing process.json and starting servers of the installed components...'
    with open('process.json', 'w') as outfile:  
        json.dump(process, outfile)
    subprocess.call(['pm2','start','process.json'])
    sys.exit()

    
# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': acedirectinstall,
    '2': acrcdrinstall,
    '3': mgmtinstall,
    '4': aserverinstall,
    '5': userverinstall,
    '6': fendeskinstall,
    '7': quickinstall,
    '0': finish,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    #check operating system
    if platform.system() != 'Linux':
        print 'Installation script can only be run on Linux. Terminating...'
        quit()
    #check distribution    
    dist = platform.dist()[0]
    if dist != 'centos' and dist != 'redhat' and dist != 'fedora':
        print 'Installation script can only be run on CentOS, RedHat, or Fedora. Terminating...'
        quit()
    print 'MySQL must be installed prior to installing several of the available modules in this script. \
In order to check for installation on this machine, run the command "rpm -qa |grep mysql".'
    sys.stdout.flush()
    sleep(1.5)
    out = subprocess.check_output('test -e dat && echo -n True || echo -n False', shell=True)
    out_bool = out.lower() in ("false")
    if out_bool:
        print 'Creating dat directory...'
        subprocess.call('mkdir dat', shell=True)
    #set up hashconfig
    print 'Installing HashConfig tool for configuration process...'
    hashconfig = Repository('hashconfig','https://github.com/mitrefccace/hashconfig.git','hconfig.js')
    hashconfig.pull()
    hashconfig.install()
    print 'HashConfig installation complete. Installing pm2, bower, and apidoc...'
    sys.stdout.flush()
    sleep(1)
    subprocess.call(['npm', 'install', '-g', 'bower'])
    subprocess.call(['npm','install','pm2','-g'])
    subprocess.call(['npm','install','apidoc','-g'])
    sys.stdout.flush()
    sleep(1)
    #stop all processes
    subprocess.call(['pm2','kill'])
    # Launch main menu
    main_menu()