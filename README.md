# Bing-Wallpaper for Python3

## 使用说明

* 该脚本缺省将图片下载到当前用户/Users/xxx/Wallpapers中，可在config.js中进行修改。
* 在桌面背景设置里指向该文件夹，并允许自动更换，如每5分钟一次等。

##
每日一言 http://guozhivip.com/nav/api/api.php
每日一句 http://guozhivip.com/


https://github.com/julienXX/terminal-notifier

## 自动执行配置 crontab
mac
crontab -e

min hour mday month wday command  
* */4 * * * /usr/local/bin/python3 ~/path/to/bing-wallpaper/app.py

## 遗留问题
* com.apple.desktop.admin.png 更改失败，暂不能自动替换mac的登录背景。

