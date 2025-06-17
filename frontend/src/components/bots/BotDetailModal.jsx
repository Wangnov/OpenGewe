import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
// Font Awesome icons are loaded via CDN in index.html
import botService from '../../services/botService';
import LoadingSpinner from '../common/LoadingSpinner';
import CachedImage from '../common/CachedImage';
import Modal from '../common/Modal';
import useApiLoading from '../../hooks/useApiLoading';
import { useProxiedImage } from '../../utils/imageProxy';
import useNotification from '../../hooks/useNotification';

/**
 * 机器人背景图片组件
 * @param {Object} props - 组件属性
 * @param {string} props.imageUrl - 图片URL
 * @returns {JSX.Element} 背景图片组件
 */
const BotBackgroundImage = ({ imageUrl }) => {
  const { imageUrl: proxiedImageUrl, loading, error } = useProxiedImage(imageUrl, true);

  if (loading) {
    return (
      <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
        <LoadingSpinner size="sm" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="absolute inset-0 bg-gray-200 flex items-center justify-center text-gray-500">
        图片加载失败
      </div>
    );
  }

  return (
    <div
      className="absolute inset-0 bg-cover bg-center"
      style={{ backgroundImage: `url(${proxiedImageUrl})` }}
    ></div>
  );
};

/**
 * 机器人详情弹窗组件
 * @param {Object} props - 组件属性
 * @param {Object} props.bot - 机器人信息
 * @param {boolean} props.isOpen - 是否打开弹窗
 * @param {Function} props.onClose - 关闭弹窗回调
 * @param {Function} props.onUpdate - 更新成功回调
 * @param {Function} props.onDelete - 删除回调
 * @returns {JSX.Element} 机器人详情弹窗组件
 */
