#!/bin/bash

# =============================================================================
# OpenGewe 全栈开发环境一键启动脚本
#
# 功能:
# 1. 检查核心依赖 (node, npm, python)。
# 2. 从 main_config.toml 读取后端端口，并提供默认值。
# 3. 启动前检查并终止占用端口的旧进程。
# 4. 提供 --install / -i 标志来安装前后端依赖。
# 5. 并发启动前端和后端服务。
# 6. 将日志合并输出，并添加 [FRONTEND] / [BACKEND] 前缀。
# 7. 捕获 Ctrl+C 信号，确保所有子进程被优雅终止。
#
# 使用方法:
#   - 首次运行或更新依赖: ./start.sh --install
#   - 常规启动: ./start.sh
#
# 作者: wangnov
# =============================================================================

# --- 配置 ---
FRONTEND_DIR="frontend"
BACKEND_DIR="backend"
CONFIG_FILE="main_config.toml"

# 默认端口 (如果配置文件中找不到)
FRONTEND_PORT_DEFAULT=5173
BACKEND_PORT_DEFAULT=5432

# --- 颜色定义 ---
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
COLOR_NC='\033[0m' # No Color

# --- 函数定义 ---

# 打印带颜色的信息
info() {
    # 将信息输出到 stderr，避免被命令替换捕获
    echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1" >&2
}

warn() {
    # 将警告输出到 stderr
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_NC} $1" >&2
}

error() {
    # 将错误输出到 stderr
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1" >&2
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error "命令 '$1' 未找到。请安装它并确保它在您的 PATH 中。"
        exit 1
    fi
}

# 从 TOML 文件中提取值
# 使用简单的 grep 和 sed，避免需要安装额外的 toml 解析工具
get_port_from_config() {
    local file="$1"
    local default_port="$2"

    if [ ! -f "$file" ]; then
        warn "配置文件 '$file' 未找到，将使用默认端口 $default_port。"
        echo "$default_port"
        return
    fi

    # 查找 [webpanel] 部分下的 port
    local port_line=$(sed -n '/\[webpanel\]/,/\[/p' "$file" | grep "port\s*=")
    
    if [[ -n "$port_line" ]]; then
        local port=$(echo "$port_line" | sed 's/.*=\s*//' | tr -d '[:space:]"')
        if [[ "$port" =~ ^[0-9]+$ ]]; then
            info "从 '$file' 中找到后端端口: $port"
            echo "$port"
            return
        fi
    fi

    warn "在 '$file' 中未找到有效的后端端口配置，将使用默认端口 $default_port。"
    echo "$default_port"
}

# 检查并终止占用指定端口的进程
kill_process_on_port() {
    local port="$1"
    info "正在检查端口 $port..."
    # 使用 lsof 命令查找占用端口的进程ID
    # -t: 只输出PID, -i: 网络连接
    local pid=$(lsof -t -i:$port)

    if [ -n "$pid" ]; then
        warn "端口 $port 已被进程 PID(s): $pid 占用。正在终止这些进程..."
        # 使用 xargs 逐个终止所有找到的PID
        echo "$pid" | xargs kill -9
        if [ $? -eq 0 ]; then
            info "占用端口 $port 的进程已成功终止。"
        else
            error "终止占用端口 $port 的部分或全部进程失败。请手动检查并终止它们。"
            # 即使终止失败，也尝试继续，而不是直接退出
        fi
    else
        info "端口 $port 未被占用。"
    fi
}

# 清理函数，用于终止所有子进程
cleanup() {
    info "\n接收到退出信号... 开始清理子进程..."
    # 获取所有后台作业的PID
    pids_to_kill=$(jobs -p)
    if [ -n "$pids_to_kill" ]; then
        # 向所有子进程发送SIGTERM信号，允许它们优雅地关闭
        kill $pids_to_kill
        info "已向子进程 ($pids_to_kill) 发送终止信号，等待它们退出..."
        # 等待所有后台作业完成，这是关键步骤
        wait
        info "所有子进程已成功终止。"
    else
        info "没有活动的子进程需要清理。"
    fi
    exit 0
}

# --- 主逻辑 ---

# 捕获退出信号 (Ctrl+C)
trap cleanup SIGINT SIGTERM

# 1. 解析命令行参数
INSTALL_DEPS=false
if [[ "$1" == "--install" || "$1" == "-i" ]]; then
    INSTALL_DEPS=true
    info "检测到 '--install' 标志，将执行依赖安装。"
fi

# 2. 环境检查
info "开始环境检查..."
check_command "node"
check_command "npm"
check_command "python"
info "核心工具检查通过。"

# 3. 获取端口配置
FRONTEND_PORT=$FRONTEND_PORT_DEFAULT
BACKEND_PORT=$(get_port_from_config "$CONFIG_FILE" "$BACKEND_PORT_DEFAULT")

# 4. 端口检查与清理
kill_process_on_port "$FRONTEND_PORT"
kill_process_on_port "$BACKEND_PORT"

# 5. 启动服务
info "准备并发启动前端和后端服务..."

# 启动后端
(
    cd "$BACKEND_DIR" || exit 1
    if [ "$INSTALL_DEPS" = true ]; then
        info "[BACKEND] 正在安装 Python 依赖..."
        if python -m pip install -r requirements.txt; then
            info "[BACKEND] Python 依赖安装成功。"
        else
            error "[BACKEND] Python 依赖安装失败。"
            exit 1
        fi
    fi
    info "[BACKEND] 正在启动 FastAPI 服务..."
    # 使用 uvicorn 启动，并添加 --reload 以支持热重载
    python -m uvicorn main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload
) | sed -e "s/^/${COLOR_GREEN}[BACKEND]${COLOR_NC} /" &

# 启动前端
(
    cd "$FRONTEND_DIR" || exit 1
    if [ "$INSTALL_DEPS" = true ]; then
        info "[FRONTEND] 正在安装 Node.js 依赖..."
        if npm install; then
            info "[FRONTEND] Node.js 依赖安装成功。"
        else
            error "[FRONTEND] Node.js 依赖安装失败。"
            exit 1
        fi
    fi
    info "[FRONTEND] 正在启动 Vite 开发服务器..."
    # 使用 npm run dev 启动，Vite会自动监听文件变化
    npm run dev -- --port "$FRONTEND_PORT"
) | sed -e "s/^/${COLOR_YELLOW}[FRONTEND]${COLOR_NC} /" &

# 等待所有后台任务完成
# 这使得脚本会一直运行，直到用户按下 Ctrl+C
wait