
import requests
from urllib.parse import urlparse

class Info:
    def __init__(self,url):
        self.url = url
        self.parser = urlparse(self.url)
        self.hostname = self.parser.hostname
        self.port = self.parser.port if self.parser.port else 80 if self.parser.scheme == 'http' else 443
        self.path = self.parser.path
        self.headers = requests.get(self.url).headers
        self.date = self.headers.get("Date")
        self.server = self.headers.get("Server")
        self.technology = self.headers.get("X-Powered-By")

    def display_server_info(self):
        print(f"HostName        :   {self.hostname}")
        print(f"Port            :   {str(self.port)}")
        print(f"Full Url        :   {self.url}")
        if self.path:
            print(f"Path            :   {self.path}")
        print(f"Date            :   {self.date}")
        print(f"Server          :   {self.server}")
        if self.technology:
            print(f"Technology      :   {self.technology}")

        print()

