from os import name,system,stat
from sys import stdout
from time import sleep
from datetime import datetime
from random import choice

colors = {'white': "\033[1;37m", 'green': "\033[0;32m", 'red': "\033[0;31m", 'yellow': "\033[1;33m",'bblue':"\033[1;34;40m",'bcyan':"\033[1;36;40m"}

def _clear():
    """Clears the console on every os."""
    if name == 'posix':
        system('clear')
    elif name in ('ce', 'nt', 'dos'):
        system('cls')
    else:
        print("\n") * 120

def _setTitle(title:str):
    """Sets the console title on every os."""
    if name == 'posix':
        stdout.write(f"\x1b]2;{title}\x07")
    elif name in ('ce', 'nt', 'dos'):
        system(f'title {title}')
    else:
        stdout.write(f"\x1b]2;{title}\x07")

def _printText(bracket_color,text_in_bracket_color,text_in_bracket,text):
    """Prints colored formatted text."""
    stdout.flush()
    text = text.encode('ascii','replace').decode()
    stdout.write(bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')

def _readFile(filename,method):
    """Read file with empty and file not found check."""
    try:
        if stat(filename).st_size != 0:
            with open(filename,method,encoding='utf8') as f:
                content = [line.strip('\n') for line in f]
                return content
        else:
            _printText(colors['red'],colors['white'],'ERROR',f'{filename} is empty!')
            sleep(2)
            raise SystemExit
    except FileNotFoundError:
        _printText(colors['red'],colors['white'],'ERROR','File not found!')
    
def _getCurrentTime():
    """Returns the current time formatted."""
    now = datetime.now()
    curr_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return curr_time

def _getRandomUserAgent(path):
    """Returns a random user agent."""
    useragents = _readFile(path,'r')
    return choice(useragents)

def _getRandomProxy(use_proxy, proxy_type,path):
    """Returns random proxy dict with proxy type check."""
    proxies = {}
    if use_proxy == 1:
        proxies_file = _readFile(path, 'r')
        random_proxy = choice(proxies_file)
        if proxy_type == 1:
            proxies = {
                "http": "http://{0}".format(random_proxy),
                "https": "https://{0}".format(random_proxy)
            }
        elif proxy_type == 2:
            proxies = {
                "http": "socks4://{0}".format(random_proxy),
                "https": "socks4://{0}".format(random_proxy)
            }
        else:
            proxies = {
                "http": "socks5://{0}".format(random_proxy),
                "https": "socks5://{0}".format(random_proxy)
            }
    else:
        proxies = {
            "http": None,
            "https": None
        }
    return proxies