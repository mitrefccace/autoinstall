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
import textwrap
import base64

class Repository:

    #constructor
    def __init__(self, name, giturl):
        self.name = name
        self.giturl = giturl
        
    #pull method -- git clone if the repo doesn't exist locally; error message if it does exist locally
    def pull(self, branch):
        out = subprocess.check_output('test -e %s && echo -n True || echo -n False' % self.name, shell=True)
        out_bool = out.lower() in ("true")
        if out_bool:
            print 'Directory already exists. Running "git pull"...'
            subprocess.call('git pull', shell=True, cwd=self.name)
        else:
            subprocess.call('git clone %s' % self.giturl, shell=True)
        subprocess.call('git checkout %s' % branch, shell=True, cwd=self.name)

    #install method -- run npm install
    def install(self):
        subprocess.call(['npm','install'], cwd=self.name)
 
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
    print "Please select one of the following options for installation. When finished, choose option 0 for " \
          "configuration:"
    print "1. Quick installation & configuration (all servers)"
    print "2. Install Agent and Consumer Portals"
    print "3. Install ACR-CDR"
    print "4. Install Management Portal"
    print "5. Install Aserver"
    print "6. Install Userver"
    print "7. Install Fendesk"
    print "8. Install Virtual Agent"
    print "9. Exit script without configuration"
    print "\n0. Finish installation, begin configuration"
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
def quickinstall():
    #gather all repos
    acedirect = Repository('acedirect', gitSource + '/acedirect.git')
    acrcdr = Repository('acr-cdr', gitSource +'/acr-cdr.git')
    mgmt = Repository('managementportal', gitSource + '/managementportal.git')
    aserver = Repository('aserver', gitSource + '/aserver.git')
    userver = Repository('userver', gitSource + '/userver.git')
    fendesk = Repository('fendesk', gitSource + '/fendesk.git')
    virtualagent = Repository('virtualagent', gitSource + '/virtualagent.git')
    #installation process for ACE Direct
    print "Installing ACE Direct \n"
    acedirect.pull(branch)
    acedirect.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = acedirect.name)
    #update process.json: replace existing ACE Direct entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-adserver-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "ACE Direct installation complete."
    #installation process for ACR-CDR
    print "Installing ACR-CDR \n"
    acrcdr.pull(branch)
    acrcdr.install()
    #update process.json: replace existing CDR entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-app-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "ACR-CDR installation complete."
    #installation process for Management Portal
    print "Installing Management Portal \n"
    mgmt.pull(branch)
    mgmt.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = mgmt.name)
    #update process.json: replace existing Management entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-server-db-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Management portal installation complete."
    #installation process for Aserver
    print "Installing Aserver \n"
    aserver.pull(branch)
    aserver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = aserver.name)
    #update process.json: replace existing Aserver entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-aserver-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Aserver installation complete."
    #installation process for Userver
    print "Installing Userver \n"
    userver.pull(branch)
    userver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = userver.name)
    #update process.json: replace existing Userver entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-userver-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Userver installation complete."
    #installation process for Fendesk
    print "Installing Fendesk \n"
    fendesk.pull(branch)
    fendesk.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = fendesk.name)
    #update process.json: replace existing Fendesk entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-fendesk-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Fendesk installation complete."
    print "Installing Virtualagent \n"
    virtualagent.pull(branch)
    virtualagent.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = virtualagent.name)
    #update process.json: replace existing Fendesk entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
        if process['apps'][i]['name'] == 'Virtualagent':
            process['apps'][i]['script'] = './virtualagent/bin/www'
            process['apps'][i]['cwd'] = './virtualagent'
            process['apps'][i]['out_file'] = './logs/pm2-virtualagent.log'
            process['apps'][i]['error_file'] = './logs/pm2-virtualagent-error.log'
            updated = True
    if updated == False:
        process['apps'].append({
            'name': 'Virtualagent',
            'script': './virtualagent/bin/www',
            'cwd': './virtualagent',
            'out_file': './logs/pm2-virtualagent.log',
            'error_file': './logs/pm2-virtualagent-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Virtualagent installation complete."
    configure_and_start_servers()
    return

# Menu 2
def acedirectinstall():
    acedirect = Repository('acedirect', gitSource + '/acedirect.git')
    print "Installing ACE Direct \n"
    acedirect.pull(branch)
    acedirect.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = acedirect.name)
    #update process.json: replace existing ACE Direct entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-adserver-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "ACE Direct installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
 
 
# Menu 3
def acrcdrinstall():
    acrcdr = Repository('acr-cdr', gitSource + '/acr-cdr.git')
    print "Installing ACR-CDR \n"
    acrcdr.pull(branch)
    acrcdr.install()
    #update process.json: replace existing CDR entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-app-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "ACR-CDR installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
 
# Menu 4
def mgmtinstall():
    mgmt = Repository('managementportal', gitSource + '/managementportal.git')
    print "Installing Management Portal \n"
    mgmt.pull(branch)
    mgmt.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = mgmt.name)
    #update process.json: replace existing Management entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-server-db-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Management portal installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return

