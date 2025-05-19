import { Routes, Route } from 'react-router-dom';
import { AppLayout } from './layouts/AppLayout';
import { AuthGuard } from './components/AuthGuard';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RobotListPage from './pages/robots/RobotListPage';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <AuthGuard>
            <AppLayout />
          </AuthGuard>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="robots" element={<RobotListPage />} />
        {/* 其他路由将在后续添加 */}
      </Route>
    </Routes>
  );
} 