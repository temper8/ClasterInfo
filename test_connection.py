import paramiko 
import json
import sys

def get_secrets(fname:str):
    try:
        f = open(fname, 'rb')
    except OSError:
        print("Could not open/read file:", fname)
        sys.exit()
    with f:
        data = json.load(f)
    return data['host'], data['user']  

def get_remote_ls(host:str, user:str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, port=22)
    stdin, stdout, stderr = client.exec_command('ls -l')
    data = stdout.read() + stderr.read()
    client.close()
    return data.decode("utf-8")

host, user = get_secrets('site.json')
res = get_remote_ls(host, user)
print(res)