# Menu 5
def aserverinstall():
    aserver = Repository('aserver', gitSource + '/aserver.git')
    print "Installing Aserver \n"
    aserver.pull(branch)
    aserver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = aserver.name)
    #update process.json: replace existing Aserver entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-aserver-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Aserver installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
    
# Menu 6
def userverinstall():
    userver = Repository('userver', gitSource + '/userver.git')
    print "Installing Userver \n"
    userver.pull(branch)
    userver.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = userver.name)
    #update process.json: replace existing Userver entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-userver-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Userver installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return


#     Menu 7
def fendeskinstall():
    fendesk = Repository('fendesk', gitSource + '/fendesk.git')
    print "Installing Fendesk \n"
    fendesk.pull(branch)
    fendesk.install()
    subprocess.call(['apidoc','-i','routes/','-o','apidoc/'], cwd = fendesk.name)
    #update process.json: replace existing Fendesk entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
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
            'error_file': './logs/pm2-fendesk-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Fendesk installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
 
# Menu 8
def virtualagentinstall():
    virtualagent = Repository('virtualagent', gitSource + '/virtualagent.git')
    print "Installing Virtualagent \n"
    virtualagent.pull(branch)
    virtualagent.install()
    subprocess.call(['bower', 'install', '--allow-root'], cwd = virtualagent.name)
    #update process.json: replace existing Fendesk entry or create new entry
    updated = False
    for i in range(len(process['apps'])):
        if process['apps'][i]['name'] == 'Virtualagent':
            process['apps'][i]['script'] = './virtualagent/bin/www'
            process['apps'][i]['cwd'] = './virtualagent'
            process['apps'][i]['out_file'] = './logs/pm2-virtualagent.log'
            process['apps'][i]['error_file'] = './logs/pm2-virtualagent-error.log'
            updated = True
    if updated == False:
        process['apps'].append({  
            'name': 'Virtualagent',
            'script': './virtualagent/bin/www',
            'cwd': './virtualagent',
            'out_file': './logs/pm2-virtualagent.log',
            'error_file': './logs/pm2-virtualagent-error.log',
            'max_restarts': 10,
            'min_uptime': '5s'
        })
    print "Virtualagent installation complete. Returning to main menu..."
    sys.stdout.flush()
    sleep(2)
    menu_actions['main_menu']()
    return
    
#Menu 9
def exit_script():
    print 'Exiting script...'
    sys.exit()
        
    
# Menu 0
def configure_and_start_servers():
    print 'Beginning configuration...'
    configure()
    print 'Writing process.json and starting servers of the installed components...'
    with open('process.json', 'w') as outfile:  
        json.dump(process, outfile)
    subprocess.call(['pm2','start','process.json'])
    sys.exit()

