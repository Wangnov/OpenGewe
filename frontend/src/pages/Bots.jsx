import React, { useState, useEffect, useCallback } from 'react';
// Font Awesome icons are loaded via CDN in index.html
import botService from '../services/botService';
import BotDetailModal from '../components/bots/BotDetailModal';
import CreateBotModal from '../components/bots/CreateBotModal';
import LoadingSpinner from '../components/common/LoadingSpinner';
import CachedImage from '../components/common/CachedImage';
import useApiLoading from '../hooks/useApiLoading';
import useNotification from '../hooks/useNotification';

/**
 * 机器人管理页面
 * @returns {JSX.Element} 机器人管理页面组件
 */
const Bots = () => {
    const [bots, setBots] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedBot, setSelectedBot] = useState(null);
    const [showDetailModal, setShowDetailModal] = useState(false);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [copiedField, setCopiedField] = useState(null);
    const [refreshingBot, setRefreshingBot] = useState(null);
    const { executeWithLoading } = useApiLoading();
    const { success, error: notifyError, info } = useNotification();

    // 获取机器人列表
    const fetchBots = useCallback(async (isManualRefresh = false) => {
        try {
            setLoading(true);
            const response = await executeWithLoading(async () => {
                return await botService.getBots();
            });
            console.log('API响应数据:', response);
            // 根据实际API响应结构解析数据
            const botsData = response.data?.data || response.data?.bots || response.data || [];
            console.log('解析的机器人数据:', botsData);
            setBots(Array.isArray(botsData) ? botsData : []);

            // 仅在手动刷新时显示成功通知
            if (isManualRefresh) {
                info('刷新成功', `已获取到 ${Array.isArray(botsData) ? botsData.length : 0} 个机器人`, {
                    duration: 2000
                });
            }
        } catch (error) {
            console.error('获取机器人列表失败:', error);
            notifyError('获取失败', '获取机器人列表失败，请检查网络连接', {
                duration: 5000,
                actions: [{
                    label: '重试',
                    onClick: () => fetchBots(true),
                    variant: 'primary'
                }]
            });
        } finally {
            setLoading(false);
        }
    }, [executeWithLoading, info, notifyError]);

    // 刷新单个机器人信息
    const updateBot = async (geweAppId) => {
        try {
            setRefreshingBot(geweAppId);
            const bot = bots.find(b => b.gewe_app_id === geweAppId);

            await executeWithLoading(async () => {
                await botService.updateBotInfo(geweAppId);
            });

            success('更新成功', `机器人 "${bot?.nickname || 'Unknown'}" 信息已成功刷新`, {
                duration: 3000,
                metadata: { botId: geweAppId, botName: bot?.nickname }
            });

            // 重新获取列表
            fetchBots();
        } catch (error) {
            console.error('刷新机器人信息失败:', error);
            const bot = bots.find(b => b.gewe_app_id === geweAppId);
            notifyError('更新失败', `机器人 "${bot?.nickname || 'Unknown'}" 信息刷新失败，请稍后重试`, {
                duration: 5000,
                metadata: { botId: geweAppId, botName: bot?.nickname },
                actions: [{
                    label: '重试',
                    onClick: () => updateBot(geweAppId),
                    variant: 'primary'
                }]
            });
        } finally {
            setRefreshingBot(null);
        }
    };

    // 复制文本到剪贴板
    const copyToClipboard = async (text, fieldName) => {
        try {
            await navigator.clipboard.writeText(text);
            setCopiedField(fieldName);

            success('复制成功', '内容已复制到剪贴板', {
                duration: 2000
            });

            setTimeout(() => setCopiedField(null), 2000);
        } catch (error) {
            console.error('复制失败:', error);
            notifyError('复制失败', '无法复制到剪贴板，请手动复制', {
                duration: 3000
            });
        }
    };

    // 打开机器人详情
    const openBotDetail = (bot) => {
        setSelectedBot(bot);
        setShowDetailModal(true);
    };

    // 进入机器人管理页面
    const enterBotManagement = (botId) => {
        window.open(`/bots/${botId}`, '_blank');
    };

    // 删除机器人
    const deleteBot = async (geweAppId) => {
        try {
            const bot = bots.find(b => b.gewe_app_id === geweAppId);

            await executeWithLoading(async () => {
                await botService.deleteBot(geweAppId);
            });

            success('删除成功', `机器人 "${bot?.nickname || 'Unknown'}" 已成功删除`, {
                duration: 3000,
                metadata: { botId: geweAppId, botName: bot?.nickname },
                actions: [{
                    label: '查看列表',
                    onClick: () => fetchBots(),
                    variant: 'primary'
                }]
            });

            fetchBots();
        } catch (error) {
            console.error('删除机器人失败:', error);
            const bot = bots.find(b => b.gewe_app_id === geweAppId);
            notifyError('删除失败', `机器人 "${bot?.nickname || 'Unknown'}" 删除失败，请稍后重试`, {
                duration: 5000,
                metadata: { botId: geweAppId, botName: bot?.nickname },
                actions: [{
                    label: '重试',
                    onClick: () => deleteBot(geweAppId),
                    variant: 'primary'
                }]
            });
        }
    };

    // 创建机器人成功回调
    const handleBotCreated = () => {
        success('创建成功', '新机器人已成功创建并添加到列表', {
            duration: 3000,
            actions: [{
                label: '查看详情',
                onClick: () => fetchBots(),
                variant: 'primary'
            }]
        });
        fetchBots();
        setShowCreateModal(false);
    };

    // 机器人更新成功回调
    const handleBotUpdated = (updatedBotData) => {
        success('更新成功', `机器人 "${updatedBotData.nickname || 'Unknown'}" 信息已成功更新`, {
            duration: 3000,
            metadata: { botId: updatedBotData.gewe_app_id, botName: updatedBotData.nickname }
        });

        // 直接更新列表中的机器人数据
        setBots(prevBots =>
            prevBots.map(bot =>
                bot.gewe_app_id === updatedBotData.gewe_app_id ? updatedBotData : bot
            )
        );

        // 如果当前选中的机器人是更新的机器人，也更新它
        if (selectedBot && selectedBot.gewe_app_id === updatedBotData.gewe_app_id) {
            setSelectedBot(updatedBotData);
        }
    };

    useEffect(() => {
        fetchBots();
    }, [fetchBots]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <LoadingSpinner size="lg" text="加载机器人列表中..." />
            </div>
        );
    }

    return (
        <div>
            {/* 页面标题和操作按钮 */}
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold text-gray-900">机器人列表</h1>
                <div className="flex space-x-3">
                    <button
                        onClick={() => fetchBots(true)}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                    >
                        <i className="fas fa-sync-alt h-4 w-4 mr-2 flex items-center"></i>
                        刷新
                    </button>
                    <button
                        onClick={() => setShowCreateModal(true)}
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                    >
                        <i className="fas fa-plus h-4 w-4 mr-2 flex items-center"></i>
                        新建
                    </button>
                </div>
            </div>

            {/* 机器人卡片网格 */}
            {bots.length === 0 ? (
                <div className="text-center py-12">
                    <div className="text-gray-400 text-lg mb-4">暂无机器人</div>
                    <button
                        onClick={() => setShowCreateModal(true)}
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700"
                    >
                        <i className="fas fa-plus h-4 w-4 mr-2 align-middle"></i>
                        创建第一个机器人
                    </button>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {bots.map((bot) => (
                        <div
                            key={bot.gewe_app_id}
                            className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden"
                        >
                            {/* 卡片头部 - 头像和基本信息 */}
                            <div className="p-4">
                                <div className="flex items-center space-x-3 mb-4">
                                    <div
                                        className="relative cursor-pointer"
                                        onClick={() => openBotDetail(bot)}
                                    >
                                        <CachedImage
                                            src={bot.small_head_img_url || '/default-avatar.png'}
                                            alt={bot.nickname || '机器人头像'}
                                            className="w-12 h-12 rounded-full object-cover ring-2 ring-purple-100 hover:ring-purple-300 transition-all"
                                        />
                                        <div className="absolute -bottom-1 -right-1">
                                            <div className={`w-4 h-4 rounded-full border-2 border-white ${bot.is_online ? 'bg-green-500' : 'bg-gray-400'
                                                }`}></div>
                                        </div>
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <h3 className="text-sm font-medium text-gray-900 truncate">
                                            {bot.nickname || '未设置昵称'}
                                        </h3>
                                        <p className="text-xs text-gray-500 truncate">
                                            {bot.is_online ? '在线' : '离线'}
                                        </p>
                                    </div>
                                </div>

                                {/* 参数区域 */}
                                <div className="space-y-2">
                                    {/* Wxid */}
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-500">Wxid:</span>
                                        <div className="flex items-center space-x-1">
                                            <span className="text-xs text-gray-900 truncate max-w-20">
                                                {bot.wxid || 'N/A'}
                                            </span>
                                            {bot.wxid && (
                                                <button
                                                    onClick={() => copyToClipboard(bot.wxid, `wxid-${bot.gewe_app_id}`)}
                                                    className="p-1 hover:bg-gray-100 rounded"
                                                >
                                                    {copiedField === `wxid-${bot.gewe_app_id}` ? (
                                                        <i className="fas fa-check h-3 w-3 text-green-500 align-middle"></i>
                                                    ) : (
                                                        <i className="fas fa-copy h-3 w-3 text-gray-400 align-middle"></i>
                                                    )}
                                                </button>
                                            )}
                                        </div>
                                    </div>

                                    {/* App ID */}
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-500">App ID:</span>
                                        <div className="flex items-center space-x-1">
                                            <span className="text-xs text-gray-900 truncate max-w-20">
                                                {bot.gewe_app_id}
                                            </span>
                                            <button
                                                onClick={() => copyToClipboard(bot.gewe_app_id, `appid-${bot.gewe_app_id}`)}
                                                className="p-1 hover:bg-gray-100 rounded"
                                            >
                                                {copiedField === `appid-${bot.gewe_app_id}` ? (
                                                    <i className="fas fa-check h-3 w-3 text-green-500 align-middle"></i>
                                                ) : (
                                                    <i className="fas fa-copy h-3 w-3 text-gray-400 align-middle"></i>
                                                )}
                                            </button>
                                        </div>
                                    </div>

                                    {/* Token */}
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs text-gray-500">Token:</span>
                                        <div className="flex items-center space-x-1">
                                            <span className="text-xs text-gray-900 truncate max-w-20">
                                                {bot.gewe_token ? '••••••••' : 'N/A'}
                                            </span>
                                            {bot.gewe_token && (
                                                <button
                                                    onClick={() => copyToClipboard(bot.gewe_token, `token-${bot.gewe_app_id}`)}
                                                    className="p-1 hover:bg-gray-100 rounded"
                                                >
                                                    {copiedField === `token-${bot.gewe_app_id}` ? (
                                                        <i className="fas fa-check h-3 w-3 text-green-500 align-middle"></i>
                                                    ) : (
                                                        <i className="fas fa-copy h-3 w-3 text-gray-400 align-middle"></i>
                                                    )}
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* 卡片底部 - 操作按钮 */}
                            <div className="px-4 py-3 bg-gray-50 border-t border-gray-200">
                                <div className="flex justify-between items-center">
                                    <div className="flex space-x-2">
                                        <button
                                            onClick={() => updateBot(bot.gewe_app_id)}
                                            disabled={refreshingBot === bot.gewe_app_id}
                                            className="inline-flex items-center px-2 py-1 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            {refreshingBot === bot.gewe_app_id ? (
                                                <>
                                                    <div className="w-3 h-3 mr-1 border border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                                                    更新中
                                                </>
                                            ) : (
                                                <>
                                                    <i className="fas fa-sync-alt h-3 w-3 mr-1 align-middle"></i>
                                                    更新
                                                </>
                                            )}
                                        </button>
                                        <button
                                            onClick={() => openBotDetail(bot)}
                                            className="inline-flex items-center px-2 py-1 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                                        >
                                            <i className="fas fa-eye h-3 w-3 mr-1 align-middle"></i>
                                            详情
                                        </button>
                                    </div>
                                    <button
                                        onClick={() => enterBotManagement(bot.gewe_app_id)}
                                        className="inline-flex items-center px-3 py-1 text-xs font-medium text-white bg-purple-600 border border-transparent rounded hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                                    >
                                        <i className="fas fa-external-link-alt h-3 w-3 mr-1 align-middle"></i>
                                        进入
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* 机器人详情弹窗 */}
            {showDetailModal && selectedBot && (
                <BotDetailModal
                    bot={selectedBot}
                    isOpen={showDetailModal}
                    onClose={() => {
                        setShowDetailModal(false);
                        setSelectedBot(null);
                    }}
                    onUpdate={handleBotUpdated}
                    onDelete={deleteBot}
                />
            )}

            {/* 创建机器人弹窗 */}
            {showCreateModal && (
                <CreateBotModal
                    isOpen={showCreateModal}
                    onClose={() => setShowCreateModal(false)}
                    onSuccess={handleBotCreated}
                />
            )}
        </div>
    );
};

export default Bots;