import { useState } from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { 
  AppShell,
  Burger,
  Group,
  NavLink,
  Text,
  UnstyledButton,
  Avatar,
  Menu,
  Divider,
  useMantineColorScheme,
  ActionIcon,
  Stack,
  Box,
  Title
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { 
  IconGauge, 
  IconUsers, 
  IconRobot, 
  IconPlugConnected,
  IconSettings,
  IconLogout,
  IconUser,
  IconMoonStars,
  IconSun
} from '@tabler/icons-react';
import { useAuthStore } from '../stores/auth';

/**
 * 应用主布局组件
 */
export function AppLayout() {
  const [opened, { toggle }] = useDisclosure();
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { colorScheme, setColorScheme } = useMantineColorScheme();

  // 导航项配置
  const navItems = [
    { label: '仪表盘', icon: <IconGauge size={20} />, path: '/' },
    { label: '机器人管理', icon: <IconRobot size={20} />, path: '/robots' },
    { label: '插件管理', icon: <IconPlugConnected size={20} />, path: '/plugins' },
    { label: '用户管理', icon: <IconUsers size={20} />, path: '/users' },
    { label: '系统设置', icon: <IconSettings size={20} />, path: '/settings' },
  ];

  // 处理登出
  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  // 切换主题
  const toggleColorScheme = () => {
    setColorScheme(colorScheme === 'dark' ? 'light' : 'dark');
  };

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 280,
        breakpoint: 'sm',
        collapsed: { mobile: !opened },
      }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Group>
            <Burger
              opened={opened}
              onClick={toggle}
              hiddenFrom="sm"
              size="sm"
            />
            <Title order={3}>OpenGewe</Title>
          </Group>

          <Group>
            <ActionIcon 
              variant="default" 
              onClick={toggleColorScheme} 
              size="lg"
            >
              {colorScheme === 'dark' ? (
                <IconSun size={20} />
              ) : (
                <IconMoonStars size={20} />
              )}
            </ActionIcon>

            <Menu position="bottom-end" shadow="md">
              <Menu.Target>
                <UnstyledButton>
                  <Group>
                    <Avatar color="blue" radius="xl">{user?.username?.charAt(0) || '?'}</Avatar>
                    <div>
                      <Text size="sm" fw={500}>
                        {user?.username || 'User'}
                      </Text>
                      <Text size="xs" c="dimmed">
                        {user?.is_superuser ? '管理员' : '普通用户'}
                      </Text>
                    </div>
                  </Group>
                </UnstyledButton>
              </Menu.Target>

              <Menu.Dropdown>
                <Menu.Item leftSection={<IconUser size={14} />}>
                  个人资料
                </Menu.Item>
                <Menu.Divider />
                <Menu.Item 
                  leftSection={<IconLogout size={14} />}
                  onClick={handleLogout}
                  color="red"
                >
                  退出登录
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Stack justify="space-between" gap={0} h="100%">
          <div>
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                label={item.label}
                leftSection={item.icon}
                active={location.pathname === item.path}
                onClick={() => navigate(item.path)}
                mb={8}
              />
            ))}
          </div>

          <Box>
            <Divider my="sm" />
            <Text size="xs" c="dimmed" ta="center" mt="md">
              版本 v1.0.0
            </Text>
          </Box>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
} 