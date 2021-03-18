const path = require("path")
// const MiniCssExtractPlugin = require('mini-css-extract-plugin')

function resolve(dir) {
    return path.join(__dirname, dir)
}

module.exports = {
    publicPath: "/",
    outputDir: "dist",
    assetsDir: "static",
    lintOnSave: process.env.NODE_ENV === "development",
    productionSourceMap: false,
    devServer: {
        disableHostCheck: true,
        proxy: {
            "/api": {
                target: "http://localhost:8000",
                changOrigin: true,
            }
        }
    },
    configureWebpack: {
        name: "Token招新系统",
        resolve: {
            alias: {
            "@": resolve("src")
            }
        },
        devtool: "source-map",
        // plugins: [
        //     new MiniCssExtractPlugin({})
        // ],
        // module: {
        //     rules: [
        //         {
        //             test: /\.css$/,
        //             use: [{
        //                 loader: MiniCssExtractPlugin.loader
        //             }]
        //         }
        //     ]
        // }

    },
    chainWebpack(config) {
    config.plugin("preload").tap(() => [
        {
            rel: "preload",
            fileBlacklist: [/\.map$/, /hot-update\.js$/, /runtime\..*\.js$/],
            include: "initial"
        }
    ])

    config.plugins.delete("prefetch")

    }
}