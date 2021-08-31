
import requests
import sys
from urllib.parse import urljoin,urlparse
from core.common import makeHeaders


def authenticate(url,user = "admin" , passwd = "password"):

    # authenticate and return cookies

    data = {
        'username' : user,
        'password' : passwd,
        'Login'    : 'Login'
    }

    headers = makeHeaders(urlparse(url).hostname)
    full_url = urljoin(url,"login.php")
    session = requests.Session()
    req = session.get(full_url,headers=headers)
    session.cookies.update(req.cookies.get_dict())
    res = session.post(full_url,headers=headers,data=data)

    if f"You have logged in as '{user}'" in res.text:
        # Login succeed
        session.cookies.set('security', None)
        session.cookies.set("security","low")
        
        return session.cookies.get_dict()

    else:
        # Login failed
        print(f"'{user}' and '{passwd}' isn't correct !!")
        print("Use -a/--auth with right credenitials")
        
        return sys.exit(1)

def handle_auth(url,auth):
    if auth:
        if ':' in auth:
            user , passwd = auth.split(':')
            return authenticate(url,user=user,passwd=passwd)
        else:
            print(f"{auth} isn't correct, use like this  -> 'user:pass'")
            return sys.exit(1)
    else:
        return authenticate(url)
    
