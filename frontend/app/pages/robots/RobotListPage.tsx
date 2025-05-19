import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Title, 
  Button, 
  Card, 
  SimpleGrid, 
  Text, 
  Badge, 
  Group,
  Stack,
  Menu,
  LoadingOverlay,
  TextInput,
  Modal,
  ActionIcon,
  Box,
} from '@mantine/core';
import { useForm, zodResolver } from '@mantine/form';
import { useDisclosure } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import { 
  IconPlus, 
  IconSearch, 
  IconDotsVertical, 
  IconRefresh, 
  IconLogin, 
  IconLogout, 
  IconTrash, 
  IconEye 
} from '@tabler/icons-react';
import { z } from 'zod';
import { useRobotStore } from '../../stores/robots';

// 创建机器人表单验证schema
const createRobotSchema = z.object({
  name: z.string().min(1, '名称不能为空'),
  app_id: z.string().optional(),
});

// 表单字段类型
type CreateRobotFormValues = z.infer<typeof createRobotSchema>;

/**
 * 机器人列表页面组件
 */
export default function RobotListPage() {
  const navigate = useNavigate();
  const { robots, isLoading, error, fetchRobots, createRobot, deleteRobot, loginRobot, logoutRobot } = useRobotStore();
  const [search, setSearch] = useState('');
  const [opened, { open, close }] = useDisclosure(false);

  // 创建机器人表单
  const form = useForm<CreateRobotFormValues>({
    validate: zodResolver(createRobotSchema),
    initialValues: {
      name: '',
      app_id: '',
    },
  });

  // 获取机器人列表
  useEffect(() => {
    fetchRobots();
  }, [fetchRobots]);

  // 处理创建机器人
  const handleCreateRobot = async (values: CreateRobotFormValues) => {
    const robot = await createRobot(values);
    if (robot) {
      form.reset();
      close();
      notifications.show({
        title: '成功',
        message: `机器人 ${robot.name} 已创建`,
        color: 'green',
      });
    }
  };

  // 处理删除机器人
  const handleDeleteRobot = async (id: number, name: string) => {
    if (window.confirm(`确定要删除机器人 ${name} 吗？`)) {
      const success = await deleteRobot(id);
      if (success) {
        notifications.show({
          title: '成功',
          message: `机器人 ${name} 已删除`,
          color: 'green',
        });
      }
    }
  };

  // 处理登录机器人
  const handleLoginRobot = async (id: number, name: string) => {
    notifications.show({
      id: `login-${id}`,
      title: '登录中',
      message: `正在登录机器人 ${name}`,
      loading: true,
      autoClose: false,
    });

    const success = await loginRobot(id);
    
    notifications.update({
      id: `login-${id}`,
      title: success ? '成功' : '失败',
      message: success ? `机器人 ${name} 登录成功` : `机器人 ${name} 登录失败`,
      color: success ? 'green' : 'red',
      loading: false,
      autoClose: 3000,
    });
  };

  // 处理登出机器人
  const handleLogoutRobot = async (id: number, name: string) => {
    if (window.confirm(`确定要登出机器人 ${name} 吗？`)) {
      const success = await logoutRobot(id);
      if (success) {
        notifications.show({
          title: '成功',
          message: `机器人 ${name} 已登出`,
          color: 'green',
        });
      }
    }
  };

  // 过滤机器人列表
  const filteredRobots = robots.filter(robot => 
    robot.name.toLowerCase().includes(search.toLowerCase()) ||
    robot.app_id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Stack gap="md">
      <Group justify="space-between">
        <Title order={2}>机器人管理</Title>
        <Button leftSection={<IconPlus size={16} />} onClick={open}>
          添加机器人
        </Button>
      </Group>

      <Group mb="md">
        <TextInput
          placeholder="搜索机器人"
          leftSection={<IconSearch size={16} />}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flexGrow: 1 }}
        />
        <Button 
          variant="outline" 
          leftSection={<IconRefresh size={16} />}
          onClick={() => fetchRobots()}
        >
          刷新
        </Button>
      </Group>

      <Box pos="relative">
        <LoadingOverlay visible={isLoading} />
        {error && (
          <Text c="red" mb="md">
            {error}
          </Text>
        )}

        {filteredRobots.length === 0 ? (
          <Card withBorder p="xl" ta="center">
            <Text size="lg" fw={500} mb="md">
              没有找到机器人
            </Text>
            <Text c="dimmed" mb="xl">
              {search ? '尝试使用不同的搜索条件' : '点击上方的"添加机器人"按钮创建一个新机器人'}
            </Text>
            {search && (
              <Button variant="outline" onClick={() => setSearch('')}>
                清除搜索
              </Button>
            )}
          </Card>
        ) : (
          <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="lg">
            {filteredRobots.map((robot) => (
              <Card key={robot.id} withBorder shadow="sm" radius="md" padding="lg">
                <Card.Section withBorder inheritPadding py="xs">
                  <Group justify="space-between">
                    <Text fw={500} truncate>
                      {robot.name}
                    </Text>
                    <Group gap={8}>
                      <Badge 
                        color={robot.status === 'online' ? 'green' : robot.status === 'logging' ? 'blue' : 'red'}
                      >
                        {robot.status === 'online' ? '在线' : robot.status === 'logging' ? '登录中' : '离线'}
                      </Badge>
                      <Menu position="bottom-end" shadow="md">
                        <Menu.Target>
                          <ActionIcon size="sm" variant="subtle">
                            <IconDotsVertical size={14} />
                          </ActionIcon>
                        </Menu.Target>
                        <Menu.Dropdown>
                          <Menu.Item 
                            leftSection={<IconEye size={14} />}
                            onClick={() => navigate(`/robots/${robot.id}`)}
                          >
                            详情
                          </Menu.Item>
                          {robot.status !== 'online' && (
                            <Menu.Item 
                              leftSection={<IconLogin size={14} />}
                              onClick={() => handleLoginRobot(robot.id, robot.name)}
                            >
                              登录
                            </Menu.Item>
                          )}
                          {robot.status === 'online' && (
                            <Menu.Item 
                              leftSection={<IconLogout size={14} />}
                              onClick={() => handleLogoutRobot(robot.id, robot.name)}
                              color="orange"
                            >
                              登出
                            </Menu.Item>
                          )}
                          <Menu.Divider />
                          <Menu.Item 
                            leftSection={<IconTrash size={14} />}
                            onClick={() => handleDeleteRobot(robot.id, robot.name)}
                            color="red"
                          >
                            删除
                          </Menu.Item>
                        </Menu.Dropdown>
                      </Menu>
                    </Group>
                  </Group>
                </Card.Section>

                <Stack gap="xs" mt="md">
                  <Group gap="xs">
                    <Text fw={500} size="sm">
                      ID:
                    </Text>
                    <Text size="sm" c="dimmed">
                      {robot.id}
                    </Text>
                  </Group>
                  <Group gap="xs">
                    <Text fw={500} size="sm">
                      App ID:
                    </Text>
                    <Text size="sm" c="dimmed" truncate>
                      {robot.app_id || '未设置'}
                    </Text>
                  </Group>
                  {robot.wxid && (
                    <Group gap="xs">
                      <Text fw={500} size="sm">
                        微信ID:
                      </Text>
                      <Text size="sm" c="dimmed" truncate>
                        {robot.wxid}
                      </Text>
                    </Group>
                  )}
                  {robot.last_login_time && (
                    <Group gap="xs">
                      <Text fw={500} size="sm">
                        最后登录:
                      </Text>
                      <Text size="sm" c="dimmed">
                        {new Date(robot.last_login_time).toLocaleString()}
                      </Text>
                    </Group>
                  )}
                </Stack>

                <Group mt="lg" justify="flex-end">
                  <Button 
                    variant="light" 
                    size="xs"
                    onClick={() => navigate(`/robots/${robot.id}`)}
                  >
                    查看详情
                  </Button>
                  {robot.status !== 'online' && (
                    <Button 
                      variant="filled" 
                      size="xs"
                      onClick={() => handleLoginRobot(robot.id, robot.name)}
                    >
                      登录
                    </Button>
                  )}
                  {robot.status === 'online' && (
                    <Button 
                      variant="outline" 
                      color="red" 
                      size="xs"
                      onClick={() => handleLogoutRobot(robot.id, robot.name)}
                    >
                      登出
                    </Button>
                  )}
                </Group>
              </Card>
            ))}
          </SimpleGrid>
        )}
      </Box>

      {/* 创建机器人模态框 */}
      <Modal 
        opened={opened} 
        onClose={() => {
          close();
          form.reset();
        }}
        title="添加机器人"
      >
        <form onSubmit={form.onSubmit(handleCreateRobot)}>
          <Stack>
            <TextInput
              label="机器人名称"
              placeholder="输入机器人名称"
              required
              {...form.getInputProps('name')}
            />
            <TextInput
              label="App ID (可选)"
              description="如果有已存在的设备ID，可以在此输入"
              placeholder="输入App ID"
              {...form.getInputProps('app_id')}
            />

            <Group justify="flex-end" mt="md">
              <Button variant="outline" onClick={() => {
                close();
                form.reset();
              }}>
                取消
              </Button>
              <Button type="submit" loading={isLoading}>
                创建
              </Button>
            </Group>
          </Stack>
        </form>
      </Modal>
    </Stack>
  );
} 