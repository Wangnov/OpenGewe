import React, { useState, useEffect, useCallback } from 'react';
import ReactDOM from 'react-dom';
import pluginService from '../services/pluginService';
import useApiLoading from '../hooks/useApiLoading';
import useNotification from '../hooks/useNotification';
import LoadingSpinner from '../components/common/LoadingSpinner';
import Modal from '../components/common/Modal';
import ReactMarkdown from 'react-markdown';
import 'github-markdown-css/github-markdown.css';

// --- 主组件 ---

const Plugins = () => {
    const [plugins, setPlugins] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showReadmeModal, setShowReadmeModal] = useState(null);
    const [showConfigModal, setShowConfigModal] = useState(null);
    const { executeWithLoading } = useApiLoading();
    const { success, error: notifyError, info, warning } = useNotification();

    const fetchPlugins = useCallback(async (isManualRefresh = false) => {
        try {
            setLoading(true);
            const response = await executeWithLoading(pluginService.getGlobalPlugins);
            const pluginData = response.data?.data || [];
            setPlugins(pluginData);
            if (isManualRefresh) {
                info('刷新成功', `共找到 ${pluginData.length} 个插件。`);
            }
        } catch (err) {
            notifyError('加载失败', '无法获取插件列表，请检查后端服务是否正常。');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [executeWithLoading, notifyError, info]);

    useEffect(() => {
        fetchPlugins();
    }, [fetchPlugins]);

    const handleToggleEnabled = async (pluginId, currentStatus) => {
        try {
            await executeWithLoading(() => pluginService.updateGlobalPluginStatus(pluginId, !currentStatus));
            setPlugins(prev =>
                prev.map(p =>
                    p.plugin_id === pluginId ? { ...p, is_globally_enabled: !currentStatus } : p
                )
            );
            success('状态已更新', `插件 ${pluginId} 已${!currentStatus ? '全局启用' : '全局禁用'}。`);
        } catch (err) {
            notifyError('操作失败', `无法更新插件 ${pluginId} 的状态。`);
            console.error(err);
        }
    };

    const handleReloadConfig = async () => {
        try {
            await executeWithLoading(pluginService.reloadPluginConfig);
            success('操作成功', '插件配置热重载任务已成功触发。');
            setTimeout(() => {
                fetchPlugins(true);
            }, 2000);
        } catch (err) {
            notifyError('操作失败', '无法触发插件配置热重载。');
            console.error(err);
        }
    };

    if (loading) {
        return <div className="flex items-center justify-center h-64"><LoadingSpinner size="lg" text="加载插件列表中..." /></div>;
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-800">插件列表</h1>
                <div className="flex items-center space-x-4">
                    <button
                        onClick={() => fetchPlugins(true)}
                        className="bg-white text-gray-700 px-4 py-2 rounded-lg shadow-sm hover:bg-gray-50 border border-gray-300 transition-colors duration-200 flex items-center"
                    >
                        <i className="fas fa-sync-alt mr-2"></i>
                        刷新列表
                    </button>
                    <button
                        onClick={handleReloadConfig}
                        className="bg-purple-600 text-white px-4 py-2 rounded-lg shadow-md hover:bg-purple-700 transition-colors duration-200 flex items-center"
                    >
                        <i className="fas fa-bolt mr-2"></i>
                        重载配置
                    </button>
                </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {plugins.map(plugin => (
                    <PluginCard
                        key={plugin.plugin_id}
                        plugin={plugin}
                        onToggleEnabled={() => handleToggleEnabled(plugin.plugin_id, plugin.is_globally_enabled)}
                        onShowReadme={() => setShowReadmeModal(plugin)}
                        onShowConfig={() => setShowConfigModal(plugin)}
                    />
                ))}
            </div>
            <ReadmeModal plugin={showReadmeModal} onClose={() => setShowReadmeModal(null)} />
            <ConfigModal
                plugin={showConfigModal}
                onClose={() => setShowConfigModal(null)}
                onSave={async (pluginId, newConfig) => {
                    try {
                        await executeWithLoading(() => pluginService.updateGlobalPluginConfig(pluginId, newConfig));
                        success('配置已保存', `插件 ${pluginId} 的配置已更新并成功热重载。`);
                        setShowConfigModal(null);
                        fetchPlugins();
                    } catch (err) {
                        if (err.response?.data?.status === 'warning') {
                            warning('部分成功', err.response.data.message);
                        } else {
                            notifyError('保存失败', `无法保存插件 ${pluginId} 的配置。`);
                        }
                        console.error(err);
                    }
                }}
            />
        </div>
    );
};

// --- 工具函数 ---

// 获取插件名称的首字母
const getInitial = (name) => {
    if (!name) return '?';
    // 尝试提取大写字母（如 "DailyQuote" -> "DQ"）
    const capitals = name.match(/[A-Z]/g);
    if (capitals && capitals.length >= 2) {
        return capitals.slice(0, 2).join('');
    }
    // 否则返回第一个字符
    return name.charAt(0).toUpperCase();
};

// 基于字符串生成一致的颜色
const generateColor = (str) => {
    if (!str) return '#6366f1'; // 默认紫色

    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    // 预定义的渐变色组合
    const gradients = [
        ['#3b82f6', '#60a5fa'], // 蓝色
        ['#8b5cf6', '#a78bfa'], // 紫色
        ['#ec4899', '#f472b6'], // 粉色
        ['#10b981', '#34d399'], // 绿色
        ['#f59e0b', '#fbbf24'], // 橙色
        ['#ef4444', '#f87171'], // 红色
        ['#06b6d4', '#22d3ee'], // 青色
        ['#6366f1', '#818cf8'], // 靛蓝色
    ];

    const index = Math.abs(hash) % gradients.length;
    return gradients[index];
};

// 获取配置项图标
const getConfigIcon = (key) => {
    const iconMap = {
        // 通用配置
        enabled: 'fas fa-power-off',
        name: 'fas fa-tag',
        description: 'fas fa-info-circle',
        version: 'fas fa-code-branch',
        author: 'fas fa-user',

        // API相关
        api_key: 'fas fa-key',
        api_url: 'fas fa-link',
        endpoint: 'fas fa-plug',
        token: 'fas fa-lock',
        secret: 'fas fa-user-secret',

        // 功能配置
        features: 'fas fa-cogs',
        settings: 'fas fa-sliders-h',
        options: 'fas fa-list-ul',
        permissions: 'fas fa-shield-alt',

        // 时间相关
        schedule: 'fas fa-clock',
        interval: 'fas fa-hourglass-half',
        timeout: 'fas fa-stopwatch',
        cron: 'fas fa-calendar-alt',

        // 数据相关
        database: 'fas fa-database',
        storage: 'fas fa-hdd',
        cache: 'fas fa-memory',

        // 通知相关
        notifications: 'fas fa-bell',
        alerts: 'fas fa-exclamation-triangle',
        messages: 'fas fa-comment',

        // 监控相关
        monitoring: 'fas fa-chart-line',
        keywords: 'fas fa-search',
        filters: 'fas fa-filter',
        rules: 'fas fa-gavel',

        // 默认图标
        default: 'fas fa-cog'
    };

    // 尝试匹配最相关的图标
    const lowerKey = key.toLowerCase();
    for (const [pattern, icon] of Object.entries(iconMap)) {
        if (lowerKey.includes(pattern)) {
            return icon;
        }
    }

    return iconMap.default;
};

// 获取配置项描述
const getConfigDescription = (key) => {
    const descriptionMap = {
        enabled: '启用或禁用此功能',
        api_key: 'API访问密钥',
        api_url: 'API服务地址',
        schedule: '定时任务配置',
        interval: '执行间隔时间',
        keywords: '关键词列表',
        notifications: '通知设置',
        permissions: '权限配置',
        features: '功能开关'
    };

    const lowerKey = key.toLowerCase();
    for (const [pattern, desc] of Object.entries(descriptionMap)) {
        if (lowerKey.includes(pattern)) {
            return desc;
        }
    }

    return null;
};

// 格式化标签名称
const formatLabel = (label) => {
    return label
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
};

// --- 子组件 ---

const PluginCard = ({ plugin, onToggleEnabled, onShowReadme, onShowConfig }) => {
    const initial = getInitial(plugin.name);
    const [colorFrom, colorTo] = generateColor(plugin.name);

    return (
        <div className="group bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between min-h-[240px] overflow-hidden hover:-translate-y-1">
            <div className="p-5">
                {/* 头部：头像 + 标题 + 状态 */}
                <div className="flex items-start gap-3 mb-3">
                    {/* 头像 */}
                    <div
                        className={`flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br flex items-center justify-center text-white font-bold text-lg shadow-lg`}
                        style={{ backgroundImage: `linear-gradient(135deg, ${colorFrom}, ${colorTo})` }}
                    >
                        {plugin.avatar ? (
                            <img src={plugin.avatar} alt={plugin.name} className="w-full h-full object-cover rounded-lg" />
                        ) : (
                            initial
                        )}
                    </div>

                    {/* 标题和状态 */}
                    <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-semibold text-gray-800 truncate mb-1" title={plugin.name}>
                            {plugin.name}
                        </h3>
                        <div className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${plugin.is_globally_enabled
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                            }`}>
                            <span className={`w-1.5 h-1.5 rounded-full mr-1.5 ${plugin.is_globally_enabled ? 'bg-green-500' : 'bg-gray-400'
                                }`}></span>
                            {plugin.is_globally_enabled ? '已启用' : '已禁用'}
                        </div>
                    </div>
                </div>

                {/* 描述 */}
                <p className="text-sm text-gray-600 mb-3 h-10 line-clamp-2" title={plugin.description}>
                    {plugin.description || '暂无描述'}
                </p>

                {/* 元信息 */}
                <div className="flex items-center justify-between text-xs text-gray-500">
                    <span className="flex items-center">
                        <i className="fas fa-user mr-1 text-gray-400"></i>
                        <span className="font-medium">{plugin.author || '未知作者'}</span>
                    </span>
                    <span className="flex items-center">
                        <i className="fas fa-code-branch mr-1 text-gray-400"></i>
                        <span className="font-medium">{plugin.version || '1.0.0'}</span>
                    </span>
                </div>
            </div>

            {/* 底部操作栏 */}
            <div className="bg-gradient-to-t from-gray-50 to-white px-4 py-3 border-t border-gray-100 flex items-center justify-between">
                <label className="relative inline-flex items-center cursor-pointer">
                    <input
                        type="checkbox"
                        checked={plugin.is_globally_enabled}
                        onChange={onToggleEnabled}
                        className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-purple-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-purple-500 peer-checked:to-purple-600"></div>
                </label>

                <div className="flex items-center space-x-1">
                    <IconButton
                        icon="fa-book"
                        tooltip="查看文档"
                        onClick={onShowReadme}
                        className="opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                    />
                    <IconButton
                        icon="fa-cog"
                        tooltip="插件设置"
                        onClick={onShowConfig}
                        className="opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                    />
                </div>
            </div>
        </div>
    );
};

const IconButton = ({ icon, tooltip, onClick, className = '' }) => (
    <button
        onClick={onClick}
        className={`p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-all duration-200 ${className}`}
        title={tooltip}
    >
        <i className={`fas ${icon}`}></i>
    </button>
);

const ReadmeModal = ({ plugin, onClose }) => (
    <Modal
        isOpen={!!plugin}
        onClose={onClose}
        title={`文档: ${plugin?.name || ''}`}
        size="3xl"
        className="max-h-[80vh] flex flex-col"
    >
        <div className="overflow-y-auto flex-grow">
            <div className="markdown-body">
                {plugin?.readme ? (
                    <ReactMarkdown>{plugin.readme}</ReactMarkdown>
                ) : (
                    <p className="text-center text-gray-500">这个插件没有提供README文档。</p>
                )}
            </div>
        </div>
    </Modal>
);

// --- 配置模态框组件 ---

const PrimitiveField = ({ label, value, path, onChange }) => {
    const fieldType = typeof value;
    const description = getConfigDescription(label);
    const icon = getConfigIcon(label);
    const formattedLabel = formatLabel(label);

    if (fieldType === 'boolean') {
        return (
            <div className="group bg-white rounded-lg p-4 hover:shadow-md transition-all duration-200">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center text-purple-600">
                            <i className={`${icon} text-sm`}></i>
                        </div>
                        <div>
                            <label className="text-sm font-medium text-gray-800">{formattedLabel}</label>
                            {description && (
                                <p className="text-xs text-gray-500 mt-0.5">{description}</p>
                            )}
                        </div>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input
                            type="checkbox"
                            checked={!!value}
                            onChange={e => onChange(path, e.target.checked)}
                            className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-purple-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-purple-500 peer-checked:to-purple-600"></div>
                    </label>
                </div>
            </div>
        );
    }

    return (
        <div className="group bg-white rounded-lg p-4 hover:shadow-md transition-all duration-200">
            <div className="flex items-center space-x-3 mb-2">
                <div className="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center text-purple-600">
                    <i className={`${icon} text-sm`}></i>
                </div>
                <div className="flex-1">
                    <label className="text-sm font-medium text-gray-800">{formattedLabel}</label>
                    {description && (
                        <p className="text-xs text-gray-500 mt-0.5">{description}</p>
                    )}
                </div>
            </div>
            <input
                type={fieldType === 'number' ? 'number' : 'text'}
                value={value}
                onChange={e => onChange(path, fieldType === 'number' ? Number(e.target.value) : e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                placeholder={`输入${formattedLabel.toLowerCase()}...`}
            />
        </div>
    );
};

const TagsField = ({ label, array, path, onChange }) => {
    const [inputValue, setInputValue] = useState('');
    const [isExpanded, setIsExpanded] = useState(true);
    const icon = getConfigIcon(label);
    const formattedLabel = formatLabel(label);
    const description = getConfigDescription(label);

    const handleAddItem = () => {
        if (inputValue.trim() && !array.includes(inputValue.trim())) {
            onChange(path, [...array, inputValue.trim()]);
            setInputValue('');
        }
    };

    const handleRemoveItem = (itemToRemove) => {
        onChange(path, array.filter(item => item !== itemToRemove));
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleAddItem();
        }
    };

    return (
        <div className="bg-purple-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center text-white shadow-lg">
                        <i className={`${icon} text-sm`}></i>
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-gray-900 group-hover:text-purple-700 transition-colors duration-200">
                            {formattedLabel}
                        </h3>
                        {description && (
                            <p className="text-xs text-gray-500 mt-0.5">{description}</p>
                        )}
                    </div>
                </div>
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-100 rounded-lg transition-all duration-200"
                >
                    <i className={`fas fa-chevron-${isExpanded ? 'up' : 'down'}`}></i>
                </button>
            </div>

            {isExpanded && (
                <div className="space-y-3">
                    <div className="flex flex-wrap gap-2">
                        {array.map((item, index) => (
                            <div
                                key={index}
                                className="group/tag inline-flex items-center bg-white px-3 py-1.5 rounded-full text-sm font-medium text-purple-700 border border-purple-200 hover:border-purple-300 hover:shadow-md transition-all duration-200"
                            >
                                <span>{item}</span>
                                <button
                                    onClick={() => handleRemoveItem(item)}
                                    className="ml-2 text-purple-400 hover:text-red-500 transition-colors duration-200"
                                >
                                    <i className="fas fa-times text-xs"></i>
                                </button>
                            </div>
                        ))}
                        {array.length === 0 && (
                            <p className="text-sm text-gray-500 italic">暂无标签</p>
                        )}
                    </div>

                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={e => setInputValue(e.target.value)}
                            onKeyDown={handleKeyDown}
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                            placeholder="添加新标签..."
                        />
                        <button
                            onClick={handleAddItem}
                            disabled={!inputValue.trim()}
                            className="px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg text-sm font-medium hover:from-purple-700 hover:to-purple-800 shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <i className="fas fa-plus mr-1.5"></i>
                            添加
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

const ArrayOfObjectsField = ({ label, array, path, onChange }) => {
    const [expandedItems, setExpandedItems] = useState({});
    const icon = getConfigIcon(label);
    const formattedLabel = formatLabel(label);
    const description = getConfigDescription(label);

    const handleAddItem = () => {
        const newItem = array.length > 0
            ? Object.fromEntries(Object.keys(array[0]).map(key => [key, '']))
            : {};
        onChange(path, [...array, newItem]);
    };

    const handleRemoveItem = (index) => {
        if (window.confirm('确定要删除这个条目吗？')) {
            onChange(path, array.filter((_, i) => i !== index));
            // 清理展开状态
            const newExpanded = { ...expandedItems };
            delete newExpanded[index];
            setExpandedItems(newExpanded);
        }
    };

    const toggleExpanded = (index) => {
        setExpandedItems(prev => ({
            ...prev,
            [index]: !prev[index]
        }));
    };

    return (
        <div className="bg-blue-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white shadow-lg">
                        <i className={`${icon} text-sm`}></i>
                    </div>
                    <div>
                        <h3 className="text-sm font-semibold text-gray-900 group-hover:text-blue-700 transition-colors duration-200">
                            {formattedLabel}
                        </h3>
                        {description && (
                            <p className="text-xs text-gray-500 mt-0.5">{description}</p>
                        )}
                        <p className="text-xs text-gray-500 mt-1">共 {array.length} 个条目</p>
                    </div>
                </div>
                <button
                    onClick={handleAddItem}
                    className="px-3 py-1.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg text-sm font-medium hover:from-blue-700 hover:to-blue-800 shadow-md hover:shadow-lg transition-all duration-200"
                >
                    <i className="fas fa-plus mr-1.5"></i>
                    添加条目
                </button>
            </div>

            <div className="space-y-3">
                {array.map((item, index) => (
                    <div
                        key={index}
                        className="bg-white rounded-lg border border-blue-200 overflow-hidden hover:border-blue-300 hover:shadow-md transition-all duration-200"
                    >
                        <div className="p-4">
                            <div className="flex items-center justify-between mb-3">
                                <h4 className="text-sm font-medium text-gray-800">
                                    条目 {index + 1}
                                </h4>
                                <div className="flex items-center space-x-2">
                                    <button
                                        onClick={() => toggleExpanded(index)}
                                        className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200"
                                        title={expandedItems[index] ? '收起' : '展开'}
                                    >
                                        <i className={`fas fa-chevron-${expandedItems[index] ? 'up' : 'down'}`}></i>
                                    </button>
                                    <button
                                        onClick={() => handleRemoveItem(index)}
                                        className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
                                        title="删除"
                                    >
                                        <i className="fas fa-trash text-sm"></i>
                                    </button>
                                </div>
                            </div>

                            {(expandedItems[index] !== false) && (
                                <div className="space-y-3">
                                    {Object.entries(item).map(([key, value]) => (
                                        <PrimitiveField
                                            key={key}
                                            label={key}
                                            value={value}
                                            path={[...path, index, key]}
                                            onChange={onChange}
                                        />
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {array.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                        <i className="fas fa-inbox text-3xl mb-2"></i>
                        <p className="text-sm">暂无条目，点击上方按钮添加</p>
                    </div>
                )}
            </div>
        </div>
    );
};

const ConfigRenderer = ({ data, path, onChange }) => {
    // 将配置项分组
    const groupedData = {};
    const primitiveFields = {};

    Object.entries(data).forEach(([key, value]) => {
        const fieldType = typeof value;

        // 基础类型字段
        if (fieldType !== 'object' || value === null) {
            primitiveFields[key] = value;
        } else if (Array.isArray(value)) {
            // 数组类型单独处理
            if (!groupedData['arrays']) groupedData['arrays'] = {};
            groupedData['arrays'][key] = value;
        } else {
            // 对象类型分组
            groupedData[key] = value;
        }
    });

    return (
        <div className="space-y-6">
            {/* 基础配置项 */}
            {Object.keys(primitiveFields).length > 0 && (
                <div className="bg-gray-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
                    <h3 className="flex items-center text-sm font-semibold text-gray-900 mb-4 group-hover:text-purple-700 transition-colors duration-200">
                        <i className="fas fa-cog mr-2 text-purple-600 group-hover:scale-110 transition-transform duration-200"></i>
                        基础配置
                    </h3>
                    <div className="space-y-3">
                        {Object.entries(primitiveFields).map(([key, value]) => (
                            <PrimitiveField
                                key={key}
                                label={key}
                                value={value}
                                path={[...path, key]}
                                onChange={onChange}
                            />
                        ))}
                    </div>
                </div>
            )}

            {/* 数组类型配置 */}
            {groupedData.arrays && Object.entries(groupedData.arrays).map(([key, value]) => {
                const newPath = [...path, key];

                // 判断是标签数组还是对象数组
                if (value.every(item => typeof item === 'string' || typeof item === 'number')) {
                    return <TagsField key={newPath.join('.')} label={key} array={value} path={newPath} onChange={onChange} />;
                } else if (value.every(item => typeof item === 'object' && item !== null && !Array.isArray(item))) {
                    return <ArrayOfObjectsField key={newPath.join('.')} label={key} array={value} path={newPath} onChange={onChange} />;
                }
                return null;
            })}

            {/* 对象类型配置 */}
            {Object.entries(groupedData).map(([key, value]) => {
                if (key === 'arrays') return null;
                const newPath = [...path, key];
                const icon = getConfigIcon(key);
                const formattedLabel = formatLabel(key);
                const description = getConfigDescription(key);

                return (
                    <div key={newPath.join('.')} className="bg-indigo-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
                        <div className="flex items-center space-x-3 mb-4">
                            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-lg">
                                <i className={`${icon} text-sm`}></i>
                            </div>
                            <div>
                                <h3 className="text-sm font-semibold text-gray-900 group-hover:text-indigo-700 transition-colors duration-200">
                                    {formattedLabel}
                                </h3>
                                {description && (
                                    <p className="text-xs text-gray-500 mt-0.5">{description}</p>
                                )}
                            </div>
                        </div>
                        <div className="space-y-3">
                            <ConfigRenderer data={value} path={newPath} onChange={onChange} />
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

const ConfigModal = ({ plugin, onClose, onSave }) => {
    const [config, setConfig] = useState({});
    const [hasChanges, setHasChanges] = useState(false);
    const [isResetting, setIsResetting] = useState(false);

    // 当 plugin 改变时，重新初始化 config
    useEffect(() => {
        if (!plugin) {
            setConfig({});
            setHasChanges(false);
            return;
        }

        const defaultConfig = JSON.parse(JSON.stringify(plugin.config_schema || {}));
        const savedConfig = plugin.global_config || {};

        const mergeConfigs = (target, source) => {
            for (const key in source) {
                if (source[key] instanceof Object && !Array.isArray(source[key]) && key in target) {
                    target[key] = mergeConfigs(target[key] || {}, source[key]);
                } else {
                    target[key] = source[key];
                }
            }
            return target;
        };

        const mergedConfig = mergeConfigs(defaultConfig, savedConfig);
        setConfig(mergedConfig);
        setHasChanges(false);
    }, [plugin]);

    const handleSave = () => {
        if (plugin) {
            onSave(plugin.plugin_id, config);
            setHasChanges(false);
        }
    };

    const handleReset = () => {
        if (window.confirm('确定要重置所有配置吗？这将恢复到默认设置。')) {
            setIsResetting(true);
            const defaultConfig = JSON.parse(JSON.stringify(plugin.config_schema || {}));
            setConfig(defaultConfig);
            setHasChanges(true);
            setTimeout(() => setIsResetting(false), 500);
        }
    };

    const handleValueChange = (path, value) => {
        setConfig(prev => {
            const newConfig = JSON.parse(JSON.stringify(prev));
            let current = newConfig;
            for (let i = 0; i < path.length - 1; i++) {
                current = current[path[i]];
            }
            current[path[path.length - 1]] = value;
            return newConfig;
        });
        setHasChanges(true);
    };

    // 获取插件颜色
    const [colorFrom, colorTo] = generateColor(plugin?.name || '');

    const footer = (
        <div className="flex items-center justify-between">
            <button
                onClick={handleReset}
                disabled={!hasChanges || isResetting}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
            >
                <i className={`fas fa-undo mr-2 ${isResetting ? 'animate-spin' : ''}`}></i>
                重置配置
            </button>
            <div className="flex space-x-3">
                <button
                    onClick={onClose}
                    className="px-5 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
                >
                    取消
                </button>
                <button
                    onClick={handleSave}
                    disabled={!hasChanges}
                    className="px-5 py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 border border-transparent rounded-xl text-sm font-medium text-white hover:from-purple-700 hover:to-purple-800 shadow-md hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <i className="fas fa-save mr-2"></i>
                    保存并重载
                </button>
            </div>
        </div>
    );

    return (
        <Modal
            isOpen={!!plugin}
            onClose={onClose}
            title=""
            size="2xl"
            footer={footer}
        >
            {plugin && (
                <>
                    {/* 插件信息头部 */}
                    <div className="relative rounded-2xl overflow-hidden mb-6 bg-gradient-to-br from-purple-50 to-pink-50">
                        {/* 背景装饰 */}
                        <div className="absolute inset-0 opacity-10">
                            <div className="absolute -top-4 -right-4 w-32 h-32 rounded-full bg-gradient-to-br from-purple-400 to-pink-400"></div>
                            <div className="absolute -bottom-4 -left-4 w-24 h-24 rounded-full bg-gradient-to-br from-blue-400 to-purple-400"></div>
                        </div>

                        {/* 插件信息 */}
                        <div className="relative z-10 p-6">
                            <div className="flex items-center space-x-4">
                                <div className="relative">
                                    <div
                                        className="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-bold text-xl shadow-xl"
                                        style={{ backgroundImage: `linear-gradient(135deg, ${colorFrom}, ${colorTo})` }}
                                    >
                                        {plugin.avatar ? (
                                            <img src={plugin.avatar} alt={plugin.name} className="w-full h-full object-cover rounded-2xl" />
                                        ) : (
                                            getInitial(plugin.name)
                                        )}
                                    </div>
                                    <div className={`absolute -bottom-1 -right-1 w-5 h-5 rounded-full border-2 border-white ${plugin.is_globally_enabled ? 'bg-green-500' : 'bg-gray-400'
                                        } shadow-lg`}></div>
                                </div>
                                <div className="flex-1">
                                    <h2 className="text-xl font-bold text-gray-900 mb-1">
                                        {plugin.name} 配置
                                    </h2>
                                    <p className="text-sm text-gray-600 mb-2">
                                        {plugin.description || '配置此插件的参数'}
                                    </p>
                                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                                        <span className="flex items-center">
                                            <i className="fas fa-user mr-1"></i>
                                            {plugin.author || '未知作者'}
                                        </span>
                                        <span className="flex items-center">
                                            <i className="fas fa-code-branch mr-1"></i>
                                            v{plugin.version || '1.0.0'}
                                        </span>
                                        {hasChanges && (
                                            <span className="flex items-center text-amber-600">
                                                <i className="fas fa-exclamation-circle mr-1"></i>
                                                有未保存的更改
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 配置内容 */}
                    <div className="max-h-[60vh] overflow-y-auto custom-scrollbar">
                        {Object.keys(config).length > 0 ? (
                            <ConfigRenderer data={config} path={[]} onChange={handleValueChange} />
                        ) : (
                            <div className="text-center py-12">
                                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <i className="fas fa-cogs text-2xl text-gray-400"></i>
                                </div>
                                <h3 className="text-lg font-medium text-gray-800 mb-2">
                                    无配置项
                                </h3>
                                <p className="text-gray-500">
                                    这个插件没有可配置的选项
                                </p>
                            </div>
                        )}
                    </div>
                </>
            )}
        </Modal>
    );
};

export default Plugins;