"""
[summary]
"""
import os
import platform
import requests
from urllib import parse

from easydict import EasyDict as edict
# from hobee import RequestX as Request

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8;',
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
}

root = 'http://www.bing.com'
url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'

local_root = '/Users/ayang/Wallpapers'
if platform.system().lower() == 'windows':
    local_root = os.environ['HOMEPATH'] + '/Wallpapers'
else:
    local_root = os.environ['HOME'] + '/Wallpapers'


log_file = local_root + '/bing-wallpaper.log'

def debug_print(message):
    return print(message, flush=True)

def execute_command(cmd, newshell=True):
    import subprocess
    p = subprocess.Popen(cmd,
                         shell=newshell,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode, stderr
    return p.returncode, stdout

def write_log(string):
    data = ''
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
    data = string + '\r\n' + '\r\n' + data
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(data)
        f.flush()
        f.close()
        
    return 0
    

def notify(filename, title):
    cmd = None
    if platform.system().lower() == 'darwin':
        cmd = "osascript -e 'display notification \"" + filename + "\r\n" +  title + "\" with title \"Bing-Wallpaper "  + "\" sound name \"Glass.aiff\" '"    
    else:
        cmd = None
    # debug_print(cmd)
    if cmd is not None:
        execute_command(cmd)
    return 0


def fetch():
    # request = Request(headers=headers)
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return -1
    
    # debug_print(resp.json())
    result = edict(resp.json())
    # print(resp.json, flush=False)
    
    for image in result.images:
        image_url = parse.unquote(image.url)
        parsed_tuple = parse.urlparse(image_url)        
        query_dict = edict(parse.parse_qs(parsed_tuple.query))
        filename = image.startdate + '-' + query_dict.rf[0]
        # debug_print(filename)
        if not os.path.exists(local_root + '/' + filename):
            resp = requests.get(root + image.url)
            if resp.status_code == 200:
                with open(local_root + '/' + filename, 'wb') as f:
                    f.write(resp.content)
                    f.flush()
                    f.close()
                logs = '\r\n'.join([filename, root + image.url, image.copyright])
                debug_print(logs)
                write_log(logs)
                notify(filename, image.copyright)
            else:
                pass
        else:
            pass
        
    return 0


def do_action(argsDict=None):
    fetch()
    pass

if __name__ == "__main__":
    do_action()
