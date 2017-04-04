import subprocess
import os.path
from time import sleep
import platform
import sys

sleep(1.5) 

#parse command line options

#download Asterisk
#(commented out during testing)
#subprocess.call(['wget', '-N', 'http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-14.3.0.tar.gz'], cwd = '/usr/src')
#subprocess.call(['tar', '-zxf', 'asterisk-14.3.0.tar.gz'], cwd = '/usr/src')

#install pre-requisites
subprocess.call(['./contrib/scripts/install_prereq'], cwd = '/usr/src/asterisk-14.3.0')

#install PJSIP and asterisk

subprocess.call(['./configure', '--with-pjproject-bundled'], cwd = '/usr/src/asterisk-14.3.0')
subprocess.call(['make', '&&', 'make', 'install', '&&', 'make', 'samples'], cwd = '/usr/src/asterisk-14.3.0')
subprocess.call(['make', 'config'], cwd = '/usr/src/asterisk-14.3.0')
subprocess.call(['service', 'asterisk', 'start'], cwd = '/usr/src/asterisk-14.3.0')

#add git repo domain name to known_hosts so RSA fingerprint prompt does not pause script
subprocess.call(['ssh-keyscan', 'github.com', '>>', '/root/.ssh/known_hosts'], cwd = '/usr/src/asterisk-14.3.0')

# pull down confi/media files and add to /etc/asterisk and /var/lib/asterisk/sounds, respectively
subprocess.call(['git', 'clone', 'https://github.com/mitrefccace/asterisk.git'], cwd = '/root')
subprocess.call(['git', 'checkout', 'AD'], cwd = '/root/asterisk')
subprocess.call(['yes', '|', 'cp', '-r', 'asterisk-configs/*', '/etc/asterisk'], cwd = '/root/asterisk')
subprocess.call(['yes', '|', 'cp', '-r', 'asterisk-videos-audios/sounds/*', '/var/lib/asterisk/sounds/'], cwd = '/root/asterisk')

subprocess.call(['sed', '-i', '-e', '"s/<public_ip>/' + sys.argv[1] + '/g"', 'pjsip.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<local_ip>/' + sys.argv[2] + '/g"', 'pjsip.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<dialin>/' + sys.argv[3] + '/g"', 'extensions.conf', 'pjsip.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<stun_server>/' + sys.argv[4] + '/g"', 'rtp.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<crt_file>/' + sys.argv[5] + '/g"', 'http.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<crt_key>/' + sys.argv[6] + '/g"', 'http.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<ss_crt>/' + sys.argv[7] + '/g"', 'pjsip.conf'], cwd = '/etc/asterisk/asterisk-configs')
subprocess.call(['sed', '-i', '-e', '"s/<ss_ca_crt>/' + sys.argv[8] + '/g"', 'pjsip.conf'], cwd = '/etc/asterisk/asterisk-configs')

subprocess.call(['service', 'asterisk', 'restart'], cwd = '/etc/asterisk')