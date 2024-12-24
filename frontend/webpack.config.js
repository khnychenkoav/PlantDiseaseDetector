const path = require('path');

module.exports = {
    entry: './src/App.js',
    output: {
        path: path.resolve(__dirname, 'public'),
        filename: 'bundle.js',
    },
    devServer: {
        contentBase: path.join(__dirname, 'public'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: 'babel-loader',
            },
        ],
    },
};
