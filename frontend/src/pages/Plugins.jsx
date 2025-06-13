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
    const { executeWithLoading } = useApiLoading();
    const { success, error: notifyError, info } = useNotification();

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

    if (loading) {
        return <div className="flex items-center justify-center h-64"><LoadingSpinner size="lg" text="加载插件列表中..." /></div>;
    }

    return (
        <div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {plugins.map(plugin => (
                    <PluginCard
                        key={plugin.plugin_id}
                        plugin={plugin}
                        onToggleEnabled={() => handleToggleEnabled(plugin.plugin_id, plugin.is_globally_enabled)}
                        onShowReadme={() => setShowReadmeModal(plugin)}
                    />
                ))}
            </div>
            {showReadmeModal && (
                <ReadmeModal plugin={showReadmeModal} onClose={() => setShowReadmeModal(null)} />
            )}
        </div>
    );
};

// --- 卡片组件 ---

const PluginCard = ({ plugin, onToggleEnabled, onShowReadme }) => {
    return (
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
                    <IconButton icon="fa-cog" tooltip="设置" onClick={() => alert(`插件的具体配置请在每个机器人的管理页面中进行。`)} />
                    <IconButton icon="fa-sync-alt" tooltip="刷新" onClick={() => alert('刷新功能待实现。')} />
                </div>
            </div>
        </div>
    );
};

// --- 其他组件 ---

const IconButton = ({ icon, tooltip, onClick }) => (
    <button onClick={onClick} className="text-gray-500 hover:text-purple-600 transition-colors duration-200" title={tooltip}>
        <i className={`fas ${icon}`}></i>
    </button>
);

const ReadmeModal = ({ plugin, onClose }) => {
    // 使用 Portal 将 Modal 渲染到 body 的末尾，避免父组件的 transform 样式影响 fixed 定位
    return ReactDOM.createPortal(
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
    );
};

export default Plugins;