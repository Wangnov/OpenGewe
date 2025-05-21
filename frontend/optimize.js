#!/usr/bin/env node
/**
 * 前端依赖预构建优化脚本
 * 
 * 此脚本清理Vite缓存并执行依赖预构建，
 * 解决大量chunk请求导致页面加载慢的问题
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

// 获取当前文件的目录
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('╔════════════════════════════════════════════╗');
console.log('║      OpenGewe 前端依赖预构建优化工具       ║');
console.log('╚════════════════════════════════════════════╝');

// 检查依赖兼容性
console.log('➤ 检查依赖兼容性...');
try {
    // 检查package.json
    const packageJsonPath = path.join(__dirname, 'package.json');
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

    const reactVersion = packageJson.dependencies.react;
    console.log(`✓ React版本: ${reactVersion}`);

    // 检查是否有React 19兼容性问题
    if (reactVersion.startsWith('19.')) {
        console.log('⚠️ 检测到使用React 19，确保vite.config.ts中已配置正确的JSX运行时');

        // 检查vite.config.ts
        const viteConfigPath = path.join(__dirname, 'vite.config.ts');
        const viteConfig = fs.readFileSync(viteConfigPath, 'utf8');

        if (!viteConfig.includes('jsxRuntime') || !viteConfig.includes('jsxImportSource')) {
            console.warn('❌ vite.config.ts可能缺少React 19所需的JSX运行时配置');
            console.warn('   请确保在react()插件中添加了jsxRuntime和jsxImportSource配置');
        } else {
            console.log('✓ vite.config.ts已包含React 19所需的JSX运行时配置');
        }
    }
} catch (error) {
    console.error(`❌ 检查依赖兼容性失败: ${error.message}`);
}

// 清理.vite缓存目录
console.log('➤ 清理 .vite 缓存目录...');
try {
    const viteCachePath = path.join(__dirname, 'node_modules', '.vite');
    if (fs.existsSync(viteCachePath)) {
        fs.rmSync(viteCachePath, { recursive: true, force: true });
    }
    console.log('✅ .vite 缓存目录已清理');
} catch (error) {
    console.error(`❌ 清理缓存目录失败: ${error.message}`);
}

// 清理可能已损坏的node_modules
console.log('➤ 检查node_modules完整性...');
try {
    // 检查关键依赖是否存在
    const criticalDependencies = ['react', 'react-dom', '@vitejs/plugin-react'];
    const missingDeps = criticalDependencies.filter(dep => {
        try {
            return !fs.existsSync(path.join(__dirname, 'node_modules', dep));
        } catch {
            return true;
        }
    });

    if (missingDeps.length > 0) {
        console.warn(`⚠️ 发现缺失的关键依赖: ${missingDeps.join(', ')}`);
        console.log('➤ 尝试修复node_modules...');

        execSync('npm install --no-save', { stdio: 'inherit' });
        console.log('✅ 依赖修复完成');
    } else {
        console.log('✓ node_modules完整性检查通过');
    }
} catch (error) {
    console.error(`❌ 检查node_modules完整性失败: ${error.message}`);
}

// 执行Vite依赖预构建
console.log('➤ 执行 Vite 依赖预构建...');
console.log('   这可能需要几分钟，请耐心等待...');

try {
    // 使用Vite优化命令
    execSync('npx vite optimize', { stdio: 'inherit' });
    console.log('✅ 依赖预构建完成');
    process.exit(0);
} catch (error) {
    console.error(`❌ 预构建命令执行失败，退出码: ${error.status || 1}`);
    process.exit(1);
} 