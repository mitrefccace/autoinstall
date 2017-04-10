import subprocess
import os.path
from time import sleep
import platform
import sys

sleep(1.5) 

ans = raw_input('Do you want to update packages using "yum -y update"? (y/n)')
if ans == 'y':
    subprocess.call('yum -y update', shell=True)
elif ans == 'n':
    print 'Skipping update...'
else:
    print 'Invalid input. Must enter "y" or "n".'
subprocess.call('yum -y install -y epel-release bzip2 dmidecode gcc-c++ ncurses-devel libxml2-devel make wget openssl-devel newt-devel kernel-devel sqlite-devel libuuid-devel gtk2-devel jansson-devel binutils-devel git patch', shell=True)

#download Asterisk
#(commented out during testing)
subprocess.call(['wget', '-N', 'http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-14.2.1.tar.gz'], cwd = '/usr/src')
subprocess.call(['tar', '-zxf', 'asterisk-14.2.1.tar.gz'], cwd = '/usr/src')

#install pre-requisites
subprocess.call(['./contrib/scripts/install_prereq', 'install'], cwd = '/usr/src/asterisk-14.2.1')

#install PJSIP and asterisk

subprocess.call(['./configure', '--with-pjproject-bundled'], cwd = '/usr/src/asterisk-14.2.1')
subprocess.call(['make'], cwd= '/usr/src/asterisk-14.2.1')
subprocess.call(['make', 'install'], cwd = '/usr/src/asterisk-14.2.1')
subprocess.call(['make', 'samples'], cwd = '/usr/src/asterisk-14.2.1')
subprocess.call(['make', 'config'], cwd = '/usr/src/asterisk-14.2.1')

subprocess.call('echo "/usr/local/lib? > /etc/ld.so.conf.d/usr_local.conf', shell=True)
subprocess.call(['/sbin/ldconfig'])

#add git repo domain name to known_hosts so RSA fingerprint prompt does not pause script
subprocess.call(['ssh-keyscan', 'github.com', '>>', '/root/.ssh/known_hosts'], cwd = '/usr/src/asterisk-14.2.1')

# pull down confi/media files and add to /etc/asterisk and /var/lib/asterisk/sounds, respectively
subprocess.call(['git', 'clone', 'https://github.com/mitrefccace/asterisk.git'], cwd = '/root')
subprocess.call(['git', 'checkout', 'AD'], cwd = '/root/asterisk')
subprocess.call('cp -rf asterisk-configs/* /etc/asterisk', shell=True, cwd = '/root/asterisk')
subprocess.call('cp -rf asterisk-videos-audios/sounds/* /var/lib/asterisk/sounds/', shell=True, cwd = '/root/asterisk')

subprocess.call('sed -i -e "s/<public_ip>/' + sys.argv[1] + '/g" pjsip.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<local_ip>/' + sys.argv[2] + '/g" pjsip.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<dialin>/' + sys.argv[3] + '/g" extensions.conf pjsip.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<stun_server>/' + sys.argv[4] + '/g" rtp.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<crt_file>/' + sys.argv[5] + '/g" http.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<crt_key>/' + sys.argv[6] + '/g" http.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<ss_crt>/' + sys.argv[7] + '/g" pjsip.conf', shell=True, cwd = '/etc/asterisk')
subprocess.call('sed -i -e "s/<ss_ca_crt>/' + sys.argv[8] + '/g" pjsip.conf', shell=True, cwd = '/etc/asterisk')

subprocess.call(['service', 'asterisk', 'start'], cwd = '/etc/asterisk')