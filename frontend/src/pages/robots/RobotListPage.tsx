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
import { Icons } from '../../utils/fa-icon-loader';
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
        <Button leftSection={Icons.Plus({ size: 16 })} onClick={open}>
          添加机器人
        </Button>
      </Group>

      <Group mb="md">
        <TextInput
          placeholder="搜索机器人"
          leftSection={Icons.Search({ size: 16 })}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flexGrow: 1 }}
        />
        <Button 
          variant="outline" 
          leftSection={Icons.icon("sync", "solid", { size: 16 })}
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
                          <ActionIcon variant="subtle" size="sm">
                            {Icons.icon("ellipsis-v", "solid", { size: 16 })}
                          </ActionIcon>
                        </Menu.Target>
                        <Menu.Dropdown>
                          <Menu.Item 
                            leftSection={Icons.icon("eye", "solid", { size: 14 })}
                            onClick={() => navigate(`/robots/${robot.id}`)}
                          >
                            查看详情
                          </Menu.Item>
                          {robot.status === 'offline' && (
                            <Menu.Item 
                              leftSection={Icons.icon("sign-in-alt", "solid", { size: 14 })}
                              onClick={() => handleLoginRobot(robot.id, robot.name)}
                            >
                              登录
                            </Menu.Item>
                          )}
                          {robot.status === 'online' && (
                            <Menu.Item 
                              leftSection={Icons.icon("sign-out-alt", "solid", { size: 14 })}
                              onClick={() => handleLogoutRobot(robot.id, robot.name)}
                            >
                              登出
                            </Menu.Item>
                          )}
                          <Menu.Item 
                            leftSection={Icons.icon("trash", "solid", { size: 14, color: "red" })}
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
                <Group mt="md" gap="xs" align="flex-start">
                  <Text size="sm" fw={500} w={60}>
                    ID:
                  </Text>
                  <Text size="sm" style={{ flex: 1, wordBreak: 'break-all' }}>
                    {robot.id}
                  </Text>
                </Group>
                <Group mt="xs" gap="xs" align="flex-start">
                  <Text size="sm" fw={500} w={60}>
                    App ID:
                  </Text>
                  <Text size="sm" style={{ flex: 1, wordBreak: 'break-all' }}>
                    {robot.app_id || '-'}
                  </Text>
                </Group>
                <Group mt="xs" gap="xs" align="flex-start">
                  <Text size="sm" fw={500} w={60}>
                    创建:
                  </Text>
                  <Text size="sm" c="dimmed">
                    {new Date(robot.created_at).toLocaleString()}
                  </Text>
                </Group>
              </Card>
            ))}
          </SimpleGrid>
        )}
      </Box>

      <Modal opened={opened} onClose={close} title="添加机器人" centered>
        <form onSubmit={form.onSubmit(handleCreateRobot)}>
          <TextInput
            label="名称"
            placeholder="请输入机器人名称"
            withAsterisk
            mb="md"
            {...form.getInputProps('name')}
          />
          <TextInput
            label="App ID"
            placeholder="可选，自动生成"
            mb="md"
            {...form.getInputProps('app_id')}
          />
          <Group justify="flex-end" mt="xl">
            <Button variant="outline" onClick={close}>取消</Button>
            <Button type="submit">添加</Button>
          </Group>
        </form>
      </Modal>
    </Stack>
  );
} 