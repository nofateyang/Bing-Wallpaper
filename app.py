"""
[summary]
"""

import os
import platform
import requests
import textwrap

from urllib import parse
from bs4 import BeautifulSoup
from easydict import EasyDict as edict

# from hobee import RequestX as Request

from PIL import Image, ImageFont, ImageDraw


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


logs = []
log_file = local_root + '/bing-wallpaper.txt'


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
        cmd = "osascript -e 'display notification \"" + filename + "\r\n" + title + \
            "\" with title \"Bing-Wallpaper " + "\" sound name \"Glass.aiff\" '"
    else:
        cmd = None
    # debug_print(cmd)
    if cmd is not None:
        execute_command(cmd)
    return 0


def draw_text_info_to_image(image_file_name, image_info):
    
    words = []
    
    # 每日一言
    url = 'http://guozhivip.com/nav/api/api.php'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200 and len(resp.content) > 0:
        result = resp.content.decode('utf-8')
        result = result.replace('document.write("', '').replace('");', '') 
        if len(result) > 0:
            words.append(result) 
    
    # 每日一句
    url = 'http://guozhivip.com/'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200 and len(resp.content) > 0:
        result = resp.content.decode('utf-8')
        # debug_print(result)
        soup = BeautifulSoup(result, "html.parser")
        result = soup.select('body > div.contents > section.com.one > div.sub.content > ul > li.words > h3')
        if result is not None and len(result) > 0:
            # debug_print(str(result[0]))
            result = str(result[0]).replace('<h3>', '').replace('</h3>', '') # 这里没有办法，因为需要用到<br/>来分行
            results = result.split('<br/>')
            for text in results:
                words.append(text.strip())
            
        result = soup.select('body > div.contents > section.com.one > div.sub.content > ul > li.words > p')
        if result is not None and len(result) > 0:
            result = result[0].text.replace('果汁小编：', '')
            words.append(result)
            # debug_print(result)
    
    logs.extend(words)
    debug_print('======================================')
    
    im = Image.open(image_file_name)
    print(im.format, im.size, im.mode)

    iw, ih = im.size[0], im.size[1]
    
    x = 220
    y = 20
   
    draw = ImageDraw.Draw(im) 
   
    y = ih - 350
    t_height = 0
    font = ImageFont.truetype("font/SourceHanSansSC-Regular.otf", 24)
    for index,text in enumerate(words):
        w, h = font.getsize(text)
        t_height = t_height + h
    
    w_h = t_height / len(words) 
    for index,text in enumerate(words):
        y = y + w_h + 0
        debug_print(text + ' %d, %d ' % (w, h))
        draw.text((x, y), text, fill=(255, 255, 255),  font=font)
    
    y = y + 10
    text_info = image_info.copyright.split('，')
    font = ImageFont.truetype("font/SourceHanSansSC-Regular.otf", 30)
    for index, text in enumerate(text_info):
        w, h = font.getsize(text)
        debug_print(text + ' %d, %d ' % (w, h))
        y = y + h
        draw.text((x, y), text, fill=(255, 255, 255),  font=font)
    im.save(image_file_name)

    return 0


def fetch():
    # request = Request(headers=headers)
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return -1

    # debug_print(resp.json())
    result = edict(resp.json())
    # debug_print(result)

    for image in result.images:
        image_url = parse.unquote(image.url)
        parsed_tuple = parse.urlparse(image_url)
        query_dict = edict(parse.parse_qs(parsed_tuple.query))
        filename = image.startdate + '.jpg'  # + query_dict.rf[0]
        l_filename = local_root + '/' + filename
        
        logs.append(filename)
        logs.append(root + image.url)
        logs.append(image.copyright)
        
        # debug_print(filename)
        if not os.path.exists(l_filename):
            resp = requests.get(root + image.url)
            if resp.status_code == 200:
                with open(l_filename, 'wb') as f:
                    f.write(resp.content)
                    f.flush()
                    f.close()
                draw_text_info_to_image(l_filename, image)
                notify(filename, image.copyright)
                
                log_text = '\r\n'.join(logs)
                write_log(log_text)

            else:
                pass
        else:
            pass
    
    
    # debug_print(log_text)
    return 0


def do_action(argsDict=None):
    fetch()
    pass


if __name__ == "__main__":
    do_action()

# end
