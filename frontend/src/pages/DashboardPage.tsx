import { useEffect } from 'react';
import { 
  SimpleGrid, 
  Card, 
  Text, 
  Title, 
  Group, 
  RingProgress, 
  Badge, 
  LoadingOverlay, 
  Stack 
} from '@mantine/core';
import { useSystemStore } from '../stores/system';
import { useRobotStore } from '../stores/robots';
import { usePluginStore } from '../stores/plugins';
import { Icons } from '../utils/fa-icon-loader';

/**
 * 系统概览组件
 */
const SystemOverview = () => {
  const { status, isLoading } = useSystemStore();

  if (!status) {
    return <LoadingOverlay visible={isLoading} />;
  }

  return (
    <SimpleGrid cols={{ base: 1, sm: 2, md: 4 }}>
      <Card withBorder p="md">
        <Group justify="space-between">
          <div>
            <Text size="xs" c="dimmed">CPU使用率</Text>
            <Title order={3}>{status.cpu_usage}%</Title>
          </div>
          {Icons.icon("microchip", "solid", { size: 32, color: "blue" })}
        </Group>
        <RingProgress
          sections={[{ value: status.cpu_usage, color: 'blue' }]}
          size={80}
          thickness={8}
          mt="md"
        />
      </Card>

      <Card withBorder p="md">
        <Group justify="space-between">
          <div>
            <Text size="xs" c="dimmed">内存使用率</Text>
            <Title order={3}>{status.memory_usage}%</Title>
          </div>
          {Icons.icon("database", "solid", { size: 32, color: "green" })}
        </Group>
        <RingProgress
          sections={[{ value: status.memory_usage, color: 'green' }]}
          size={80}
          thickness={8}
          mt="md"
        />
      </Card>

      <Card withBorder p="md">
        <Group justify="space-between">
          <div>
            <Text size="xs" c="dimmed">机器人</Text>
            <Group gap={5}>
              <Title order={3}>{status.robots_count.online}</Title>
              <Text c="dimmed" size="sm">/ {status.robots_count.total}</Text>
            </Group>
          </div>
          {Icons.icon("robot", "solid", { size: 32, color: "violet" })}
        </Group>
        <Text size="xs" c="dimmed" mt="md">
          {status.robots_count.online} 个在线，{status.robots_count.total - status.robots_count.online} 个离线
        </Text>
      </Card>

      <Card withBorder p="md">
        <Group justify="space-between">
          <div>
            <Text size="xs" c="dimmed">插件</Text>
            <Group gap={5}>
              <Title order={3}>{status.plugins_count.enabled}</Title>
              <Text c="dimmed" size="sm">/ {status.plugins_count.total}</Text>
            </Group>
          </div>
          {Icons.icon("plug", "solid", { size: 32, color: "orange" })}
        </Group>
        <Text size="xs" c="dimmed" mt="md">
          {status.plugins_count.enabled} 个启用，{status.plugins_count.total - status.plugins_count.enabled} 个禁用
        </Text>
      </Card>
    </SimpleGrid>
  );
};

/**
 * 机器人状态组件
 */
const RobotStatus = () => {
  const { robots, isLoading } = useRobotStore();

  if (isLoading || robots.length === 0) {
    return <LoadingOverlay visible={isLoading} />;
  }

  return (
    <Card withBorder p="md">
      <Title order={5} mb="md">机器人状态</Title>
      <Stack gap="xs">
        {robots.slice(0, 5).map(robot => (
          <Group key={robot.id} justify="space-between">
            <Text size="sm">{robot.name}</Text>
            <Badge 
              color={robot.status === 'online' ? 'green' : robot.status === 'logging' ? 'blue' : 'red'}
            >
              {robot.status === 'online' ? '在线' : robot.status === 'logging' ? '登录中' : '离线'}
            </Badge>
          </Group>
        ))}
        {robots.length > 5 && (
          <Text size="xs" c="dimmed" ta="center">
            还有 {robots.length - 5} 个机器人未显示
          </Text>
        )}
      </Stack>
    </Card>
  );
};

/**
 * 插件状态组件
 */
const PluginStatus = () => {
  const { plugins, isLoading } = usePluginStore();

  if (isLoading || plugins.length === 0) {
    return <LoadingOverlay visible={isLoading} />;
  }

  return (
    <Card withBorder p="md">
      <Title order={5} mb="md">插件状态</Title>
      <Stack gap="xs">
        {plugins.slice(0, 5).map(plugin => (
          <Group key={plugin.id} justify="space-between">
            <Text size="sm">{plugin.name}</Text>
            <Badge color={plugin.is_enabled ? 'green' : 'gray'}>
              {plugin.is_enabled ? '已启用' : '已禁用'}
            </Badge>
          </Group>
        ))}
        {plugins.length > 5 && (
          <Text size="xs" c="dimmed" ta="center">
            还有 {plugins.length - 5} 个插件未显示
          </Text>
        )}
      </Stack>
    </Card>
  );
};

/**
 * 仪表盘页面组件
 */
export default function DashboardPage() {
  const { fetchStatus } = useSystemStore();
  const { fetchRobots } = useRobotStore();
  const { fetchPlugins } = usePluginStore();

  useEffect(() => {
    // 加载数据
    fetchStatus();
    fetchRobots();
    fetchPlugins();
  
    // 设置定时刷新
    const intervalId = setInterval(() => {
      fetchStatus();
    }, 30000); // 每30秒刷新一次系统状态
  
    return () => clearInterval(intervalId);
  }, [fetchStatus, fetchRobots, fetchPlugins]);

  return (
    <Stack gap="md">
      <Title order={2}>系统概览</Title>
      <SystemOverview />
      
      <SimpleGrid cols={{ base: 1, md: 2 }} mt="lg">
        <RobotStatus />
        <PluginStatus />
      </SimpleGrid>
    </Stack>
  );
} 