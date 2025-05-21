import { useState, useEffect } from 'react';
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
  Alert,
  Loader
} from '@mantine/core';
import { useForm, zodResolver } from '@mantine/form';
import { z } from 'zod';
import { useAuthStore } from '../stores/auth';
import { Icons } from '../utils/fa-icon-loader';
import { AuthService } from '../api/auth';

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
  const [isInitializing, setIsInitializing] = useState<boolean>(true);
  const [initMessage, setInitMessage] = useState<string | null>(null);
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

  // 在组件加载时检查管理员账户状态
  useEffect(() => {
    const checkAdmin = async () => {
      try {
        setIsInitializing(true);
        const response = await AuthService.checkAdminInit();
        
        if (response.success && response.data) {
          if (response.data.detail) {
            setInitMessage(response.data.detail);
            // 设置默认登录凭证
            form.setValues({
              username: 'admin',
              password: 'admin123'
            });
          }
        } else if (response.error) {
          setError(`初始化检查失败: ${response.message || response.error}`);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : '无法连接到服务器，请检查网络连接');
      } finally {
        setIsInitializing(false);
      }
    };
    
    checkAdmin();
  }, []); // 空依赖数组，确保仅执行一次

  // 登录处理函数
  const handleSubmit = async (values: LoginFormValues) => {
    try {
      setError(null);
      console.log('[LoginPage] 提交登录表单:', values);
      
      const success = await login(values);
      console.log('[LoginPage] 登录结果:', success);
      
      if (success) {
        console.log('[LoginPage] 登录成功，准备跳转到首页');
        // 登录成功，跳转到首页
        navigate('/');
      } else {
        // 登录失败，显示错误
        console.error('[LoginPage] 登录失败');
        setError('登录失败，请检查用户名和密码');
      }
    } catch (err) {
      console.error('[LoginPage] 登录异常:', err);
      setError(err instanceof Error ? err.message : '登录失败，请重试');
    }
  };

  // 加载中状态显示
  if (isInitializing) {
    return (
      <Container size="xs" py="xl">
        <Center style={{ minHeight: '80vh' }}>
          <Stack align="center" gap="md">
            <Loader size="lg" />
            <Text>正在检查系统状态，请稍候...</Text>
          </Stack>
        </Center>
      </Container>
    );
  }

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
                <Alert icon={Icons.icon("exclamation-circle", "solid", { size: 16 })} color="red" title="错误">
                  {error}
                </Alert>
              )}
              
              {initMessage && (
                <Alert icon={Icons.icon("info-circle", "solid", { size: 16 })} color="blue" title="提示">
                  {initMessage}
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
                leftSection={Icons.icon("sign-in-alt", "solid", { size: 16 })}
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