const BotDetailModal = ({ bot, isOpen, onClose, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    gewe_app_id: '',
    gewe_token: '',
    base_url: ''
  });
  const [testing, setTesting] = useState(false);
  const [testPassed, setTestPassed] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [copiedField, setCopiedField] = useState(null);
  const [generalError, setGeneralError] = useState('');
  const { loading: saving, executeWithLoading } = useApiLoading();
  const { success, error: notifyError } = useNotification();

  // 初始化编辑表单
  useEffect(() => {
    if (bot) {
      setEditForm({
        gewe_app_id: bot.gewe_app_id || '',
        gewe_token: bot.gewe_token || '',
        base_url: bot.base_url || 'https://www.geweapi.com/gewe/v2/api'
      });
    }
  }, [bot]);

  // 复制到剪贴板
  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(text === bot.gewe_app_id ? 'gewe_app_id' :
        text === bot.gewe_token ? 'gewe_token' :
          text === bot.base_url ? 'base_url' :
            text === bot.wxid ? 'wxid' : 'unknown');

      setTimeout(() => setCopiedField(null), 2000);
      success('复制成功', '内容已复制到剪贴板', { duration: 2000 });
    } catch (error) {
      console.error('复制失败:', error);
      notifyError('复制失败', '无法复制到剪贴板，请手动复制', { duration: 3000 });
    }
  };

  // 测试机器人连接
  const testConnection = async () => {
    try {
      setTesting(true);
      setTestPassed(false);

      // 使用加载管理器调用测试API
      await executeWithLoading(async () => {
        await botService.testBotConnection({
          gewe_app_id: editForm.gewe_app_id,
          gewe_token: editForm.gewe_token,
          base_url: editForm.base_url
        });
      });

      setTestPassed(true);
      success('连接测试成功', `机器人 "${bot.nickname || 'Unknown'}" 连接正常`, {
        duration: 3000,
        metadata: { botId: bot.gewe_app_id, botName: bot.nickname }
      });
    } catch (error) {
      // 更全面的错误消息提取逻辑
      let errorMessage = '连接测试失败';

      try {
        if (error.response?.data) {
          const responseData = error.response.data;

          // 尝试多种错误消息格式
          if (typeof responseData === 'string') {
            errorMessage = responseData;
          } else if (responseData.detail) {
            errorMessage = responseData.detail;
          } else if (responseData.message) {
            errorMessage = responseData.message;
          } else if (responseData.error) {
            errorMessage = responseData.error;
          } else if (responseData.errors) {
            // 处理验证错误数组
            if (Array.isArray(responseData.errors)) {
              errorMessage = responseData.errors.map(err =>
                typeof err === 'string' ? err : err.message || err.detail || JSON.stringify(err)
              ).join(', ');
            } else {
              errorMessage = JSON.stringify(responseData.errors);
            }
          } else {
            // 如果没有标准错误字段，使用整个响应数据
            errorMessage = JSON.stringify(responseData);
          }
        } else if (error.message) {
          errorMessage = error.message;
        }
      } catch {
        errorMessage = '连接测试失败，请检查控制台获取详细信息';
      }

      // 通知系统调用
      setTimeout(() => {
        notifyError('连接测试失败', `机器人 "${bot.nickname || 'Unknown'}" 连接失败: ${errorMessage}`, {
          duration: 5000,
          metadata: { botId: bot.gewe_app_id, botName: bot.nickname },
          actions: [{
            label: '重试',
            onClick: () => testConnection(),
            variant: 'primary'
          }]
        });
      }, 0);

      // 同时设置备用错误显示
      setGeneralError('连接测试失败: ' + errorMessage);

      setTestPassed(false);
    } finally {
      setTesting(false);
    }
  };

  // 保存编辑
  const saveEdit = async () => {
    if (!testPassed) {
      notifyError('保存失败', '请先通过连接测试再保存', {
        duration: 3000,
        actions: [{
          label: '测试连接',
          onClick: () => testConnection(),
          variant: 'primary'
        }]
      });
      return;
    }

    try {
      const response = await executeWithLoading(async () => {
        return await botService.updateBot(bot.gewe_app_id, {
          gewe_token: editForm.gewe_token,
          base_url: editForm.base_url
        });
      });

      const updatedBotData = response.data;

      setIsEditing(false);
      setTestPassed(false);
      setGeneralError('');

      // 调用更新回调，并传递更新后的数据
      if (onUpdate) {
        onUpdate(updatedBotData);
      }
    } catch (error) {
      let errorMessage = '保存失败，请重试';
      if (error.response?.data) {
        const responseData = error.response.data;
        if (typeof responseData === 'string') {
          errorMessage = responseData;
        } else if (responseData.detail) {
          errorMessage = responseData.detail;
        } else if (responseData.message) {
          errorMessage = responseData.message;
        }
      }

      notifyError('保存失败', `机器人 "${bot.nickname || 'Unknown'}" 更新失败: ${errorMessage}`, {
        duration: 5000,
        metadata: { botId: bot.gewe_app_id, botName: bot.nickname }
      });

      setGeneralError('保存失败: ' + errorMessage);
    }
  };

  // 删除机器人
  const handleDelete = async () => {
    try {
      await executeWithLoading(async () => {
        await botService.deleteBot(bot.gewe_app_id);
      });

      success('删除成功', `机器人 "${bot.nickname || bot.gewe_app_id}" 已删除`, {
        duration: 3000,
        metadata: { botId: bot.gewe_app_id, botName: bot.nickname }
      });

      // 关闭确认弹窗和主弹窗
      setShowDeleteConfirm(false);
      handleClose();

      // 调用删除回调
      if (onDelete) {
        onDelete(bot.gewe_app_id);
      }
    } catch (error) {
      let errorMessage = '删除失败，请重试';
      if (error.response?.data) {
        const responseData = error.response.data;
        if (typeof responseData === 'string') {
          errorMessage = responseData;
        } else if (responseData.detail) {
          errorMessage = responseData.detail;
        } else if (responseData.message) {
          errorMessage = responseData.message;
        }
      }

      notifyError('删除失败', `机器人 "${bot.nickname || bot.gewe_app_id}" 删除失败: ${errorMessage}`, {
        duration: 5000,
        metadata: { botId: bot.gewe_app_id, botName: bot.nickname }
      });
    }
  };

  // 获取性别文本
  const getSexText = (sex) => {
    switch (sex) {
      case 1: return '男';
      case 2: return '女';
      default: return '未知';
    }
  };

  // 格式化时间
  const formatTime = (timestamp) => {
    if (!timestamp || timestamp === null || timestamp === undefined) return 'N/A';

    try {
      // 直接使用Date构造函数处理ISO字符串
      const date = new Date(timestamp);

      // 检查日期是否有效
      if (isNaN(date.getTime())) {
        console.warn('无效的日期:', timestamp);
        return 'N/A';
      }

      // 返回本地化的时间字符串
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch (error) {
      console.error('时间格式化错误:', error, timestamp);
      return 'N/A';
    }
  };

  // 格式化相对时间
  const formatRelativeTime = (timestamp) => {
    if (!timestamp) return 'N/A';

    try {
      const date = new Date(timestamp);
      if (isNaN(date.getTime())) return 'N/A';

      const now = new Date();
      const diff = now - date;
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);

      if (seconds < 60) return '刚刚';
      if (minutes < 60) return `${minutes}分钟前`;
      if (hours < 24) return `${hours}小时前`;
      if (days < 7) return `${days}天前`;
      if (days < 30) return `${Math.floor(days / 7)}周前`;
      if (days < 365) return `${Math.floor(days / 30)}个月前`;
      return `${Math.floor(days / 365)}年前`;
    } catch {
      return formatTime(timestamp);
    }
  };

  /**
   * 处理主弹窗关闭
   */
  const handleClose = () => {
    onClose();
  };

  // 生成复制按钮
  const CopyButton = ({ text, fieldName }) => (
    <button
      onClick={() => copyToClipboard(text)}
      className={`ml-2 p-1.5 rounded-lg transition-all duration-200 ${copiedField === fieldName
        ? 'bg-green-100 text-green-600'
        : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
        }`}
      title={copiedField === fieldName ? '已复制' : '复制'}
    >
      <motion.div
        key={copiedField === fieldName ? 'check' : 'copy'}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ duration: 0.2 }}
      >
        {copiedField === fieldName ? (
          <i className="fas fa-check h-4 w-4"></i>
        ) : (
          <i className="fas fa-copy h-4 w-4"></i>
        )}
      </motion.div>
    </button>
  );

  // 信息项组件
  const InfoItem = ({ label, value, icon, canCopy = false, fieldName }) => (
    <div className="flex flex-col space-y-1">
      <div className="flex items-center text-xs text-gray-500">
        {icon && <i className={`${icon} mr-1.5 w-4`}></i>}
        <span>{label}</span>
      </div>
      <div className="flex items-center">
        <span className="text-sm text-gray-900 font-medium">{value || 'N/A'}</span>
        {canCopy && value && <CopyButton text={value} fieldName={fieldName} />}
      </div>
    </div>
  );

  // 底部操作按钮
  const footer = (
    <>
      {isEditing ? (
        <div className="flex flex-col sm:flex-row gap-3 sm:justify-end">
          <button
            onClick={testConnection}
            disabled={testing || !editForm.gewe_app_id || !editForm.gewe_token}
            className={`inline-flex items-center px-5 py-2.5 border rounded-xl text-sm font-medium transition-all duration-200 focus:outline-none focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed ${testing
              ? 'border-purple-300 bg-purple-50 text-purple-700'
              : testPassed
                ? 'border-green-300 bg-green-50 text-green-700 hover:bg-green-100'
                : 'border-gray-200 bg-white text-gray-700 hover:bg-gray-50 hover:border-gray-300 focus:ring-gray-200'
              }`}
          >
            {testing ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="mr-2"
                >
                  <i className="fas fa-spinner h-4 w-4"></i>
                </motion.div>
                测试中...
              </>
            ) : testPassed ? (
              <>
                <i className="fas fa-check-circle mr-2 text-green-600"></i>
                测试通过
              </>
            ) : (
              <>
                <i className="fas fa-plug mr-2"></i>
                测试连接
              </>
            )}
          </button>
          <button
            onClick={saveEdit}
            disabled={!testPassed}
            className="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 border border-transparent rounded-xl text-sm font-medium text-white hover:from-purple-700 hover:to-purple-800 shadow-md hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i className="fas fa-check mr-2"></i>
            保存
          </button>
          <button
            onClick={() => {
              setIsEditing(false);
              setTestPassed(false);
              setGeneralError('');
              setEditForm({
                gewe_app_id: bot.gewe_app_id || '',
                gewe_token: bot.gewe_token || '',
                base_url: bot.base_url || 'https://www.geweapi.com/gewe/v2/api'
              });
            }}
            className="inline-flex items-center px-5 py-2.5 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
          >
            <i className="fas fa-times mr-2"></i>
            取消
          </button>
        </div>
      ) : (
        <div className="flex flex-col sm:flex-row gap-3 sm:justify-end">
          <button
            onClick={() => setIsEditing(true)}
            className="inline-flex items-center px-5 py-2.5 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
          >
            <i className="fas fa-edit mr-2"></i>
            编辑
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-red-600 to-red-700 border border-transparent rounded-xl text-sm font-medium text-white hover:from-red-700 hover:to-red-800 shadow-md hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            <i className="fas fa-trash mr-2"></i>
            删除
          </button>
        </div>
      )}
    </>
  );

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={handleClose}
        title="机器人详情"
        size="2xl"
        footer={footer}
      >
        {/* 机器人头部信息卡片 */}
        <div className={`relative rounded-2xl overflow-hidden mb-6 ${bot.sns_bg_img ? 'bg-gray-900' : 'bg-gradient-to-br from-purple-50 to-pink-50'
          }`}>
          {/* 背景图片 */}
          {bot.sns_bg_img && (
            <div className="absolute inset-0">
              <BotBackgroundImage imageUrl={bot.sns_bg_img} />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-black/20"></div>
            </div>
          )}

          {/* 机器人信息 */}
          <div className="relative z-10 p-6">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <CachedImage
                  src={bot.big_head_img_url || bot.avatar_url || '/default-avatar.png'}
                  alt={bot.nickname || '机器人头像'}
                  className="w-20 h-20 rounded-2xl object-cover shadow-xl ring-4 ring-white/90"
                />
                <div className={`absolute -bottom-1 -right-1 w-6 h-6 rounded-full border-3 border-white ${bot.is_online ? 'bg-green-500' : 'bg-gray-400'
                  } shadow-lg`}></div>
              </div>
              <div className="flex-1">
                {/* 信息容器 - 添加毛玻璃背景 */}
                <div className={`${bot.sns_bg_img
                  ? 'bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/20'
                  : ''
                  }`}>
                  <h2 className={`text-2xl font-bold mb-1 ${bot.sns_bg_img ? 'text-white drop-shadow-lg' : 'text-gray-900'
                    }`}>
                    {bot.nickname || '未设置昵称'}
                  </h2>
                  <p className={`text-sm mb-3 ${bot.sns_bg_img ? 'text-white/90 drop-shadow' : 'text-gray-600'
                    }`}>
                    {bot.signature || '这个人很懒，什么都没留下'}
                  </p>
                  <div className="flex items-center text-sm">
                    <div className={`inline-flex items-center px-3 py-1 rounded-full ${bot.is_online
                      ? bot.sns_bg_img
                        ? 'bg-green-500/20 backdrop-blur-sm text-green-100 border border-green-400/30'
                        : 'bg-green-100 text-green-700'
                      : bot.sns_bg_img
                        ? 'bg-gray-500/20 backdrop-blur-sm text-gray-100 border border-gray-400/30'
                        : 'bg-gray-100 text-gray-600'
                      }`}>
                      <i className={`fas fa-circle text-xs mr-1.5 ${bot.is_online
                        ? bot.sns_bg_img ? 'text-green-300' : 'text-green-500'
                        : bot.sns_bg_img ? 'text-gray-300' : 'text-gray-400'
                        }`}></i>
                      {bot.is_online ? '在线' : '离线'}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 信息区域 */}
        <div className="space-y-6">
          {/* 基本信息卡片 */}
          <div className="bg-gray-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
            <h3 className="flex items-center text-sm font-semibold text-gray-900 mb-4 group-hover:text-purple-700 transition-colors duration-200">
              <i className="fas fa-user-circle mr-2 text-purple-600 group-hover:scale-110 transition-transform duration-200"></i>
              基本信息
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <InfoItem
                label="微信号"
                value={bot.wxid}
                icon="fas fa-at"
                canCopy={true}
                fieldName="wxid"
              />
              <InfoItem
                label="手机号"
                value={bot.mobile}
                icon="fas fa-mobile-alt"
              />
              <InfoItem
                label="性别"
                value={getSexText(bot.sex)}
                icon="fas fa-venus-mars"
              />
              <InfoItem
                label="地区"
                value={[bot.country, bot.province, bot.city].filter(Boolean).join(' ')}
                icon="fas fa-map-marker-alt"
              />
            </div>
          </div>

          {/* Gewe信息卡片 */}
          <div className="bg-purple-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
            <h3 className="flex items-center text-sm font-semibold text-gray-900 mb-4 group-hover:text-purple-700 transition-colors duration-200">
              <i className="fas fa-robot mr-2 text-purple-600 group-hover:scale-110 transition-transform duration-200"></i>
              Gewe信息
            </h3>
            <div className="space-y-4">
              {/* App ID */}
              <div className="bg-white rounded-lg p-3">
                <label className="block text-xs font-medium text-gray-600 mb-1">App ID</label>
                <div className="flex items-center justify-between">
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.gewe_app_id}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      disabled
                    />
                  ) : (
                    <span className="text-sm font-mono text-gray-900">{bot.gewe_app_id}</span>
                  )}
                  {!isEditing && <CopyButton text={bot.gewe_app_id} fieldName="gewe_app_id" />}
                </div>
              </div>

              {/* Token */}
              <div className="bg-white rounded-lg p-3">
                <label className="block text-xs font-medium text-gray-600 mb-1">Token</label>
                <div className="flex items-center justify-between">
                  {isEditing ? (
                    <div className="flex-1 relative">
                      <input
                        type="password"
                        value={editForm.gewe_token}
                        onChange={(e) => {
                          setEditForm({ ...editForm, gewe_token: e.target.value });
                          setGeneralError('');
                          setTestPassed(false);
                        }}
                        className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg text-sm font-mono bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                        placeholder="输入新的Token"
                      />
                      {editForm.gewe_token && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="absolute right-2 top-1/2 -translate-y-1/2"
                        >
                          <i className="fas fa-key text-purple-500"></i>
                        </motion.div>
                      )}
                    </div>
                  ) : (
                    <span className="text-sm font-mono text-gray-900">••••••••••••••••</span>
                  )}
                  {!isEditing && bot.gewe_token && <CopyButton text={bot.gewe_token} fieldName="gewe_token" />}
                </div>
              </div>

              {/* Base URL */}
              <div className="bg-white rounded-lg p-3">
                <label className="block text-xs font-medium text-gray-600 mb-1">Base URL</label>
                <div className="flex items-center justify-between">
                  {isEditing ? (
                    <div className="flex-1 relative">
                      <input
                        type="url"
                        value={editForm.base_url}
                        onChange={(e) => {
                          setEditForm({ ...editForm, base_url: e.target.value });
                          setGeneralError('');
                          setTestPassed(false);
                        }}
                        className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg text-sm font-mono bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                        placeholder="输入Base URL"
                      />
                      {editForm.base_url && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="absolute right-2 top-1/2 -translate-y-1/2"
                        >
                          <i className="fas fa-link text-purple-500"></i>
                        </motion.div>
                      )}
                    </div>
                  ) : (
                    <div className="flex-1 overflow-hidden">
                      <span className="text-sm font-mono text-gray-900 block truncate" title={bot.base_url}>
                        {bot.base_url}
                      </span>
                    </div>
                  )}
                  {!isEditing && <CopyButton text={bot.base_url} fieldName="base_url" />}
                </div>
              </div>
            </div>
          </div>

          {/* 编辑模式下的状态提示 */}
          {isEditing && (
            <div className="space-y-3">
              {generalError && (
                <div className="flex items-start p-4 bg-red-50 border border-red-200 rounded-lg">
                  <i className="fas fa-exclamation-triangle text-red-500 mr-3 mt-0.5"></i>
                  <div className="flex-1">
                    <p className="text-sm text-red-700">{generalError}</p>
                  </div>
                  <button
                    onClick={() => setGeneralError('')}
                    className="text-red-400 hover:text-red-600 ml-2"
                  >
                    <i className="fas fa-times"></i>
                  </button>
                </div>
              )}

              {testPassed && (
                <div className="flex items-center p-4 bg-green-50 border border-green-200 rounded-lg">
                  <i className="fas fa-check-circle text-green-500 mr-3"></i>
                  <span className="text-sm text-green-700">连接测试通过，可以保存机器人</span>
                </div>
              )}
            </div>
          )}

          {/* 时间信息卡片 */}
          <div className="bg-blue-50 rounded-xl p-5 hover:shadow-lg transition-all duration-300 group">
            <h3 className="flex items-center text-sm font-semibold text-gray-900 mb-4 group-hover:text-blue-700 transition-colors duration-200">
              <i className="fas fa-clock mr-2 text-blue-600 group-hover:scale-110 transition-transform duration-200"></i>
              时间信息
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="bg-white rounded-lg p-3 hover:shadow-md transition-shadow duration-200 cursor-default group">
                <div className="text-xs text-gray-600 mb-1">创建时间</div>
                <div className="text-sm text-gray-900 font-medium">{formatRelativeTime(bot.created_at)}</div>
                <div className="text-xs text-gray-500 mt-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  {formatTime(bot.created_at)}
                </div>
              </div>
              <div className="bg-white rounded-lg p-3 hover:shadow-md transition-shadow duration-200 cursor-default group">
                <div className="text-xs text-gray-600 mb-1">更新时间</div>
                <div className="text-sm text-gray-900 font-medium">{formatRelativeTime(bot.updated_at)}</div>
                <div className="text-xs text-gray-500 mt-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  {formatTime(bot.updated_at)}
                </div>
              </div>
              <div className="bg-white rounded-lg p-3 sm:col-span-2 hover:shadow-md transition-shadow duration-200 cursor-default group">
                <div className="text-xs text-gray-600 mb-1 flex items-center">
                  最后在线
                  {bot.is_online && <span className="ml-2 flex items-center">
                    <span className="relative flex h-2 w-2">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                    </span>
                  </span>}
                </div>
                <div className="text-sm text-gray-900 font-medium">{formatRelativeTime(bot.last_seen_at)}</div>
                <div className="text-xs text-gray-500 mt-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  {formatTime(bot.last_seen_at)}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Modal>

      {/* 删除确认弹窗 */}
      <Modal
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        title=""
        size="sm"
        footer={
          <div className="flex gap-3 justify-end">
            <button
              onClick={() => setShowDeleteConfirm(false)}
              disabled={saving}
              className="px-4 py-2 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200 disabled:opacity-50"
            >
              取消
            </button>
            <button
              onClick={handleDelete}
              disabled={saving}
              className="px-4 py-2 bg-gradient-to-r from-red-600 to-red-700 border border-transparent rounded-xl text-sm font-medium text-white hover:from-red-700 hover:to-red-800 shadow-md hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2 inline-block"></div>
                  删除中...
                </>
              ) : (
                '确认删除'
              )}
            </button>
          </div>
        }
      >
        <div className="text-center py-4">
          <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4">
            <i className="fas fa-trash text-red-600 text-2xl"></i>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            删除机器人
          </h3>
          <p className="text-gray-600">
            确定要删除机器人 <span className="font-semibold">"{bot?.nickname || bot?.gewe_app_id}"</span> 吗？
          </p>
          <p className="text-sm text-red-600 mt-2">
            此操作不可撤销
          </p>
        </div>
      </Modal>
    </>
  );
};

export default BotDetailModal;