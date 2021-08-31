
import socket
import sys
import requests
import threading
import netifaces as ni
from netaddr import IPNetwork
from http.server import HTTPServer, CGIHTTPRequestHandler

class WebServerHandler(CGIHTTPRequestHandler):

    # To Override log_message function for avoid console output
    def log_message(self, format, *args):
        pass


class WebServer():

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server = HTTPServer( ('0.0.0.0', self.port) , WebServerHandler)

    def run(self):
        thread = threading.Thread(target=self.server.serve_forever)
        thread.setDaemon(True)
        thread.start()

    def stop(self):
        self.server.server_close()
        self.server.shutdown()
    

def ip_on_same_network(ip):
    # Get all IPs from internet card and return ip which in same lan

    for i in socket.if_nameindex():
        try:
            ip2 = ni.ifaddresses(i[1])[ni.AF_INET][0]['addr']
            if IPNetwork(f"{ip}/255.255.255.0") == IPNetwork(f"{ip2}/255.255.255.0"):
                return ip2
        except ValueError:
            continue
        except KeyError:
            continue

def get_public_ip():
    return requests.get('https://api.ipify.org').text

def check_connection(url):
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        print("This server is unreachable !!")
        sys.exit(1)