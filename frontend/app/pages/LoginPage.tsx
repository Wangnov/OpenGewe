import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  TextInput, 
  PasswordInput, 
  Button, 
  Group, 
  Box, 
  Paper, 
  Title, 
  Text, 
  Container, 
  Center,
  Stack,
  Alert
} from '@mantine/core';
import { useForm, zodResolver } from '@mantine/form';
import { z } from 'zod';
import { useAuthStore } from '../stores/auth';
import { IconAlertCircle, IconLogin } from '@tabler/icons-react';

// 登录表单验证schema
const loginSchema = z.object({
  username: z.string().min(1, '用户名不能为空'),
  password: z.string().min(1, '密码不能为空'),
});

// 表单字段类型
type LoginFormValues = z.infer<typeof loginSchema>;

/**
 * 登录页组件
 */
export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  // 设置表单
  const form = useForm<LoginFormValues>({
    validate: zodResolver(loginSchema),
    initialValues: {
      username: '',
      password: '',
    },
  });

  // 登录处理函数
  const handleSubmit = async (values: LoginFormValues) => {
    try {
      setError(null);
      const success = await login(values);
      
      if (success) {
        // 登录成功，跳转到首页
        navigate('/');
      } else {
        // 登录失败，显示错误
        setError('登录失败，请检查用户名和密码');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '登录失败，请重试');
    }
  };

  return (
    <Container size="xs" py="xl">
      <Center style={{ minHeight: '80vh' }}>
        <Paper radius="md" p="xl" withBorder>
          <Title order={2} ta="center" mt="md" mb={50}>
            微信机器人管理系统
          </Title>

          <form onSubmit={form.onSubmit(handleSubmit)}>
            <Stack>
              {error && (
                <Alert icon={<IconAlertCircle size={16} />} color="red" title="错误">
                  {error}
                </Alert>
              )}

              <TextInput
                label="用户名"
                placeholder="请输入用户名"
                required
                {...form.getInputProps('username')}
              />

              <PasswordInput
                label="密码"
                placeholder="请输入密码"
                required
                {...form.getInputProps('password')}
              />
            </Stack>

            <Group justify="space-between" mt="xl">
              <Text size="sm" c="dimmed">
                首次使用请联系管理员获取账号
              </Text>
              <Button 
                type="submit" 
                loading={isLoading}
                leftSection={<IconLogin size={16} />}
              >
                登录
              </Button>
            </Group>
          </form>
        </Paper>
      </Center>
    </Container>
  );
} 