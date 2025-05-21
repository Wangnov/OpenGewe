import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconProp, SizeProp } from '@fortawesome/fontawesome-svg-core';
import { findIconDefinition, IconName, IconPrefix } from '@fortawesome/fontawesome-svg-core';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';

// 添加所有图标到库
library.add(fas, fab, far);

// 图标样式类型
type IconStyle = 'solid' | 'regular' | 'brands';

// 图标选项类型
interface IconOptions {
  size?: SizeProp; // 使用正确的SizeProp类型
  className?: string;
  color?: string;
  spin?: boolean;
  fixedWidth?: boolean;
}

// 将数字转换为SizeProp
const numToSize = (num?: number): SizeProp | undefined => {
  if (num === undefined) return undefined;
  
  // FontAwesome只接受特定的尺寸字符串
  if (num <= 12) return 'xs';
  if (num <= 14) return 'sm';
  if (num <= 16) return 'lg';
  if (num <= 20) return 'xl';
  if (num <= 24) return '2x';
  if (num <= 36) return '3x';
  if (num <= 48) return '4x';
  if (num <= 64) return '5x';
  return '6x';
};

// 图标加载器
export const Icons = {
  /**
   * 获取图标组件
   * @param name 图标名称
   * @param style 图标样式 ('solid', 'regular', 'brands')
   * @param options 图标选项
   * @returns 图标React组件
   */
  icon(name: string, style: IconStyle = 'solid', options: IconOptions & { size?: number | SizeProp } = {}) {
    // 处理数字尺寸
    let sizeValue: SizeProp | undefined = undefined;
    if (typeof options.size === 'number') {
      sizeValue = numToSize(options.size as number);
    } else {
      sizeValue = options.size as SizeProp | undefined;
    }
    
    // 确保name是有效的IconName
    const iconName = name as IconName;
    
    // 根据样式确定前缀
    let prefix: IconPrefix;
    switch (style) {
      case 'solid':
        prefix = 'fas';
        break;
      case 'regular':
        prefix = 'far';
        break;
      case 'brands':
        prefix = 'fab';
        break;
      default:
        prefix = 'fas';
    }
    
    // 查找图标定义
    const iconDefinition = findIconDefinition({ prefix, iconName });
    
    if (!iconDefinition) {
      console.warn(`Icon not found: ${prefix} ${iconName}`);
      return null;
    }
    
    // 返回FontAwesomeIcon组件
    return (
      <FontAwesomeIcon
        icon={[prefix, iconName]}
        size={sizeValue}
        className={options.className}
        color={options.color}
        spin={options.spin}
        fixedWidth={options.fixedWidth}
      />
    );
  }
}; 