#!/bin/bash
# 后端服务启动脚本

# 切换到项目根目录
cd "$(dirname "$0")"

# 激活虚拟环境（如果存在）
if [ -d ".venv" ]; then
  echo "激活虚拟环境..."
  source .venv/bin/activate
fi

# 确保必要的目录存在
mkdir -p logs
mkdir -p static/uploads

# 检查配置文件
if [ ! -f "main_config.toml" ]; then
  echo "错误: main_config.toml 不存在"
  
  if [ -f "main_config_example.toml" ]; then
    echo "复制示例配置文件..."
    cp main_config_example.toml main_config.toml
    echo "请编辑 main_config.toml 文件，然后重新运行此脚本"
    exit 1
  else
    echo "错误: 示例配置文件也不存在"
    exit 1
  fi
fi

# 检查端口是否被占用
PORT=$(grep -A 10 '\[backend\]' main_config.toml | grep 'port' | sed 's/.*= *\([0-9]*\).*/\1/')
if [ -z "$PORT" ]; then
  PORT=5433  # 默认端口
  echo "警告: 未能从配置文件获取端口，使用默认端口 $PORT"
fi

echo "检查端口 $PORT 是否被占用..."
if command -v lsof >/dev/null 2>&1; then
  PORT_USAGE=$(lsof -i:$PORT -P -n)
  if [ ! -z "$PORT_USAGE" ]; then
    echo "警告: 端口 $PORT 已被占用:"
    echo "$PORT_USAGE"
    echo "尝试停止已存在的服务..."
    
    # 尝试找到并终止已有进程
    PID=$(lsof -i:$PORT -t)
    if [ ! -z "$PID" ]; then
      echo "终止进程 $PID..."
      kill $PID
      sleep 2
      
      # 检查是否仍在运行
      if ps -p $PID > /dev/null; then
        echo "警告: 无法停止进程，尝试强制终止..."
        kill -9 $PID
        sleep 1
      fi
    fi
  else
    echo "端口 $PORT 可用"
  fi
else
  echo "警告: lsof 命令不可用，无法检查端口占用情况"
fi

# 设置环境变量
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# 打印启动信息
echo "=================================="
echo "启动 OpenGewe 后端服务..."
echo "使用配置文件: $(pwd)/main_config.toml"
echo "使用端口: $PORT"
echo "=================================="

# 启动后端服务
python -m backend.app.main

# 如果服务异常退出，打印错误信息
if [ $? -ne 0 ]; then
  echo "后端服务异常退出，请检查日志文件获取更多信息"
  exit 1
fi 