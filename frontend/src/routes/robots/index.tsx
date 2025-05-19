import { type MetaFunction } from "react-router";
import RobotListPage from "../../pages/robots/RobotListPage";

export const meta: MetaFunction = () => {
  return [
    { title: "机器人管理 - 微信机器人管理系统" },
    { name: "description", content: "微信机器人管理列表" },
  ];
};

export default function RobotListRoute() {
  return <RobotListPage />;
} 