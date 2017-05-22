//http://stackoverflow.com/questions/10639914/is-there-a-way-to-get-bings-photo-of-the-day

const os = require('os');
var process = require('process')
var request = require('request');
var fs = require('fs');
var path = require('path');
var config = require('./config.js');

const logfile = "bing-wallpaper.txt";
const platform = os.platform();

// 将图片说明信息写在文件的最前面，方便查看。
function write_log(message) {
    var notes = path.join(config.path.pictures, logfile);
    if (fs.existsSync(notes)) {
        fs.readFile(notes, 'utf8', (err, data) => {
            if (err) throw err;
            fs.writeFile(notes, message + '\r\n\r\n' + data, 'utf8');
        });
    } else {
        fs.writeFile(notes, message + '\r\n', 'utf8');
    }
}

function execute_command(cmd) {
    var exec = require('child_process').execSync;
    // console.log("execute_command:" + cmd)
    exec(cmd, function(error, stdout, stderr) {
        // console.error(error);
        // console.log(stdout);
        // console.error(stderr);
    });
}

function show_notification(filename, title) {
    // osascript -e 'display notification "为了你的健康! " with title "快站会儿" sound name "Glass.aiff" '
    var cmd = "";
    if (platform === "win32") {
        cmd = ""; // 暂不支持。
    } else if (platform === "darwin") {
        cmd = "osascript -e 'display notification \"" + title + "\" with title \"Bing-Wallpaper: " + filename + "\" sound name \"Glass.aiff\" '";
    } else if (platform === "linux") {
        cmd = "";
    }

    if (cmd.length > 0) {
        execute_command(cmd)
    }
}

function update_login_background(imgFileName) {
    var lock = true;
    var fn = "/Library/Caches/com.apple.desktop.admin.png"
    if (fs.existsSync(fn)) {
        if (lock) {
            execute_command("Chflags nouchg " + fn);
        }
        fs.unlinkSync(fn);
    }
    var cmd = "sips -s format png '" + imgFileName + "' --out " + fn;
    cmd = cmd + " && xattr -w com.apple.quarantine 22 " + fn;
    if (lock) {
        cmd = cmd + " && Chflags uchg " + fn;
    }

    execute_command(cmd);

    // 初始属性: com.apple.quarantine: 0082;5923237f;Preview;
    // xattr -w 属性名 属性值 文件名
    // xattr -w com.apple.quarantine 22 com.apple.desktop.admin.png
}

function fetch() {
    var root = 'http://www.bing.com';
    var uri = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1';

    request(uri, function(error, response, body) {
        if (!error && response.statusCode == 200) {
            try {
                var data = JSON.parse(body);
                var images = data.images;

                images.forEach(function(image) {
                    var ext = path.extname(image.url);
                    var name = image.fullstartdate + ext;
                    var imgFileName = path.join(config.path.pictures, name);
                    var data = [
                        image.fullstartdate + ext,
                        root + image.url,
                        image.copyright,
                        ' '
                    ].join("\r\n");

                    if (!fs.existsSync(imgFileName)) {
                        request(root + image.url).pipe(fs.createWriteStream(imgFileName)).on('finish', function() {
                            write_log(data);
                            update_login_background(imgFileName);
                            show_notification(name, image.copyright);
                        });
                    } else {
                        console.error('already exists');
                    }
                });
            } catch (e) {
                console.error(e);
                write_log(e);
            }
        }
    });
}

// console.log(`Current gid: ${process.getegid()}`);
// console.log(`Current uid: ${process.geteuid()}`);
// console.log(`Current gid: ${process.getgid()}`);

fetch();