import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
// Font Awesome icons are loaded via CDN in index.html
import LoadingSpinner from '../common/LoadingSpinner';
import useApiLoading from '../../hooks/useApiLoading';
import CachedImage from '../common/CachedImage';
import useNotification from '../../hooks/useNotification';
import botService from '../../services/botService';

/**
 * 创建机器人弹窗组件
 * @param {Object} props - 组件属性
 * @param {boolean} props.isOpen - 是否打开弹窗
 * @param {Function} props.onClose - 关闭弹窗回调
 * @param {Function} props.onSuccess - 创建成功回调
 * @returns {JSX.Element} 创建机器人弹窗组件
 */
const CreateBotModal = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    gewe_app_id: '',
    gewe_token: '',
    nickname: '',
    remark: '',
    base_url: 'https://www.geweapi.com/gewe/v2/api'
  });
  const [testing, setTesting] = useState(false);
  const [testPassed, setTestPassed] = useState(false);
  const [creating, setCreating] = useState(false);
  const [errors, setErrors] = useState({});
  const [generalError, setGeneralError] = useState('');
  const [isClosing, setIsClosing] = useState(false);
  const { loading: apiLoading, executeWithLoading } = useApiLoading();
  const { success, error: notifyError } = useNotification();
  const backdropRef = useRef(null);
  const contentRef = useRef(null);

  // 重置表单
  const resetForm = () => {
    setFormData({
      gewe_app_id: '',
      gewe_token: '',
      nickname: '',
      remark: '',
      base_url: 'https://www.geweapi.com/gewe/v2/api'
    });
    setTesting(false);
    setTestPassed(false);
    setCreating(false);
    setErrors({});
    setGeneralError('');
  };

  // 表单验证
  const validateForm = () => {
    const newErrors = {};

    if (!formData.gewe_app_id.trim()) {
      newErrors.gewe_app_id = 'App ID不能为空';
    }

    if (!formData.gewe_token.trim()) {
      newErrors.gewe_token = 'Token不能为空';
    }

    if (!formData.base_url.trim()) {
      newErrors.base_url = 'Base URL不能为空';
    } else if (!isValidUrl(formData.base_url)) {
      newErrors.base_url = '请输入有效的URL';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // URL验证
  const isValidUrl = (string) => {
    try {
      new URL(string);
      return true;
    } catch {
      return false;
    }
  };

  // 处理输入变化
  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // 清除该字段的错误
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
    // 清除通用错误
    if (generalError) {
      setGeneralError('');
    }
    // 如果修改了关键字段，重置测试状态
    if (['gewe_app_id', 'gewe_token', 'base_url'].includes(field)) {
      setTestPassed(false);
    }
  };

  /**
   * 处理关闭弹窗
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
        resetForm();
        onClose(); // 真正关闭弹窗
      };

      contentRef.current.addEventListener('animationend', handleAnimationEnd);

      // 备用：如果动画事件没有触发，使用定时器
      setTimeout(() => {
        if (contentRef.current) {
          contentRef.current.removeEventListener('animationend', handleAnimationEnd);
          setIsClosing(false);
          resetForm();
          onClose();
        }
      }, 300);
    } else {
      // 如果DOM元素不存在，直接关闭
      setIsClosing(false);
      resetForm();
      onClose();
    }
  };

  /**
   * 处理蒙版点击
   */
  const handleBackdropClick = (e) => {
    // 确保点击的是蒙版本身，而不是内容区域
    if (e.target === e.currentTarget) {
      handleClose();
    }
  };

  // 重置关闭状态
  useEffect(() => {
    if (isOpen) {
      setIsClosing(false);
    }
  }, [isOpen]);

  // 测试连接
  const testConnection = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      setTesting(true);
      setTestPassed(false);

      // 使用加载管理器调用测试API
      await executeWithLoading(async () => {
        await botService.testBotConnection({
          gewe_app_id: formData.gewe_app_id,
          gewe_token: formData.gewe_token,
          base_url: formData.base_url
        });
      });

      setTestPassed(true);
      success('连接测试成功！可以保存机器人了');
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
        errorMessage = `连接测试失败: ${error.message || '未知错误'}`;
      }

      // 限制错误消息长度
      if (errorMessage.length > 200) {
        errorMessage = errorMessage.substring(0, 200) + '...';
      }

      setGeneralError(errorMessage);
      notifyError('测试失败', errorMessage, {
        duration: 5000,
        actions: [{
          label: '重试',
          onClick: testConnection,
          variant: 'primary'
        }]
      });
    } finally {
      setTesting(false);
    }
  };

  // 创建机器人
  const createBot = async () => {
    if (!testPassed || !validateForm()) {
      return;
    }

    try {
      setCreating(true);

      await executeWithLoading(async () => {
        await botService.createBot(formData);
      });

      success('机器人创建成功', `机器人 "${formData.nickname || formData.gewe_app_id}" 已创建`, {
        duration: 3000,
        metadata: { botId: formData.gewe_app_id, botName: formData.nickname }
      });

      onSuccess?.();
      handleClose();
    } catch (error) {
      console.error('创建机器人失败:', error);

      let errorMessage = '创建机器人失败';

      try {
        if (error.response?.data) {
          const responseData = error.response.data;

          if (typeof responseData === 'string') {
            errorMessage = responseData;
          } else if (responseData.detail) {
            errorMessage = responseData.detail;
          } else if (responseData.message) {
            errorMessage = responseData.message;
          } else if (responseData.error) {
            errorMessage = responseData.error;
          } else {
            errorMessage = JSON.stringify(responseData);
          }
        } else if (error.message) {
          errorMessage = error.message;
        }
      } catch (parseError) {
        console.error('解析错误消息失败:', parseError);
        errorMessage = `创建失败: ${error.message || '未知错误'}`;
      }

      if (errorMessage.length > 200) {
        errorMessage = errorMessage.substring(0, 200) + '...';
      }

      setGeneralError(errorMessage);
      notifyError('创建失败', errorMessage, {
        duration: 5000,
        metadata: { botId: formData.gewe_app_id, botName: formData.nickname },
        actions: [{
          label: '重试',
          onClick: createBot,
          variant: 'primary'
        }]
      });
    } finally {
      setCreating(false);
    }
  };

  if (!isOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* 背景遮罩 */}
        <div
          ref={backdropRef}
          className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity animate-modal-backdrop-enter"
          onClick={handleBackdropClick}
        />

        {/* 弹窗内容 */}
        <div
          ref={contentRef}
          className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all relative sm:my-8 sm:align-middle sm:max-w-lg sm:w-full animate-modal-content-enter"
          onClick={(e) => e.stopPropagation()}
        >
          {/* 显示加载遮罩 */}
          {(apiLoading || testing || creating) && (
            <div className="absolute inset-0 bg-white bg-opacity-80 backdrop-blur-sm flex items-center justify-center z-50">
              <LoadingSpinner
                size="md"
                text={testing ? '测试连接中...' : creating ? '创建中...' : '处理中...'}
              />
            </div>
          )}

          {/* 弹窗头部 */}
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                新建机器人
              </h3>
              <button
                onClick={handleClose}
                disabled={isClosing}
                className="text-gray-400 hover:text-gray-600 focus:outline-none disabled:opacity-50"
              >
                <i className="fas fa-times h-6 w-6 align-middle"></i>
              </button>
            </div>

            {/* 表单内容 */}
            <div className="space-y-4">
              {/* App ID */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  GeWe App ID <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={formData.gewe_app_id}
                  onChange={(e) => handleInputChange('gewe_app_id', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent ${errors.gewe_app_id ? 'border-red-300' : 'border-gray-300'
                    }`}
                  placeholder="请输入GeWe App ID"
                />
                {errors.gewe_app_id && (
                  <p className="mt-1 text-sm text-red-600">{errors.gewe_app_id}</p>
                )}
              </div>

              {/* Token */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  GeWe Token <span className="text-red-500">*</span>
                </label>
                <input
                  type="password"
                  value={formData.gewe_token}
                  onChange={(e) => handleInputChange('gewe_token', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent ${errors.gewe_token ? 'border-red-300' : 'border-gray-300'
                    }`}
                  placeholder="请输入GeWe Token"
                />
                {errors.gewe_token && (
                  <p className="mt-1 text-sm text-red-600">{errors.gewe_token}</p>
                )}
              </div>

              {/* Base URL */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Base URL <span className="text-red-500">*</span>
                </label>
                <input
                  type="url"
                  value={formData.base_url}
                  onChange={(e) => handleInputChange('base_url', e.target.value)}
                  className={`w-full px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent ${errors.base_url ? 'border-red-300' : 'border-gray-300'
                    }`}
                  placeholder="请输入Base URL"
                />
                {errors.base_url && (
                  <p className="mt-1 text-sm text-red-600">{errors.base_url}</p>
                )}
                <p className="mt-1 text-xs text-gray-500">
                  默认: https://www.geweapi.com/gewe/v2/api
                </p>
              </div>

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
          </div>

          {/* 弹窗底部操作按钮 */}
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <div className="flex space-x-3">
              {/* 测试按钮 */}
              <button
                onClick={testConnection}
                disabled={testing || !formData.gewe_app_id || !formData.gewe_token || !formData.base_url}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {testing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600 mr-2"></div>
                    测试中...
                  </>
                ) : (
                  '测试连接'
                )}
              </button>

              {/* 保存按钮 */}
              <button
                onClick={createBot}
                disabled={!testPassed || creating}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {creating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    创建中...
                  </>
                ) : (
                  <>
                    <i className="fas fa-check h-4 w-4 mr-2 flex items-center"></i>
                    保存
                  </>
                )}
              </button>

              {/* 取消按钮 */}
              <button
                onClick={handleClose}
                disabled={creating || isClosing}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i className="fas fa-times-circle h-4 w-4 mr-2 flex items-center"></i>
                取消
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>,
    document.body
  );
};

export default CreateBotModal;