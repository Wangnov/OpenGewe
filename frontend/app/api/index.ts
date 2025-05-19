// 导出API客户端
export * from './client';

// 导出API服务
export * from './auth';
export * from './robots';
export * from './plugins';
export * from './system';

// 统一API命名空间
export const API = {
  Auth: require('./auth').AuthService,
  Robot: require('./robots').RobotService,
  Plugin: require('./plugins').PluginService,
  System: require('./system').SystemService,
}; 