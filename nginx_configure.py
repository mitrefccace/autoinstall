# Import the modules needed to run the script.
import sys, os
import subprocess
import os.path
from time import sleep
import platform
import json
import textwrap
import base64

if __name__ == '__main__':
    start_prompt = textwrap.fill('This script will modify the Nginx configuration based on the most recent ACE Direct '
                                 'configuration. Any changes made to /etc/nginx/nginx.conf will be overwritten. Do you '
                                 'wish to continue? (y/n): ', width=80)
    start = raw_input(start_prompt)
    if start == 'n':
        sys.exit()
    elif start == 'y':
        #open config.json and determine whether it's encoded
        with open('dat/config.json') as data_file:
            config = json.load(data_file)
        cleartext = config['common']['cleartext']
        #extract relevant values from config.json
        if len(cleartext) == 0: #encoded file
            openam_fqdn = base64.b64decode(config['openam']['fqdn'])
            openam_port = base64.b64decode(config['openam']['port'])
            ace_direct_port = base64.b64decode(config['ace_direct']['https_listen_port'])
            management_portal_port = base64.b64decode(config['management_portal']['https_listen_port'])
        else: #decoded file
            openam_fqdn = config['openam']['fqdn']
            openam_port = config['openam']['port']
            ace_direct_port = config['ace_direct']['https_listen_port']
            management_portal_port = config['management_portal']['https_listen_port']
        #re-download nginx
        subprocess.call('git pull', shell=True, cwd='nginx')
        subprocess.call(['sudo','cp','nginx/nginx.conf','/etc/nginx/nginx.conf'])
        subprocess.call('sudo sed -i -e \'s/<OPENAM FQDN>/' + openam_fqdn + '/g\' /etc/nginx/nginx.conf', shell=True)
        subprocess.call('sudo sed -i -e \'s/<OPENAM PORT>/' + openam_port + '/g\' /etc/nginx/nginx.conf', shell=True)
        subprocess.call('sudo sed -i -e \'s/<ACE DIRECT PORT>/' + ace_direct_port + '/g\' /etc/nginx/nginx.conf',
                        shell=True)
        subprocess.call('sudo sed -i -e \'s/<MANAGEMENT PORTAL PORT>/' + management_portal_port +
                        '/g\' /etc/nginx/nginx.conf', shell=True)
        subprocess.call(['sudo','service','nginx','restart'])
