import { type RouteConfig, route } from "@react-router/dev/routes";
import { authGuard } from "./components/AuthGuard";

export default [
  // 登录页面 - 无需验证
  route("/login", "routes/login.tsx"),
  
  // 应用主布局 - 需要验证
  route("/", {
    loader: authGuard,
    Component: async () => {
      const { AppLayout } = await import("./layouts/AppLayout");
      return { Component: AppLayout };
    },
    children: [
      // 仪表盘 - 首页
      route("", "routes/dashboard.tsx"),
      
      // 机器人管理相关路由
      route("robots", "routes/robots/index.tsx"),
      route("robots/:id", "routes/robots/detail.tsx"),
      
      // 插件管理相关路由
      route("plugins", "routes/plugins/index.tsx"),
      route("plugins/:id", "routes/plugins/detail.tsx"),
      
      // 用户管理路由
      route("users", "routes/users/index.tsx"),
      
      // 系统设置路由
      route("settings", "routes/settings/index.tsx"),
    ],
  }),
] satisfies RouteConfig;
