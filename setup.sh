#!/bin/bash
# desc:安装脚本

# 检验是否安装docker
function checkVersion() {
    docker -version >/dev/null 2>&1
    if [ echo $? -gt 0 ];then
      echo "未检测到docker,是否安装docker"
    fi
}

# 格式化配置
function parseConfig() {
    pwd=$(pwd)
    port=read "选择程序运行端口(默认:8080)"
}

# 初始化数据库
function initDatabase() {
    sqlite3 init.sql
}

# 帮助函数
function help() {
    echo "安装程序:sh setup.sh install"
    echo "启动程序:sh setup.sh start"
    echo "停止程序:sh setup.sh stop"
    echo "重启程序:sh setup.sh restart"
}

# 主函数
function main() {
    case "$1" in
      "install")  # 安装程序
        ;;
      "start")  # 启动程序
        ;;
      "stop")  # 停止程序
        ;;
      "restart")  # 重启程序
        ;;
      *)
        help
        ;;
    esac
}

main $1