#Configuration
def configure():
    #configure node servers with config.json
    if not os.path.isfile('/home/centos/dat/color_config.json'):
        subprocess.call(['cp', 'dat/color_config.json_TEMPLATE', 'dat/color_config.json'])
    if not os.path.isfile('/home/centos/dat/default_color_config.json'):
        subprocess.call(['cp', 'dat/default_color_config.json_TEMPLATE', 'dat/default_color_config.json'])
    if os.path.isfile('/home/centos/config_acedirect.json_TEMPLATE'):
        encoded = 'y'
        subprocess.call(['node','hconfig.js', '-fn', '/home/centos/config_acedirect.json_TEMPLATE'],
                        cwd = hashconfig.name)
        subprocess.call(['cp', 'hashconfig/config_new.json', 'dat/config.json'])
    else:
        templatePrompt = textwrap.fill('Please enter the full path to the configuration template file, or press enter to'
                                       ' use the default file: ',width=80)
        template = raw_input(templatePrompt)
        if template == '':
            template = '/home/centos/dat/config.json_TEMPLATE'
        print 'Please follow prompts to generate the configuration file. For more information about the configuration ' \
              'parameters, please refer to dat/parameter_desc.json.'
        encodePrompt = textwrap.fill('Do you want the configuration file config.json to be base64 encoded? (y/n): ',
                                     width=80)
        encoded = raw_input(encodePrompt)
        if encoded == 'y':
            subprocess.call(['node','hconfig.js', '-n', template], cwd = hashconfig.name)
        else:
            subprocess.call(['node', 'hconfig.js', '-no', template], cwd=hashconfig.name)
        subprocess.call(['cp', 'hashconfig/config_new.json', 'dat/config.json'])
    #configure nginx with nginx.conf
    with open('/home/centos/dat/config.json') as data_file:
        config = json.load(data_file)
    nginx = Repository('nginx',gitSource + '/nginx.git')
    nginx.pull(branch)
    if encoded = 'y':
        openam_fqdn = base64.decode(config['openam']['fqdn'])
        openam_port = base64.decode(config['openam']['port'])
        ace_direct_port = base64.decode(config['ace_direct']['https_listen_port'])
        management_portal_port = base64.decode(config['management_portal']['https_listen_port'])
    else:
        openam_fqdn = config['openam']['fqdn']
        openam_port = config['openam']['port']
        ace_direct_port = config['ace_direct']['https_listen_port']
        management_portal_port = config['management_portal']['https_listen_port']
    subprocess.call('sed -i -e \'s/<OPENAM FQDN>/' + openam_fqdn + '/g\' nginx/nginx.conf', shell=True)
    subprocess.call('sed -i -e \'s/<OPENAM PORT>/' + openam_port + '/g\' nginx/nginx.conf', shell=True)
    subprocess.call('sed -i -e \'s/<ACE DIRECT PORT>/' + ace_direct_port + '/g\' nginx/nginx.conf',
                    shell=True)
    subprocess.call('sed -i -e \'s/<MANAGEMENT PORTAL PORT>/' + management_portal_port +
                    '/g\' nginx/nginx.conf', shell=True)
    subprocess.call(['sudo', 'cp', 'nginx/nginx.conf', '/etc/nginx/nginx.conf'])
    subprocess.call(['sudo','service','nginx','restart'])


