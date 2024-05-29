import paramiko 
import json
import sys
import hashlib

def get_secrets(fname:str):
    try:
        f = open(fname, 'rb')
    except OSError:
        print("Could not open/read file:", fname)
        sys.exit()
    with f:
        data = json.load(f)
    return data['host'], data['user']  

def get_last_hash(fname):
    # ='last_hash.txt'
    try:
        f = open(fname, 'rb')
    except OSError:
        print("Could not open/read file:", fname)
        return "12345678"
    with f:
        return f.read().decode("utf-8")
    
def compare_hash(hash:str):
    fn = "last_hash"
    last = get_last_hash(fn)
    print(last)
    print(hash)
    if last == hash:
        print("хэши совпадают")
        return True
    else:
        with open(fn, 'w') as f:
            f.write(hash)
        print('записал новый хэш')
        return False


def get_remote_sinfo(host:str, user:str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, port=22)
    stdin, stdout, stderr = client.exec_command('sinfo')
    data = stdout.read() + stderr.read()
    client.close()
    return data.decode("utf-8")

host, user = get_secrets('site.json')
info = get_remote_sinfo(host, user)
print(info)


h = hashlib.md5(info.encode('utf-8')).hexdigest()
if compare_hash(h):
    print('ничего не делать')
else:
    print('отправить в телеграмм')
