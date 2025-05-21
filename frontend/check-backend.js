#!/usr/bin/env node
/**
 * 检查后端服务是否正常运行的脚本
 * 
 * 用于在前端启动前检查后端服务状态
 */

import http from 'http';
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';

// 获取当前文件的目录
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 默认配置
const DEFAULT_BACKEND_PORT = 5433;
const HEALTH_ENDPOINT = '/health';
const CHECK_INIT_ENDPOINT = '/api/admin/check-init'; // 添加初始化检查
const MAX_RETRIES = 3; // 减少重试次数
const INITIAL_RETRY_INTERVAL = 2000; // 初始重试间隔2秒

// 计算退避间隔
function getBackoffInterval(retryCount) {
    return Math.min(INITIAL_RETRY_INTERVAL * Math.pow(2, retryCount), 10000); // 最大10秒
}

// 读取配置文件中的端口
function getBackendPortFromConfig() {
    try {
        // 尝试读取项目根目录的main_config.toml文件
        const configPath = path.join(__dirname, '..', 'main_config.toml');
        if (fs.existsSync(configPath)) {
            const configContent = fs.readFileSync(configPath, 'utf8');

            // 使用正则表达式查找端口配置
            const portMatch = configContent.match(/\[backend\][\s\S]*?port\s*=\s*(\d+)/);
            if (portMatch && portMatch[1]) {
                return parseInt(portMatch[1], 10);
            }
        }
        return DEFAULT_BACKEND_PORT;
    } catch (error) {
        console.warn(`读取配置文件失败: ${error.message}`);
        return DEFAULT_BACKEND_PORT;
    }
}

// 检查后端健康状态
function checkBackendHealth(port, endpoint, retryCount = 0) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'localhost',
            port: port,
            path: endpoint,
            method: 'GET',
            timeout: 5000, // 5秒超时
        };

        console.log(`正在检查后端服务 (http://localhost:${port}${endpoint})...`);

        const req = http.request(options, (res) => {
            if (res.statusCode === 200) {
                let data = '';
                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    try {
                        const response = JSON.parse(data);
                        resolve({
                            status: response.status || response.code === 0 ? 'ok' : 'error',
                            data: response
                        });
                    } catch (error) {
                        resolve({ status: 'ok', raw: data });
                    }
                });
            } else {
                if (retryCount < MAX_RETRIES) {
                    const interval = getBackoffInterval(retryCount);
                    console.log(`服务器返回状态码 ${res.statusCode}，${retryCount + 1}/${MAX_RETRIES} 次重试中... (等待 ${interval / 1000} 秒)`);
                    setTimeout(() => {
                        checkBackendHealth(port, endpoint, retryCount + 1)
                            .then(resolve)
                            .catch(reject);
                    }, interval);
                } else {
                    reject(new Error(`服务器返回状态码 ${res.statusCode}`));
                }
            }
        });

        req.on('error', (error) => {
            if (retryCount < MAX_RETRIES) {
                const interval = getBackoffInterval(retryCount);
                console.log(`连接失败: ${error.message}，${retryCount + 1}/${MAX_RETRIES} 次重试中... (等待 ${interval / 1000} 秒)`);
                setTimeout(() => {
                    checkBackendHealth(port, endpoint, retryCount + 1)
                        .then(resolve)
                        .catch(reject);
                }, interval);
            } else {
                reject(error);
            }
        });

        req.on('timeout', () => {
            req.destroy();
            if (retryCount < MAX_RETRIES) {
                const interval = getBackoffInterval(retryCount);
                console.log(`连接超时，${retryCount + 1}/${MAX_RETRIES} 次重试中... (等待 ${interval / 1000} 秒)`);
                setTimeout(() => {
                    checkBackendHealth(port, endpoint, retryCount + 1)
                        .then(resolve)
                        .catch(reject);
                }, interval);
            } else {
                reject(new Error('请求超时'));
            }
        });

        req.end();
    });
}

// 尝试启动后端服务
function startBackendService() {
    return new Promise((resolve, reject) => {
        console.log('尝试启动后端服务...');

        // 执行启动脚本
        const startScript = path.join(__dirname, '..', 'start_backend.sh');
        const child = exec(`bash ${startScript}`, { detached: true });

        // 分离子进程，让它在后台运行
        child.unref();

        console.log('后端服务启动中，请稍候...');
        setTimeout(() => {
            resolve();
        }, 5000); // 等待5秒
    });
}

// 主函数
async function main() {
    const port = getBackendPortFromConfig();
    console.log(`╔════════════════════════════════════════════╗`);
    console.log(`║      OpenGewe 前端后端连接检查工具         ║`);
    console.log(`╚════════════════════════════════════════════╝`);
    console.log(`➤ 使用端口: ${port}`);

    try {
        // 先检查健康状态
        const health = await checkBackendHealth(port, HEALTH_ENDPOINT);
        console.log('✅ 后端服务运行正常!');
        console.log(`➤ 状态: ${health.status}`);

        if (health.data && health.data.version) {
            console.log(`➤ 版本: ${health.data.version}`);
        }

        if (health.data && health.data.components) {
            console.log('➤ 组件状态:');
            Object.entries(health.data.components).forEach(([name, status]) => {
                const icon = status === 'ok' ? '✓' : '✗';
                console.log(`  ${icon} ${name}: ${status}`);
            });
        }

        // 检查初始化状态
        try {
            console.log(`正在检查管理员初始化状态...`);
            const initCheck = await checkBackendHealth(port, CHECK_INIT_ENDPOINT);
            if (initCheck.status === 'ok') {
                console.log('✅ 管理员账户检查成功!');
                if (initCheck.data && initCheck.data.data && initCheck.data.data.initialized) {
                    console.log(`➤ 管理员账户状态: 已初始化`);
                } else {
                    console.log(`➤ 管理员账户状态: 未初始化`);
                }
            } else {
                console.warn('⚠️ 管理员账户检查失败，但不影响前端启动');
            }
        } catch (initError) {
            console.warn('⚠️ 检查管理员初始化状态失败，但不影响前端启动');
            console.warn(`  错误信息: ${initError.message}`);
        }

        process.exit(0);
    } catch (error) {
        console.error(`❌ 后端服务检查失败: ${error.message}`);
        console.error('➤ 请确保后端服务已启动，或使用 ./start_backend.sh 启动后端');

        // 询问是否尝试自动启动后端
        console.log('尝试自动启动后端服务...');
        try {
            await startBackendService();
            console.log('已尝试启动后端服务，请等待几秒钟后再尝试启动前端');
        } catch (startError) {
            console.error(`启动后端服务失败: ${startError.message}`);
        }

        process.exit(1);
    }
}

// 执行主函数
main(); 