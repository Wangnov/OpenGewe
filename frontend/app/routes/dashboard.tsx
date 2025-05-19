import { type MetaFunction } from "react-router";
import DashboardPage from "../pages/DashboardPage";

export const meta: MetaFunction = () => {
  return [
    { title: "仪表盘 - 微信机器人管理系统" },
    { name: "description", content: "微信机器人管理系统仪表盘" },
  ];
};

export default function DashboardRoute() {
  return <DashboardPage />;
} 