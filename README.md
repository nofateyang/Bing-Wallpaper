# Bing-Wallpaper for Python3

## 使用说明

* 该脚本缺省将图片下载到当前用户/Users/xxx/Wallpapers中，可在config.js中进行修改。
* 在桌面背景设置里指向该文件夹，并允许自动更换，如每5分钟一次等。


## 自动执行配置 crontab

min hour mday month wday command  
20 9,12,15,19,22 * * * /usr/local/bin/node ~/path/to/bingwallpaper/app.js

## 遗留问题
* com.apple.desktop.admin.png 更改失败，暂不能自动替换mac的登录背景。

