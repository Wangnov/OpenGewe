import { createTheme } from '@mantine/core';

// 创建Mantine主题
export const theme = createTheme({
  // 设置主色调
  primaryColor: 'blue',
  
  // 自定义字体
  fontFamily: 'Inter, sans-serif',
  
  // 设置元素圆角
  radius: {
    xs: '2px',
    sm: '4px',
    md: '8px',
    lg: '16px',
    xl: '32px',
  },
  
  // 设置阴影
  shadows: {
    xs: '0 1px 2px rgba(0, 0, 0, 0.05)',
    sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px rgba(0, 0, 0, 0.1)',
  },
  
  // 其他主题配置
  components: {
    Button: {
      defaultProps: {
        radius: 'md',
      },
    },
    Card: {
      defaultProps: {
        shadow: 'sm',
        radius: 'md',
        p: 'lg',
      },
    },
  },
  
  // 自定义颜色
  colors: {
    // 品牌蓝色
    'brand-blue': [
      '#E6F7FF',
      '#BAE7FF',
      '#91D5FF',
      '#69C0FF',
      '#40A9FF',
      '#1890FF',
      '#096DD9',
      '#0050B3',
      '#003A8C',
      '#002766',
    ],
    // 成功绿色
    'success-green': [
      '#F6FFED',
      '#D9F7BE',
      '#B7EB8F',
      '#95DE64',
      '#73D13D',
      '#52C41A',
      '#389E0D',
      '#237804',
      '#135200',
      '#092B00',
    ],
    // 警告黄色
    'warning-yellow': [
      '#FFFBE6',
      '#FFF1B8',
      '#FFE58F',
      '#FFD666',
      '#FFC53D',
      '#FAAD14',
      '#D48806',
      '#AD6800',
      '#874D00',
      '#613400',
    ],
    // 错误红色
    'error-red': [
      '#FFF1F0',
      '#FFCCC7',
      '#FFA39E',
      '#FF7875',
      '#FF4D4F',
      '#F5222D',
      '#CF1322',
      '#A8071A',
      '#820014',
      '#5C0011',
    ],
  },
}); 