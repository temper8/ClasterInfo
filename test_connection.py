import paramiko 
import json
import sys

def get_info(fname:str):
    try:
        f = open(fname, 'rb')
    except OSError:
        print("Could not open/read file:", fname)
        sys.exit()
    with f:
        data = json.load(f)
    return data['host'], data['user']  

host, user = get_info('site.json')

port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, port=port)
stdin, stdout, stderr = client.exec_command('ls -l')
data = stdout.read() + stderr.read()
client.close()

print(data.decode("utf-8"))