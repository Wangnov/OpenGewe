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
    if (fieldType === 'boolean') {
        return (
            <div className="flex items-center justify-between py-2">
                <label className="text-sm font-medium text-gray-700 capitalize">{label.replace(/_/g, ' ')}</label>
                <div className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" checked={!!value} onChange={e => onChange(path, e.target.checked)} className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-purple-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                </div>
            </div>
        );
    }
    return (
        <div className="flex items-center">
            <label className="text-sm font-medium text-gray-700 capitalize w-1/3">{label.replace(/_/g, ' ')}</label>
            <input
                type={fieldType === 'number' ? 'number' : 'text'}
                value={value}
                onChange={e => onChange(path, fieldType === 'number' ? Number(e.target.value) : e.target.value)}
                className="block w-2/3 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
            />
        </div>
    );
};

const TagsField = ({ label, array, path, onChange }) => {
    const [inputValue, setInputValue] = useState('');
    const handleAddItem = () => {
        if (inputValue && !array.includes(inputValue)) {
            onChange(path, [...array, inputValue]);
            setInputValue('');
        }
    };
    const handleRemoveItem = (itemToRemove) => {
        onChange(path, array.filter(item => item !== itemToRemove));
    };
    return (
        <div className="pt-4">
            <h3 className="text-lg font-semibold text-gray-800 capitalize border-b pb-2 mb-2">{label}</h3>
            <div className="flex flex-wrap gap-2 mb-2">
                {array.map((item, index) => (
                    <div key={index} className="flex items-center bg-purple-100 text-purple-800 text-sm font-medium px-2.5 py-1 rounded-full">
                        {item}
                        <button onClick={() => handleRemoveItem(item)} className="ml-2 text-purple-500 hover:text-purple-700">
                            <i className="fas fa-times-circle"></i>
                        </button>
                    </div>
                ))}
            </div>
            <div className="flex gap-2">
                <input
                    type="text"
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleAddItem()}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
                    placeholder="添加新标签..."
                />
                <button onClick={handleAddItem} className="px-4 py-2 bg-purple-600 text-white rounded-md text-sm font-medium hover:bg-purple-700">添加</button>
            </div>
        </div>
    );
};

const ArrayOfObjectsField = ({ label, array, path, onChange }) => {
    const handleAddItem = () => {
        const newItem = array.length > 0 ? Object.fromEntries(Object.keys(array[0]).map(key => [key, ''])) : {};
        onChange(path, [...array, newItem]);
    };
    const handleRemoveItem = (index) => {
        onChange(path, array.filter((_, i) => i !== index));
    };
    return (
        <div className="pt-4">
            <h3 className="text-lg font-semibold text-gray-800 capitalize border-b pb-2 mb-4">{label}</h3>
            <div className="space-y-4">
                {array.map((item, index) => (
                    <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200 relative">
                        <div className="space-y-2">
                            {Object.entries(item).map(([key, value]) => (
                                <PrimitiveField key={key} label={key} value={value} path={[...path, index, key]} onChange={onChange} />
                            ))}
                        </div>
                        <button onClick={() => handleRemoveItem(index)} className="absolute top-1/2 -translate-y-1/2 right-[-30px] text-red-500 hover:text-red-700 px-2 py-1">
                            <i className="fas fa-trash-alt"></i>
                        </button>
                    </div>
                ))}
            </div>
            <button onClick={handleAddItem} className="mt-4 px-4 py-2 bg-purple-100 text-purple-700 rounded-md text-sm font-medium hover:bg-purple-200 flex items-center">
                <i className="fas fa-plus mr-2"></i> 添加新条目
            </button>
        </div>
    );
};

const ConfigRenderer = ({ data, path, onChange }) => (
    <div className="space-y-4">
        {Object.entries(data).map(([key, value]) => {
            const newPath = [...path, key];
            const fieldType = typeof value;

            if (Array.isArray(value)) {
                if (value.every(item => typeof item === 'object' && item !== null && !Array.isArray(item))) {
                    return <ArrayOfObjectsField key={newPath.join('.')} label={key} array={value} path={newPath} onChange={onChange} />;
                } else if (value.every(item => typeof item === 'string' || typeof item === 'number')) {
                    return <TagsField key={newPath.join('.')} label={key} array={value} path={newPath} onChange={onChange} />;
                }
            }

            if (fieldType === 'object' && value !== null) {
                return (
                    <div key={newPath.join('.')} className="pt-4">
                        <h3 className="text-lg font-semibold text-gray-800 capitalize border-b pb-2 mb-4">{key}</h3>
                        <div className="space-y-4 pl-2">
                            <ConfigRenderer data={value} path={newPath} onChange={onChange} />
                        </div>
                    </div>
                );
            }

            return <PrimitiveField key={newPath.join('.')} label={key} value={value} path={newPath} onChange={onChange} />;
        })}
    </div>
);

const ConfigModal = ({ plugin, onClose, onSave }) => {
    const [config, setConfig] = useState({});

    // 当 plugin 改变时，重新初始化 config
    useEffect(() => {
        if (!plugin) {
            setConfig({});
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
    }, [plugin]);

    const handleSave = () => {
        if (plugin) {
            onSave(plugin.plugin_id, config);
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
    };

    const footer = (
        <div className="flex justify-end space-x-3">
            <button
                onClick={onClose}
                className="px-5 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
            >
                取消
            </button>
            <button
                onClick={handleSave}
                className="px-5 py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 border border-transparent rounded-xl text-sm font-medium text-white hover:from-purple-700 hover:to-purple-800 shadow-md hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
            >
                <i className="fas fa-save mr-2"></i>
                保存并重载
            </button>
        </div>
    );

    return (
        <Modal
            isOpen={!!plugin}
            onClose={onClose}
            title={`配置: ${plugin?.name || ''}`}
            size="2xl"
            className="max-h-[80vh] flex flex-col"
            footer={footer}
        >
            <div className="overflow-y-auto flex-grow">
                {Object.keys(config).length > 0 ? (
                    <ConfigRenderer data={config} path={[]} onChange={handleValueChange} />
                ) : (
                    <p className="text-center text-gray-500">这个插件没有可配置的选项。</p>
                )}
            </div>
        </Modal>
    );
};

export default Plugins;