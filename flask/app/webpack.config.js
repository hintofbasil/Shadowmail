var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');

module.exports = {
    context: __dirname,
    devtool: debug ? "inline-sourcemap" : false,
    entry: "./js/index.js",
    output: {
      path: __dirname + "/static/js",
      filename: "bundle.js"
    },
  };
