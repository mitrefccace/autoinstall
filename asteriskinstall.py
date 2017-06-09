import subprocess

public_ip = raw_input('Enter value for public_ip:')
local_ip = raw_input('Enter value for local_ip:')
dial_in = raw_input('Enter value for dial_in:')
stun_server = raw_input('Enter value for stun_server:')
public_key = raw_input('Enter value for public_key:')
private_key = raw_input('Enter value for private_key:')
#crt_file = raw_input('Enter value for crt_file:')
#crt_key = raw_input('Enter value for crt_key:')

subprocess.call(['wget', 'https://raw.githubusercontent.com/mitrefccace/asterisk/AD/scripts/AD_asterisk_install_script.sh'])
subprocess.call(['chmod', '+x', 'AD_asterisk_install_script.sh'])
subprocess.call('./AD_asterisk_install_script.sh' + ' ' + public_ip + ' ' + local_ip + ' ' + dial_in + ' '
                 + stun_server + ' ' + public_key + ' ' + private_key, shell=True)
#subprocess.call(['./AD_asterisk_install.sh', '--public-ip', public_ip, '--local-ip', local_ip, 
#                 '--stun-server', stun_server, '--dial-in', dial_in, '--crt-file', crt_file,
#                 '--crt-key', crt_key])