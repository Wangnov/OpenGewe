import React, { useState, useEffect, useCallback } from 'react';
import configService from '../services/configService';
import useApiLoading from '../hooks/useApiLoading';
import useNotification from '../hooks/useNotification';
import LoadingSpinner from '../components/common/LoadingSpinner';

/**
 * 系统设置页面
 * @returns {JSX.Element} 系统设置页面组件
 */
const Settings = () => {
    const [configs, setConfigs] = useState(null);
    const [loading, setLoading] = useState(true);
    const { executeWithLoading } = useApiLoading();
    const { success, error: notifyError, warning, removeNotification } = useNotification();

    const fetchConfigs = useCallback(async () => {
        try {
            setLoading(true);
            const response = await executeWithLoading(configService.getAllConfigs);
            const configData = response.data?.data || {};
            setConfigs(configData);
        } catch (error) {
            console.error('获取系统配置失败:', error);
            notifyError('获取失败', '获取系统配置失败，请稍后重试。');
        } finally {
            setLoading(false);
        }
    }, [executeWithLoading, notifyError]);

    useEffect(() => {
        fetchConfigs();
    }, [fetchConfigs]);

    const handleSave = async (sectionName, newConfig) => {
        try {
            await executeWithLoading(() => configService.updateConfigSection(sectionName, newConfig));
            success('保存成功', `配置项 "${sectionName}" 已成功更新。`);
            // Optionally, refetch configs to confirm update
            fetchConfigs();
        } catch (error) {
            console.error(`保存配置 ${sectionName} 失败:`, error);
            notifyError('保存失败', `配置项 "${sectionName}" 保存失败，请稍后重试。`);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <LoadingSpinner size="lg" text="加载系统配置中..." />
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {configs && <PluginSettings config={configs.plugins} onSave={(newConfig) => handleSave('plugins', newConfig)} />}
            {configs && <QueueSettings config={configs.queue} onSave={(newConfig) => handleSave('queue', newConfig)} />}
            {configs && <LoggingSettings config={configs.logging} onSave={(newConfig) => handleSave('logging', newConfig)} />}
            {configs && <WebPanelSettings
                config={configs.webpanel}
                onSave={(newConfig) => handleSave('webpanel', newConfig)}
                warning={warning}
                removeNotification={removeNotification}
            />}
        </div>
    );
};

// --- 子组件 ---

const ConfigCard = ({ title, description, icon, children }) => (
    <div className="bg-white rounded-lg shadow-md">
        <div className="p-6">
            <div className="flex items-start">
                <div className="flex-shrink-0 bg-purple-100 text-purple-600 rounded-lg w-12 h-12 flex items-center justify-center">
                    <i className={`fas ${icon} fa-lg`}></i>
                </div>
                <div className="ml-4">
                    <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
                    <p className="mt-1 text-sm text-gray-600">{description}</p>
                </div>
            </div>
            <div className="mt-6 border-t border-gray-200 pt-6 space-y-4">{children}</div>
            {children.find(child => child.type === SaveButton) ? null : <SaveButton />}
        </div>
    </div>
);

const FormField = ({ label, helpText, children }) => (
    <div>
        <label className="block text-sm font-medium text-gray-700">{label}</label>
        <div className="mt-1">{children}</div>
        {helpText && <p className="mt-2 text-xs text-gray-500">{helpText}</p>}
    </div>
);

const TextInput = (props) => (
    <input
        type="text"
        {...props}
        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
    />
);

const Select = ({ children, ...props }) => (
    <select
        {...props}
        className="block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
    >
        {children}
    </select>
);

const SaveButton = ({ onClick, isSaving }) => (
    <div className="pt-4 flex justify-end">
        <button
            type="button"
            onClick={onClick}
            disabled={isSaving}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
        >
            {isSaving ? '保存中...' : '保存更改'}
        </button>
    </div>
);


const PluginSettings = ({ config, onSave }) => {
    const [pluginsDir, setPluginsDir] = useState(config?.plugins_dir || '');
    const [isSaving, setIsSaving] = useState(false);

    const handleSave = async () => {
        setIsSaving(true);
        await onSave({ ...config, plugins_dir: pluginsDir });
        setIsSaving(false);
    };

    return (
        <ConfigCard title="插件管理" description="配置插件系统的基本参数。" icon="fa-puzzle-piece">
            <FormField label="插件目录" helpText="存放所有插件的根目录路径。">
                <TextInput value={pluginsDir} onChange={(e) => setPluginsDir(e.target.value)} placeholder="例如: plugins" />
            </FormField>
            <SaveButton onClick={handleSave} isSaving={isSaving} />
        </ConfigCard>
    );
};

const QueueSettings = ({ config, onSave }) => {
    const [formState, setFormState] = useState(config || {});
    const [isSaving, setIsSaving] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormState(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const handleSave = async () => {
        setIsSaving(true);
        await onSave(formState);
        setIsSaving(false);
    };

    return (
        <ConfigCard title="任务队列" description="配置消息处理的任务队列类型和参数。" icon="fa-cogs">
            <FormField label="队列类型" helpText="Simple为简单内存队列，Advanced为使用Celery的专业队列。">
                <Select name="queue_type" value={formState.queue_type || 'simple'} onChange={handleChange}>
                    <option value="simple">Simple</option>
                    <option value="advanced">Advanced</option>
                </Select>
            </FormField>
            {formState.queue_type === 'advanced' && (
                <>
                    <FormField label="Broker URL" helpText="消息中间件的连接地址，例如 Redis 或 RabbitMQ。">
                        <TextInput name="broker" value={formState.broker || ''} onChange={handleChange} placeholder="redis://localhost:6379/0" />
                    </FormField>
                    <FormField label="Backend URL" helpText="任务结果存储的连接地址。">
                        <TextInput name="backend" value={formState.backend || ''} onChange={handleChange} placeholder="redis://localhost:6379/0" />
                    </FormField>
                    <FormField label="并发数" helpText="Worker的并发数量。">
                        <TextInput type="number" name="concurrency" value={formState.concurrency || 4} onChange={handleChange} />
                    </FormField>
                </>
            )}
            <SaveButton onClick={handleSave} isSaving={isSaving} />
        </ConfigCard>
    );
};

const LoggingSettings = ({ config, onSave }) => {
    const [formState, setFormState] = useState(config || {});
    const [isSaving, setIsSaving] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormState(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
    };

    const handleSave = async () => {
        setIsSaving(true);
        await onSave(formState);
        setIsSaving(false);
    };

    return (
        <ConfigCard title="日志配置" description="管理系统的日志记录级别、格式和存储方式。" icon="fa-file-alt">
            <FormField label="日志级别">
                <Select name="level" value={formState.level || 'INFO'} onChange={handleChange}>
                    <option value="TRACE">TRACE</option>
                    <option value="DEBUG">DEBUG</option>
                    <option value="INFO">INFO</option>
                    <option value="SUCCESS">SUCCESS</option>
                    <option value="WARNING">WARNING</option>
                    <option value="ERROR">ERROR</option>
                    <option value="CRITICAL">CRITICAL</option>
                </Select>
            </FormField>
            <FormField label="日志格式">
                <Select name="format" value={formState.format || 'color'} onChange={handleChange}>
                    <option value="color">Color</option>
                    <option value="json">JSON</option>
                    <option value="simple">Simple</option>
                </Select>
            </FormField>
            <FormField label="日志路径">
                <TextInput name="path" value={formState.path || './logs'} onChange={handleChange} />
            </FormField>
            <FormField label="日志轮换大小">
                <TextInput name="rotation" value={formState.rotation || '500 MB'} onChange={handleChange} />
            </FormField>
            <FormField label="日志保留时间">
                <TextInput name="retention" value={formState.retention || '10 days'} onChange={handleChange} />
            </FormField>
            <SaveButton onClick={handleSave} isSaving={isSaving} />
        </ConfigCard>
    );
};

const WebPanelSettings = ({ config, onSave, warning, removeNotification }) => {
    const [formState, setFormState] = useState(config || { database: {}, redis: {} });
    const [isSaving, setIsSaving] = useState(false);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        const [section, field] = name.split('.');

        if (field) {
            setFormState(prev => ({
                ...prev,
                [section]: {
                    ...prev[section],
                    [field]: type === 'checkbox' ? checked : value,
                }
            }));
        } else {
            setFormState(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
        }
    };

    const handleSave = async () => {
        const notificationId = warning(
            '确认修改?',
            '修改数据库或Redis配置是高危操作，可能导致应用无法启动或数据丢失。确定要继续吗？',
            {
                duration: 0, // 永不自动关闭
                actions: [
                    {
                        label: '确认保存',
                        onClick: async () => {
                            removeNotification(notificationId);
                            setIsSaving(true);
                            await onSave(formState);
                            setIsSaving(false);
                        },
                        variant: 'primary'
                    },
                    {
                        label: '取消',
                        onClick: () => removeNotification(notificationId),
                        variant: 'secondary'
                    }
                ]
            }
        );
    };

    return (
        <ConfigCard title="Web面板" description="管理Web后台的核心参数、数据库和Redis连接。" icon="fa-server">
            <h3 className="text-md font-semibold text-gray-800 -mt-2 mb-3">基础配置</h3>
            <FormField label="Host">
                <TextInput name="host" value={formState.host || '0.0.0.0'} onChange={handleChange} />
            </FormField>
            <FormField label="Port">
                <TextInput type="number" name="port" value={formState.port || 5432} onChange={handleChange} />
            </FormField>
            <FormField label="Admin Username">
                <TextInput name="admin_username" value={formState.admin_username || 'admin'} onChange={handleChange} />
            </FormField>
            <FormField label="Admin Password">
                <TextInput type="password" name="admin_password" value={formState.admin_password || ''} onChange={handleChange} placeholder="留空表示不修改" />
            </FormField>
            <FormField label="Secret Key">
                <TextInput type="password" name="secret_key" value={formState.secret_key || ''} onChange={handleChange} placeholder="留空表示不修改" />
            </FormField>

            <h3 className="text-md font-semibold text-gray-800 mt-6 pt-4 border-t border-gray-200">数据库配置 (MySQL)</h3>
            <FormField label="DB Host">
                <TextInput name="database.host" value={formState.database?.host || ''} onChange={handleChange} />
            </FormField>
            <FormField label="DB Port">
                <TextInput type="number" name="database.port" value={formState.database?.port || 3306} onChange={handleChange} />
            </FormField>
            <FormField label="DB Username">
                <TextInput name="database.username" value={formState.database?.username || ''} onChange={handleChange} />
            </FormField>
            <FormField label="DB Password">
                <TextInput type="password" name="database.password" value={formState.database?.password || ''} onChange={handleChange} placeholder="留空表示不修改" />
            </FormField>
            <FormField label="DB Name">
                <TextInput name="database.database" value={formState.database?.database || ''} onChange={handleChange} />
            </FormField>

            <h3 className="text-md font-semibold text-gray-800 mt-6 pt-4 border-t border-gray-200">Redis 配置</h3>
            <FormField label="Redis Host">
                <TextInput name="redis.host" value={formState.redis?.host || ''} onChange={handleChange} />
            </FormField>
            <FormField label="Redis Port">
                <TextInput type="number" name="redis.port" value={formState.redis?.port || 6379} onChange={handleChange} />
            </FormField>
            <FormField label="Redis DB">
                <TextInput type="number" name="redis.db" value={formState.redis?.db || 0} onChange={handleChange} />
            </FormField>
            <FormField label="Redis Password">
                <TextInput type="password" name="redis.password" value={formState.redis?.password || ''} onChange={handleChange} placeholder="留空表示无密码" />
            </FormField>

            <SaveButton onClick={handleSave} isSaving={isSaving} />
        </ConfigCard>
    );
};

export default Settings;