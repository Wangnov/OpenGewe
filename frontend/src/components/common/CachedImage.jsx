import React, { useState, useEffect } from 'react';
import { getImageAsBase64 } from '../../utils/imageProxy';

/**
 * 带缓存功能的图片组件
 * 可以替换普通的img标签，自动缓存所有网络图片
 */
const CachedImage = ({ src, alt, className, style, onLoad, onError, ...props }) => {
  const [imageSrc, setImageSrc] = useState(src);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!src) {
      setImageSrc(src);
      return;
    }

    // 如果是本地图片或data URL，直接使用
    if (src.startsWith('/') || src.startsWith('data:') || src.startsWith('blob:')) {
      setImageSrc(src);
      return;
    }

    // 对网络图片进行缓存处理
    setLoading(true);
    setError(false);
    
    getImageAsBase64(src)
      .then(cachedSrc => {
        setImageSrc(cachedSrc);
        setLoading(false);
      })
      .catch(err => {
        console.error('CachedImage加载失败:', err);
        setImageSrc(src); // 回退到原始URL
        setError(true);
        setLoading(false);
      });
  }, [src]);

  const handleLoad = (e) => {
    setLoading(false);
    if (onLoad) onLoad(e);
  };

  const handleError = (e) => {
    setError(true);
    setLoading(false);
    if (onError) onError(e);
  };

  return (
    <img
      src={imageSrc}
      alt={alt}
      className={className}
      style={style}
      onLoad={handleLoad}
      onError={handleError}
      {...props}
    />
  );
};

export default CachedImage;