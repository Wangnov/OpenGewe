import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
// Font Awesome icons are loaded via CDN in index.html
import botService from '../../services/botService';
import { toast } from 'react-hot-toast';

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

  // 复制文本到剪贴板
  const copyToClipboard = async (text, fieldName) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(fieldName);
      toast.success('复制成功');
      setTimeout(() => setCopiedField(null), 2000);
    } catch (error) {
      console.error('复制失败:', error);
      toast.error('复制失败');
    }
  };

  // 测试机器人连接
  const testConnection = async () => {
    try {
      setTesting(true);
      setTestPassed(false);

      // 调用测试API
      await botService.testBotConnection({
        gewe_app_id: editForm.gewe_app_id,
        gewe_token: editForm.gewe_token,
        base_url: editForm.base_url
      });

      setTestPassed(true);
      toast.success('连接测试成功');
    } catch (error) {
      console.error('连接测试失败:', error);
      toast.error('连接测试失败: ' + (error.response?.data?.detail || error.message));
      setTestPassed(false);
    } finally {
      setTesting(false);
    }
  };

  // 保存编辑
  const saveEdit = async () => {
    if (!testPassed) {
      toast.error('请先通过连接测试');
      return;
    }

    try {
      await botService.updateBot(bot.gewe_app_id, {
        gewe_token: editForm.gewe_token,
        base_url: editForm.base_url
      });

      toast.success('机器人信息更新成功');
      setIsEditing(false);
      setTestPassed(false);
      onUpdate();
    } catch (error) {
      console.error('更新机器人失败:', error);
      toast.error('更新机器人失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  // 删除机器人
  const handleDelete = async () => {
    try {
      await onDelete(bot.gewe_app_id);
      setShowDeleteConfirm(false);
      onClose();
    } catch (error) {
      console.error('删除机器人失败:', error);
    }
  };

  // 格式化时间
  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    return new Date(timeString).toLocaleString('zh-CN');
  };

  // 获取性别文本
  const getSexText = (sex) => {
    switch (sex) {
      case 1: return '男';
      case 2: return '女';
      default: return '未知';
    }
  };

  if (!isOpen || !bot) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* 背景遮罩 */}
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>

        {/* 弹窗内容 */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          {/* 弹窗头部 */}
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                机器人详情
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 focus:outline-none">
                <i className="fas fa-times h-6 w-6 align-middle"></i>
              </button>
            </div>
            {/* 机器人卡片 */}
            <div className="bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 rounded-lg overflow-hidden mb-6">
              {/* SNS背景图 */}
              {bot.sns_bg_img && (
                <div
                  className="h-32 bg-cover bg-center"
                  style={{ backgroundImage: `url(${bot.sns_bg_img})` }}
                ></div>
              )}

              {/* 用户信息区域 */}
              <div className="bg-white bg-opacity-90 p-4">
                <div className="flex items-center space-x-4">
                  <img
                    src={bot.big_head_img_url || bot.avatar_url || '/default-avatar.png'}
                    alt={bot.nickname || '机器人头像'}
                    className="w-16 h-16 rounded-full object-cover border-4 border-white shadow-lg"
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
                        onClick={() => copyToClipboard(bot.wxid, 'wxid')}
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
                          onChange={(e) => setEditForm({ ...editForm, gewe_app_id: e.target.value })}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                          disabled
                        />
                      ) : (
                        <>
                          <span className="text-sm text-gray-900 font-mono">{bot.gewe_app_id}</span>
                          <button
                            onClick={() => copyToClipboard(bot.gewe_app_id, 'app_id')}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            {copiedField === 'app_id' ? (
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
                          onChange={(e) => setEditForm({ ...editForm, gewe_token: e.target.value })}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                          placeholder="输入新的Token"
                        />
                      ) : (
                        <>
                          <span className="text-sm text-gray-900 font-mono">••••••••••••••••</span>
                          <button
                            onClick={() => copyToClipboard(bot.gewe_token, 'token')}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            {copiedField === 'token' ? (
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
                          onChange={(e) => setEditForm({ ...editForm, base_url: e.target.value })}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                          placeholder="输入Base URL"
                        />
                      ) : (
                        <>
                          <span className="text-sm text-gray-900 font-mono">{bot.base_url}</span>
                          <button
                            onClick={() => copyToClipboard(bot.base_url, 'base_url')}
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
        </div>
      </div>

      {/* 删除确认弹窗 */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 z-60 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                    <i className="fas fa-trash h-6 w-6 text-red-600 flex items-center"></i>
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
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  确认删除
                </button>
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  取消
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>,
    document.body
  );
};

export default BotDetailModal;