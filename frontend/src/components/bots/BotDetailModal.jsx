import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
// Font Awesome icons are loaded via CDN in index.html
import botService from '../../services/botService';
import LoadingSpinner from '../common/LoadingSpinner';
import CachedImage from '../common/CachedImage';
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
  const [isClosing, setIsClosing] = useState(false);
  const { loading: saving, executeWithLoading } = useApiLoading();
  const { success, error: notifyError } = useNotification();
  const backdropRef = useRef(null);
  const contentRef = useRef(null);

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
      // 详细的错误调试日志
      console.error('连接测试失败 - 完整错误对象:', error);
      console.error('错误响应数据:', error.response?.data);
      console.error('错误状态码:', error.response?.status);
      console.error('错误消息:', error.message);

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
      } catch (parseError) {
        console.error('解析错误消息失败:', parseError);
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
      await executeWithLoading(async () => {
        await botService.updateBot(bot.gewe_app_id, {
          gewe_token: editForm.gewe_token,
          base_url: editForm.base_url
        });
      });

      setIsEditing(false);
      setTestPassed(false);
      setGeneralError(''); // 清除错误状态

      success('保存成功', `机器人 "${bot.nickname || 'Unknown'}" 信息已更新`, {
        duration: 3000,
        metadata: { botId: bot.gewe_app_id, botName: bot.nickname }
      });

      // 调用更新回调
      if (onUpdate) {
        onUpdate();
      }
    } catch (error) {
      console.error('保存失败:', error);

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
      console.error('删除失败:', error);

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
    if (!timestamp) return 'N/A';
    return new Date(timestamp * 1000).toLocaleString('zh-CN');
  };

  /**
   * 处理主弹窗关闭
   */
  const handleClose = () => {
    if (isClosing) return; // 防止重复触发

    setIsClosing(true);

    // 添加退出动画类
    if (backdropRef.current && contentRef.current) {
      backdropRef.current.classList.add('animate-modal-backdrop-exit');
      backdropRef.current.classList.remove('animate-modal-backdrop-enter');

      contentRef.current.classList.add('animate-modal-content-exit');
      contentRef.current.classList.remove('animate-modal-content-enter');

      // 监听动画结束事件
      const handleAnimationEnd = () => {
        contentRef.current?.removeEventListener('animationend', handleAnimationEnd);
        setIsClosing(false);
        onClose(); // 真正关闭弹窗
      };

      contentRef.current.addEventListener('animationend', handleAnimationEnd);

      // 备用：如果动画事件没有触发，使用定时器
      setTimeout(() => {
        if (contentRef.current) {
          contentRef.current.removeEventListener('animationend', handleAnimationEnd);
          setIsClosing(false);
          onClose();
        }
      }, 300);
    } else {
      // 如果DOM元素不存在，直接关闭
      setIsClosing(false);
      onClose();
    }
  };

  // 重置关闭状态
  useEffect(() => {
    if (isOpen) {
      setIsClosing(false);
    }
  }, [isOpen]);

  // 动画变体
  const backdropVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { duration: 0.3, ease: "easeOut" }
    },
    exit: {
      opacity: 0,
      transition: { duration: 0.2, ease: "easeIn" }
    }
  };

  const modalVariants = {
    hidden: {
      opacity: 0,
      scale: 0.9,
      y: 20
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: "easeOut"
      }
    },
    exit: {
      opacity: 0,
      scale: 0.95,
      y: 10,
      transition: {
        duration: 0.2,
        ease: "easeIn"
      }
    }
  };

  const confirmModalVariants = {
    hidden: {
      opacity: 0,
      scale: 0.8,
      y: 30
    },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        duration: 0.25,
        ease: "easeOut"
      }
    },
    exit: {
      opacity: 0,
      scale: 0.9,
      y: 20,
      transition: {
        duration: 0.2,
        ease: "easeIn"
      }
    }
  };

  if (!isOpen || !bot) return null;

  return createPortal(
    <AnimatePresence mode="wait">
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 overflow-y-auto"
          initial="hidden"
          animate="visible"
          exit="exit"
        >
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            {/* 背景遮罩 */}
            <motion.div
              ref={backdropRef}
              variants={backdropVariants}
              className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity animate-modal-backdrop-enter"
              onClick={(e) => e.target === e.currentTarget && handleClose()}
            />

            {/* 弹窗内容 */}
            <motion.div
              ref={contentRef}
              variants={modalVariants}
              className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all relative sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full animate-modal-content-enter"
            >
              {/* 显示加载遮罩 */}
              {(saving || testing) && (
                <div className="absolute inset-0 bg-white bg-opacity-80 backdrop-blur-sm flex items-center justify-center z-50">
                  <LoadingSpinner
                    size="md"
                    text={testing ? '测试连接中...' : '保存中...'}
                  />
                </div>
              )}

              {/* 弹窗头部 */}
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    机器人详情
                  </h3>
                  <button
                    onClick={handleClose}
                    disabled={isClosing}
                    className="text-gray-400 hover:text-gray-600 focus:outline-none disabled:opacity-50"
                  >
                    <i className="fas fa-times h-6 w-6 align-middle"></i>
                  </button>
                </div>

                {/* 机器人卡片 */}
                <div className="relative bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 rounded-lg overflow-hidden mb-6 h-48">
                  {/* SNS背景图 */}
                  {bot.sns_bg_img && (
                    <div className="absolute inset-0">
                      <BotBackgroundImage imageUrl={bot.sns_bg_img} />
                    </div>
                  )}

                  {/* 用户信息区域 */}
                  <div className="absolute bottom-0 left-0 right-0 backdrop-blur-md bg-white bg-opacity-20 p-4 rounded-none">
                    <div className="flex items-center space-x-4">
                      <CachedImage
                        src={bot.big_head_img_url || bot.avatar_url || '/default-avatar.png'}
                        alt={bot.nickname || '机器人头像'}
                        className="w-16 h-16 rounded-full object-cover shadow-lg"
                      />
                      <div className="flex-1">
                        <h4 className="text-xl font-bold text-gray-900">
                          {bot.nickname || '未设置昵称'}
                        </h4>
                        <p className="text-gray-600">{bot.signature || '这个人很懒，什么都没留下'}</p>
                        <div className="flex items-center mt-2">
                          <div className={`w-3 h-3 rounded-full mr-2 ${bot.is_online ? 'bg-green-500' : 'bg-gray-400'
                            }`}></div>
                          <span className="text-sm text-gray-600">
                            {bot.is_online ? '在线' : '离线'}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* 详细信息 */}
                <div className="space-y-4">
                  {/* 基本信息 */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">微信号</label>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-900">{bot.wxid || 'N/A'}</span>
                        {bot.wxid && (
                          <button
                            onClick={() => copyToClipboard(bot.wxid)}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            {copiedField === 'wxid' ? (
                              <i className="fas fa-check h-4 w-4 text-green-500 "></i>
                            ) : (
                              <i className="fas fa-copy h-4 w-4 text-gray-400 "></i>
                            )}
                          </button>
                        )}
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">手机号</label>
                      <span className="text-sm text-gray-900">{bot.mobile || 'N/A'}</span>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">性别</label>
                      <span className="text-sm text-gray-900">{getSexText(bot.sex)}</span>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">地区</label>
                      <span className="text-sm text-gray-900">
                        {[bot.country, bot.province, bot.city].filter(Boolean).join(' ') || 'N/A'}
                      </span>
                    </div>
                  </div>

                  {/* Gewe信息 */}
                  <div className="border-t pt-4">
                    <h5 className="text-sm font-medium text-gray-700 mb-3">Gewe信息</h5>
                    <div className="space-y-3">
                      {/* App ID */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">App ID</label>
                        <div className="flex items-center space-x-2">
                          {isEditing ? (
                            <input
                              type="text"
                              value={editForm.gewe_app_id}
                              onChange={(e) => {
                                setEditForm({ ...editForm, gewe_app_id: e.target.value });
                                setGeneralError(''); // 清除错误状态
                                setTestPassed(false); // 重置测试状态
                              }}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                              disabled
                            />
                          ) : (
                            <>
                              <span className="text-sm text-gray-900 font-mono">{bot.gewe_app_id}</span>
                              <button
                                onClick={() => copyToClipboard(bot.gewe_app_id)}
                                className="p-1 hover:bg-gray-100 rounded"
                              >
                                {copiedField === 'gewe_app_id' ? (
                                  <i className="fas fa-check h-4 w-4 text-green-500 "></i>
                                ) : (
                                  <i className="fas fa-copy h-4 w-4 text-gray-400 "></i>
                                )}
                              </button>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Token */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Token</label>
                        <div className="flex items-center space-x-2">
                          {isEditing ? (
                            <input
                              type="password"
                              value={editForm.gewe_token}
                              onChange={(e) => {
                                setEditForm({ ...editForm, gewe_token: e.target.value });
                                setGeneralError(''); // 清除错误状态
                                setTestPassed(false); // 重置测试状态
                              }}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                              placeholder="输入新的Token"
                            />
                          ) : (
                            <>
                              <span className="text-sm text-gray-900 font-mono">••••••••••••••••</span>
                              <button
                                onClick={() => copyToClipboard(bot.gewe_token)}
                                className="p-1 hover:bg-gray-100 rounded"
                              >
                                {copiedField === 'gewe_token' ? (
                                  <i className="fas fa-check h-4 w-4 text-green-500 "></i>
                                ) : (
                                  <i className="fas fa-copy h-4 w-4 text-gray-400 "></i>
                                )}
                              </button>
                            </>
                          )}
                        </div>
                      </div>

                      {/* Base URL */}
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
                        <div className="flex items-center space-x-2">
                          {isEditing ? (
                            <input
                              type="url"
                              value={editForm.base_url}
                              onChange={(e) => {
                                setEditForm({ ...editForm, base_url: e.target.value });
                                setGeneralError(''); // 清除错误状态
                                setTestPassed(false); // 重置测试状态
                              }}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                              placeholder="输入Base URL"
                            />
                          ) : (
                            <>
                              <span className="text-sm text-gray-900 font-mono">{bot.base_url}</span>
                              <button
                                onClick={() => copyToClipboard(bot.base_url)}
                                className="p-1 hover:bg-gray-100 rounded"
                              >
                                {copiedField === 'base_url' ? (
                                  <i className="fas fa-check h-4 w-4 text-green-500 "></i>
                                ) : (
                                  <i className="fas fa-copy h-4 w-4 text-gray-400 "></i>
                                )}
                              </button>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* 编辑模式下的错误和状态显示 */}
                  {isEditing && (
                    <div className="space-y-3">
                      {/* 通用错误显示 */}
                      {generalError && (
                        <div className="flex items-start p-3 bg-red-50 border border-red-200 rounded-md">
                          <i className="fas fa-exclamation-triangle h-5 w-5 text-red-500 mr-2 flex-shrink-0 mt-0.5"></i>
                          <div className="flex-1">
                            <span className="text-sm text-red-700 break-words">{generalError}</span>
                            <button
                              onClick={() => setGeneralError('')}
                              className="ml-2 text-red-400 hover:text-red-600 focus:outline-none"
                            >
                              <i className="fas fa-times h-4 w-4"></i>
                            </button>
                          </div>
                        </div>
                      )}

                      {/* 测试状态提示 */}
                      {testPassed && (
                        <div className="flex items-center p-3 bg-green-50 border border-green-200 rounded-md">
                          <i className="fas fa-check h-5 w-5 text-green-500 mr-2 flex items-center"></i>
                          <span className="text-sm text-green-700">连接测试通过，可以保存机器人</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* 时间信息 */}
                  <div className="border-t pt-4">
                    <h5 className="text-sm font-medium text-gray-700 mb-3">时间信息</h5>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">创建时间:</span>
                        <span className="ml-2 text-gray-900">{formatTime(bot.created_at)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">更新时间:</span>
                        <span className="ml-2 text-gray-900">{formatTime(bot.updated_at)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">最后在线:</span>
                        <span className="ml-2 text-gray-900">{formatTime(bot.last_seen_at)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">资料更新:</span>
                        <span className="ml-2 text-gray-900">{formatTime(bot.profile_updated_at)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* 弹窗底部操作按钮 */}
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                {isEditing ? (
                  <div className="flex space-x-3">
                    <button
                      onClick={testConnection}
                      disabled={testing || !editForm.gewe_app_id || !editForm.gewe_token}
                      className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {testing ? '测试中...' : '测试连接'}
                    </button>
                    <button
                      onClick={saveEdit}
                      disabled={!testPassed}
                      className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <i className="fas fa-check h-4 w-4 mr-2 flex items-center"></i>
                      保存
                    </button>
                    <button
                      onClick={() => {
                        setIsEditing(false);
                        setTestPassed(false);
                        setGeneralError(''); // 清除错误状态
                        setEditForm({
                          gewe_app_id: bot.gewe_app_id || '',
                          gewe_token: bot.gewe_token || '',
                          base_url: bot.base_url || 'https://www.geweapi.com/gewe/v2/api'
                        });
                      }}
                      className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    >
                      <i className="fas fa-times-circle h-4 w-4 mr-2 flex items-center"></i>
                      取消
                    </button>
                  </div>
                ) : (
                  <div className="flex space-x-3">
                    <button
                      onClick={() => setIsEditing(true)}
                      className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                    >
                      <i className="fas fa-edit h-4 w-4 mr-2 flex items-center"></i>
                      编辑
                    </button>
                    <button
                      onClick={() => setShowDeleteConfirm(true)}
                      className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      <i className="fas fa-trash h-4 w-4 mr-2 flex items-center"></i>
                      删除
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          </div>

          {/* 删除确认弹窗 */}
          <AnimatePresence>
            {showDeleteConfirm && (
              <motion.div
                className="fixed inset-0 z-60 overflow-y-auto"
                initial="hidden"
                animate="visible"
                exit="exit"
              >
                <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                  <motion.div
                    variants={backdropVariants}
                    className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
                    onClick={(e) => e.target === e.currentTarget && setShowDeleteConfirm(false)}
                  />
                  <motion.div
                    variants={confirmModalVariants}
                    className="inline-block align-middle bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all relative sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
                  >
                    <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                      <div className="sm:flex sm:items-start">
                        <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                          <i className="fas fa-trash h-6 w-6 text-red-600 flex items-center justify-center"></i>
                        </div>
                        <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                          <h3 className="text-lg leading-6 font-medium text-gray-900">
                            删除机器人
                          </h3>
                          <div className="mt-2">
                            <p className="text-sm text-gray-500">
                              确定要删除机器人 "{bot.nickname || bot.gewe_app_id}" 吗？此操作不可撤销。
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                      <button
                        onClick={handleDelete}
                        disabled={saving}
                        className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
                      >
                        {saving ? '删除中...' : '确认删除'}
                      </button>
                      <button
                        onClick={() => setShowDeleteConfirm(false)}
                        disabled={saving}
                        className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
                      >
                        取消
                      </button>
                    </div>
                  </motion.div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      )}
    </AnimatePresence>,
    document.body
  );
};

export default BotDetailModal;