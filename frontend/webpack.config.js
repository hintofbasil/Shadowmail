var path = require("path");
var webpack = require("webpack");
var HtmlWebpackPlugin = require("html-webpack-plugin");
const PrerenderSPAPlugin = require("prerender-spa-plugin");
const Renderer = PrerenderSPAPlugin.PuppeteerRenderer;
const VueLoaderPlugin = require("vue-loader/lib/plugin");

module.exports = {
  mode: process.env.NODE_ENV,
  entry: "./src/main.js",
  output: {
    path: path.resolve(__dirname, "./dist"),
    publicPath: "/",
    filename: "build.js"
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader"
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: "file-loader",
        options: {
          name: "[name].[ext]?[hash]"
        }
      },
      {
        test: /\.scss$/,
        use: ["vue-style-loader", "css-loader", "sass-loader"]
      }
    ]
  },
  resolve: {
    alias: {
      "@": path.join(__dirname, "src/")
    }
  },
  devServer: {
    historyApiFallback: true,
    noInfo: false
  },
  devtool: "#eval-source-map",
  plugins: [new VueLoaderPlugin()]
};
if (process.env.NODE_ENV === "production") {
  module.exports.devtool = "#source-map";
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: '"production"'
      }
    }),
    new HtmlWebpackPlugin({
      title: "PRODUCTION prerender-spa-plugin",
      template: "public/index.html",
      filename: path.resolve(__dirname, "dist/index.html"),
      favicon: "public/favicon.png"
    }),
    new PrerenderSPAPlugin({
      staticDir: path.join(__dirname, "dist"),
      routes: ["/", "/delete", "/request_delete"],

      renderer: new Renderer({
        // inject: {
        //   foo: 'bar'
        // },
        headless: true,
        // renderAfterElementExists: '#app'
        renderAfterTime: 5000
      })
    })
  ]);
} else {
  // NODE_ENV === 'development'
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: '"development"'
      }
    }),
    new HtmlWebpackPlugin({
      title: "DEVELOPMENT prerender-spa-plugin",
      template: "index.html",
      filename: "index.html",
      favicon: "favicon.png"
    })
  ]);
}
