import { type MetaFunction } from "react-router";
import LoginPage from "../pages/LoginPage";

export const meta: MetaFunction = () => {
  return [
    { title: "登录 - 微信机器人管理系统" },
    { name: "description", content: "微信机器人管理系统登录页面" },
  ];
};

export default function LoginRoute() {
  return <LoginPage />;
} 