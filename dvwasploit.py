#!/usr/bin/python3

import requests
from core import authenticator , info
from core.network import check_connection
from urllib.parse import urljoin
from optparse import OptionParser
from vulns import rce , sqli , lfi , upload , password_spray

def banner():

    banner = "\033[1;90m\n"
    banner += """                                                                 .*#####.       
                                               .(##############(((.    *######  
                                                  *.           ,########   *### 
                                           *((.                     /######* .##
                                      ,###                             ######. #
                                   .##.                                  #####  
 ############   ####.     ####  ####   .####*   ####   ######            .####% 
 ####     ####(  ####    ####,## ###,  (#####   ###   ###(###/            ####* 
 ####      ####.  ###/   ###//#. ####  ######, ####  /### ,###.           ####  
 ####      ####,  (###, ####/#   .###.(## .###,###   ###   /###          #### # 
 ####     .####    ####(### #,    #######  ######(  ############        ###(*#* 
 ####(//#####/      ###### #/     .#####   /#####  ####     (####      ##(.###  
 #########,         .####*###      ####(    ####  .###,      #### .* (#/ ####   
                       ##.###/                                 *#  (( *#####    
                       ,##  (###                            ##* .(  ######,     
                         ###.    (###/                 (###     .#######        
                          ######                 *#####      ########           
                             /###################(      #######/                """


    banner += "\n\n\t\t\t\033[1;91m   Author\033[0;37m  ->  \033[0;104mAbdallah Mohamed Elsharif\033[0;37m\n\n"
    
    return banner

def register_option():
    parser = OptionParser(banner())
    parser.add_option('-u','--url',dest='url',help='Your Target Url')
    parser.add_option('-a','--auth',dest='auth',help='For DVWA authentication Ex (USER:PASSWD)')
    opt , _ = parser.parse_args()
    return (parser , opt)

def is_dvwa(url):
    response = requests.get(urljoin(url,"login.php"))
    return response.status_code == 200 and "Damn Vulnerable Web Application" in response.text

def main():
    parser , option = register_option()
    print(parser.usage)

    if option.url:
        url = (option.url + '/') if (option.url[-1] != '/') else option.url
        check_connection(url) # tool will close if the server was unreachable
        info.Info(url).display_server_info()        

        if is_dvwa(url):
            cookies = authenticator.handle_auth(url,option.auth)
            rce.exploit(url,cookies)
            sqli.exploit(url,cookies)
            lfi.exploit(url,cookies)
            upload.exploit(url,cookies)
            password_spray.exploit(url,cookies)

        else:
            print("This cms is not DVWA")

if __name__ == '__main__':
    main()