import React, { useState, useEffect, useCallback } from 'react';
import ReactDOM from 'react-dom';
import pluginService from '../services/pluginService';
import useApiLoading from '../hooks/useApiLoading';
import useNotification from '../hooks/useNotification';
import LoadingSpinner from '../components/common/LoadingSpinner';
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
            {showReadmeModal && (
                <ReadmeModal plugin={showReadmeModal} onClose={() => setShowReadmeModal(null)} />
            )}
            {showConfigModal && (
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
            )}
        </div>
    );
};

// --- 子组件 ---

const PluginCard = ({ plugin, onToggleEnabled, onShowReadme, onShowConfig }) => (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 flex flex-col justify-between min-h-[200px]">
        <div className="p-5">
            <div className="flex items-center justify-between gap-2">
                <h3 className="text-lg font-semibold text-gray-800 truncate" title={plugin.name}>{plugin.name}</h3>
                <div className={`px-2 py-0.5 rounded-full text-xs font-medium flex-shrink-0 ${plugin.is_globally_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                    {plugin.is_globally_enabled ? '已启用' : '已禁用'}
                </div>
            </div>
            <p className="text-sm text-gray-500 mt-2 h-10 line-clamp-2" title={plugin.description}>{plugin.description || '暂无描述'}</p>
            <div className="mt-3 text-xs text-gray-400 flex items-center justify-between">
                <span className="truncate pr-2">作者: <span className="font-medium text-gray-600">{plugin.author}</span></span>
                <span className="truncate flex-shrink-0">版本: <span className="font-medium text-gray-600">{plugin.version}</span></span>
            </div>
        </div>
        <div className="bg-gray-50 px-4 py-2 border-t border-gray-100 flex items-center justify-between rounded-b-lg">
            <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" checked={plugin.is_globally_enabled} onChange={onToggleEnabled} className="sr-only peer" />
                <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-purple-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
            <div className="flex items-center space-x-4">
                <IconButton icon="fa-book" tooltip="文档" onClick={onShowReadme} />
                <IconButton icon="fa-cog" tooltip="设置" onClick={onShowConfig} />
            </div>
        </div>
    </div>
);

const IconButton = ({ icon, tooltip, onClick }) => (
    <button onClick={onClick} className="text-gray-500 hover:text-purple-600 transition-colors duration-200" title={tooltip}>
        <i className={`fas ${icon}`}></i>
    </button>
);

const ReadmeModal = ({ plugin, onClose }) => (
    ReactDOM.createPortal(
        <div className="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4" onClick={onClose}>
            <div className="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[80vh] flex flex-col overflow-hidden" onClick={e => e.stopPropagation()}>
                <div className="p-5 border-b flex justify-between items-center flex-shrink-0">
                    <h2 className="text-xl font-bold text-gray-800">文档: {plugin.name}</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-800 text-2xl leading-none">&times;</button>
                </div>
                <div className="p-6 overflow-y-auto flex-grow">
                    <div className="markdown-body">
                        {plugin.readme ? <ReactMarkdown>{plugin.readme}</ReactMarkdown> : <p className="text-center text-gray-500">这个插件没有提供README文档。</p>}
                    </div>
                </div>
            </div>
        </div>,
        document.body
    )
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
    const [config, setConfig] = useState(() => {
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
        return mergeConfigs(defaultConfig, savedConfig);
    });

    const handleSave = () => {
        onSave(plugin.plugin_id, config);
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

    return ReactDOM.createPortal(
        <div className="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4" onClick={onClose}>
            <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col" onClick={e => e.stopPropagation()}>
                <div className="p-5 border-b flex justify-between items-center flex-shrink-0">
                    <h2 className="text-xl font-bold text-gray-800">配置: {plugin.name}</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-800 text-2xl leading-none">&times;</button>
                </div>
                <div className="p-6 overflow-y-auto flex-grow">
                    {Object.keys(config).length > 0 ? (
                        <ConfigRenderer data={config} path={[]} onChange={handleValueChange} />
                    ) : (
                        <p className="text-center text-gray-500">这个插件没有可配置的选项。</p>
                    )}
                </div>
                <div className="p-4 bg-gray-50 border-t flex justify-end space-x-3 flex-shrink-0">
                    <button onClick={onClose} className="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                        取消
                    </button>
                    <button onClick={handleSave} className="px-4 py-2 bg-purple-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-purple-700">
                        保存并重载
                    </button>
                </div>
            </div>
        </div>,
        document.body
    );
};

export default Plugins;