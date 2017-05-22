var path = require('path');

module.exports = {
    path: {
        // pictures: path.resolve(__dirname, '/Users/ayang/Wallpapers'),
        pictures: path.join(process.env.HOME, "Wallpapers")
    }
};