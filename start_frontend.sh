#!/bin/bash
# 前端服务启动脚本

# 切换到项目根目录
cd "$(dirname "$0")"

# 进入前端目录
cd frontend

# 检查是否安装了依赖
if [ ! -d "node_modules" ]; then
  echo "正在安装前端依赖..."
  npm install
  
  if [ $? -ne 0 ]; then
    echo "依赖安装失败，请手动运行 npm install"
    exit 1
  fi
fi

# 检查后端服务是否正常运行
echo "检查后端服务状态..."
npm run check-backend

# 如果后端检查失败，询问是否继续
if [ $? -ne 0 ]; then
  echo "后端服务检查失败"
  read -p "是否仍然继续启动前端服务? (y/n): " continue_frontend
  if [ "$continue_frontend" != "y" ]; then
    echo "已取消前端服务启动"
    exit 1
  fi
  echo "警告: 虽然后端服务可能未正常运行，但将继续启动前端服务"
fi

# 执行依赖优化
echo "正在执行依赖预构建优化..."
npm run optimize

# 打印启动信息
echo "=================================="
echo "启动 OpenGewe 前端服务..."
echo "前端地址: http://localhost:5432"
echo "=================================="

# 使用开发模式启动前端服务
npm run dev

# 如果服务异常退出，打印错误信息
if [ $? -ne 0 ]; then
  echo "前端服务异常退出，请检查日志获取更多信息"
  exit 1
fi 