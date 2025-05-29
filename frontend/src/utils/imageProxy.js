/**
 * 图片代理工具函数
 * 解决微信图片防盗链问题
 */

import { useState, useEffect } from 'react';
import api from '../services/api';

// 图片缓存Map，用于存储已获取的base64图片
const imageCache = new Map();

/**
 * 检查是否需要代理的图片URL
 * @param {string} url - 图片URL
 * @returns {boolean} 是否需要代理
 */
export const needsProxy = (url) => {
  if (!url || typeof url !== 'string') return false;
  
  const wechatDomains = [
    'shmmsns.qpic.cn',
    'mmsns.qpic.cn',
    'wx.qlogo.cn',
    'thirdwx.qlogo.cn',
    'weixin.qq.com',
    'res.wx.qq.com'
  ];
  
  return wechatDomains.some(domain => url.includes(domain));
};

/**
 * 获取代理后的图片URL
 * @param {string} originalUrl - 原始图片URL
 * @returns {string} 代理后的URL
 */
export const getProxiedImageUrl = (originalUrl) => {
  if (!originalUrl || !needsProxy(originalUrl)) {
    return originalUrl;
  }
  
  // 构造代理URL - 使用相对路径避免重复的baseURL
  const proxyUrl = `/api/v1/proxy/image?url=${encodeURIComponent(originalUrl)}`;
  
  return proxyUrl;
};

/**
 * 获取base64格式的图片数据
 * @param {string} originalUrl - 原始图片URL
 * @returns {Promise<string>} base64格式的图片数据
 */
export const getImageAsBase64 = async (originalUrl) => {
  // 检查缓存中是否已有该图片（对所有图片都进行缓存）
  if (imageCache.has(originalUrl)) {
    console.log('从缓存加载图片:', originalUrl);
    return imageCache.get(originalUrl);
  }
  
  // 如果不需要代理，直接获取图片并缓存
  if (!originalUrl || !needsProxy(originalUrl)) {
    try {
      const response = await fetch(originalUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const blob = await response.blob();
      const base64Result = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
      
      // 将结果存入缓存
      imageCache.set(originalUrl, base64Result);
      console.log('普通图片已缓存:', originalUrl);
      
      return base64Result;
    } catch (error) {
      console.error('获取普通图片失败:', error);
      // 如果获取失败，回退到原始URL
      imageCache.set(originalUrl, originalUrl); // 缓存原始URL避免重复请求
      return originalUrl;
    }
  }
  
  // 需要代理的图片
  try {
    // 从localStorage获取access_token
    const accessToken = localStorage.getItem('access_token');
    
    const response = await fetch(getProxiedImageUrl(originalUrl), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const blob = await response.blob();
    const base64Result = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
    
    // 将结果存入缓存
    imageCache.set(originalUrl, base64Result);
    console.log('代理图片已缓存:', originalUrl);
    
    return base64Result;
  } catch (error) {
    console.error('获取代理图片失败:', error);
    // 如果代理失败，回退到原始URL
    imageCache.set(originalUrl, originalUrl); // 缓存原始URL避免重复请求
    return originalUrl;
  }
};

/**
 * React Hook：处理图片代理
 * @param {string} originalUrl - 原始图片URL
 * @param {boolean} useBase64 - 是否使用base64格式（默认false）
 * @returns {Object} { imageUrl, loading, error }
 */
export const useProxiedImage = (originalUrl, useBase64 = false) => {
  const [imageUrl, setImageUrl] = useState(originalUrl);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!originalUrl || !needsProxy(originalUrl)) {
      setImageUrl(originalUrl);
      return;
    }
    
    if (useBase64) {
      setLoading(true);
      setError(null);
      
      getImageAsBase64(originalUrl)
        .then(base64Url => {
          setImageUrl(base64Url);
        })
        .catch(err => {
          console.error('加载代理图片失败:', err);
          setError(err);
          setImageUrl(originalUrl); // 回退到原始URL
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setImageUrl(getProxiedImageUrl(originalUrl));
    }
  }, [originalUrl, useBase64]);
  
  return { imageUrl, loading, error };
};

export default {
  needsProxy,
  getProxiedImageUrl,
  getImageAsBase64,
  useProxiedImage
};