# Parse command line
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts					

    
# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': quickinstall,
    '2': acedirectinstall,
    '3': acrcdrinstall,
    '4': mgmtinstall,
    '5': aserverinstall,
    '6': userverinstall,
    '7': fendeskinstall,
    '8': virtualagentinstall,
    '9': exit_script,
    '0': configure_and_start_servers,
}
 
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    #import command line args
    myargs = getopts(sys.argv)
    if '-s' in myargs:  #Git source
        gitSource = myargs['-s']
	if '-b' in myargs: #Git branch
		branch = myargs['-b']
    #check operating system
    if platform.system() != 'Linux':
        print 'Installation script can only be run on Linux. Terminating...'
        quit()
    #check distribution    
    dist = platform.dist()[0]
    if dist != 'centos' and dist != 'redhat' and dist != 'fedora':
        print 'Installation script can only be run on CentOS, RedHat, or Fedora. Terminating...'
        quit()

    #Install Redis
    print 'Installing Redis...'
    subprocess.call(['sudo','yum','install','epel-release'])
    subprocess.call(['sudo','yum','update'])
    subprocess.call(['sudo','yum','install','redis'])
    subprocess.call(['sudo','systemctl','start','redis'])
    subprocess.call(['sudo', 'systemctl', 'enable', 'redis'])

    #Install Nginx
    print 'Installing Nginx...'
    subprocess.call(['sudo','yum','install','nginx'])
    subprocess.call(['sudo','systemctl','start','nginx'])
    subprocess.call(['sudo', 'systemctl', 'enable', 'nginx'])

    # install mongoDB
    print 'Installing MongoDB...'
    if os.path.isfile('/etc/yum.repos.d/mongodb-org.repo'):
        subprocess.call(['sudo','rm','/etc/yum.repos.d/mongodb-org.repo'])
    subprocess.call(['sudo', 'touch', '/etc/yum.repos.d/mongodb-org.repo'])
    subprocess.call('echo \'[mongodb-org-3.4]\' | sudo tee -a /etc/yum.repos.d/mongodb-org.repo > /dev/null', shell=True)
    subprocess.call('echo \'name=MongoDB Repository\' | sudo tee -a /etc/yum.repos.d/mongodb-org.repo > /dev/null',
                    shell=True)
    subprocess.call('echo \'baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.4/x86_64/\' | sudo '
                    'tee -a /etc/yum.repos.d/mongodb-org.repo > /dev/null', shell=True)
    subprocess.call('echo \'gpgcheck=1\' | sudo tee -a /etc/yum.repos.d/mongodb-org.repo > /dev/null', shell=True)
    subprocess.call('echo \'enabled=1\' | sudo tee -a /etc/yum.repos.d/mongodb-org.repo > /dev/null', shell=True)
    subprocess.call('echo \'gpgkey=https://www.mongodb.org/static/pgp/server-3.4.asc\' | sudo tee -a /etc/yum.repos.d/'
                    'mongodb-org.repo > /dev/null', shell=True)
    subprocess.call(['sudo', 'yum', 'install', 'mongodb-org'])
    subprocess.call(['sudo', 'systemctl', 'start', 'mongod'])
    subprocess.call(['sudo', 'systemctl', 'enable', 'mongod'])

    #install git, wget, and node.js
    print 'Installing Git, wget, and Node.js...'
    sleep(1)
    subprocess.call(['sudo', 'yum', 'install', 'git'])
    subprocess.call(['sudo', 'yum', 'install', 'wget'])
    subprocess.call(['sudo', 'yum', 'install', 'nodejs'])


    #install dat
    print 'Pulling configuration files...'
    #dat = Repository('dat','https://github.com/mitrefccace/dat.git')
    dat = Repository('dat', gitSource + '/dat.git')
    dat.pull(branch)

    #set up hashconfig
    print 'Installing HashConfig tool for configuration process...'
    #hashconfig = Repository('hashconfig','https://github.com/mitrefccace/hashconfig.git')
    hashconfig = Repository('hashconfig', gitSource + '/hashconfig.git')
    hashconfig.pull(branch)
    hashconfig.install()
    print 'HashConfig installation complete. Installing pm2, bower, and apidoc...'
    sys.stdout.flush()
    sleep(1)
    subprocess.call(['sudo','npm', 'install', '-g', 'bower'])
    subprocess.call(['sudo','npm','install','pm2','-g'])
    subprocess.call(['sudo','npm','install','apidoc','-g'])
    sys.stdout.flush()
    sleep(1)

    #stop all processes
    subprocess.call(['pm2','kill'])

    # Launch main menu
    main_menu()