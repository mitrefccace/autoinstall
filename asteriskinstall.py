import subprocess
import os.path
from time import sleep
import platform

print 'Before running this script, make sure the public/private key-pair for Git \
 have been added to /root/.ssh/ and their permissions are 600'

sleep(1.5) 

#download Asterisk
subprocess.call(['sudo', 'wget', '-N', 'http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-14.3.0.tar.gz'], cwd = '/usr/src')
subprocess.call(['sudo', 'tar', '-zxf', 'asterisk-14.3.0.tar.gz'], cwd = '/usr/src')

#install pre-requisites
subprocess.call(['./contrib/scripts/install_prereq'], cwd = '/usr/src/asterisk-14.3.0')

#install PJSIP and asterisk

subprocess.call(['./configure', '--with-pjproject-bundled'], cwd = '/usr/src/asterisk-14.3.0')
subprocess.call(['make', '&&', 'make', 'install', '&&', 'make', 'samples'], cwd = '/usr/src/asterisk-14.3.0')
subprocess.call(['make', 'config'], cwd = '/usr/src/asterisk-14.3.0')
subprocess.call(['service', 'asterisk', 'start'], cwd = '/usr/src/asterisk-14.3.0')

#add git repo domain name to known_hosts so RSA fingerprint prompt does not pause script
subprocess.call(['ssh-keyscan', 'github.com', '>>', '~/.ssh/known_hosts'], cwd = '/usr/src/asterisk-14.3.0')

# pull down confi/media files and add to /etc/asterisk and /var/lib/asterisk/sounds, respectively
subprocess.call(['git', 'clone', 'https://github.com/mitrefccace/asterisk.git'], cwd = '~')
subprocess.call(['git', 'checkout', 'AD'], cwd = '~/asterisk')
subprocess.call(['yes', '|', 'cp', '-rf', 'asterisk-configs/*', '/etc/asterisk'], cwd = '~/asterisk')
subprocess.call(['yes', '|', 'cp', '-rf', 'asterisk-videos-audios/sounds/*', '/var/lib/asterisk/sounds/'], cwd = '~/asterisk')

subprocess.call(['sed', '-i', '-e', '"s/<public_ip>/$1/g"', 'pjsip.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<local_ip>/$2/g"', 'pjsip.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<dialin>/$3/g"', 'extensions.conf', 'pjsip.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<stun_server>/$4/g"', 'rtp.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<crt_file>/$5/g"', 'http.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<crt_key>/$6/g"', 'http.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<ss_crt>/$7/g"', 'pjsip.conf'], cwd = '/etc/asterisk')
subprocess.call(['sed', '-i', '-e', '"s/<ss_ca_crt>/$8/g"', 'pjsip.conf'], cwd = '/etc/asterisk')

subprocess.call(['service', 'asterisk', 'restart'], cwd = '/etc/asterisk')