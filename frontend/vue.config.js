module.exports = {
    // 開發環境中使用的端口
    devServer: {
    port: 8001
    },
    // 取消生成map文件（map文件可以準確的輸出是哪一行哪一列有錯）
    productionSourceMap: false,
    // 開發環境和部署環境的路徑
    publicPath: process.env.NODE_ENV === 'production'
    ? '/'
    : '/my/',
    configureWebpack: (config) => {
    // 增加 iview-loader
    config.module.rules[0].use.push({
    loader: 'iview-loader',
    options: {
    prefix: false
    }
    })
    // 在命令行使用 vue inspect > o.js 可以檢查修改後的webpack配置文件
    }
    }