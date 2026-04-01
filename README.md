# GitHub Trending Daily Push

每天早上自动获取 GitHub Trending 热门项目，并通过邮件推送到你的邮箱。

## 项目简介

GitHub Trending Daily Push 是一个自动化工具，能够每天定时抓取 GitHub 热门项目，并以美观的 HTML 邮件格式推送给用户。通过本项目，你可以每天第一时间了解到 GitHub 上最受欢迎的热门项目，无需手动查看。

## 主要功能

- **自动抓取**：每天自动获取 GitHub Trending 今日热门项目
- **邮件推送**：通过 QQ 邮箱发送精美的 HTML 格式邮件
- **定时任务**：支持 Windows 任务计划程序，实现每天自动执行
- **无需值守**：配置完成后完全自动化运行
- **配置灵活**：支持自定义推送时间、项目数量等参数

## 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.8+ | 编程语言 |
| requests | HTTP 请求库，用于抓取网页 |
| BeautifulSoup | HTML 解析库，用于提取项目信息 |
| schedule | 定时任务调度库 |
| smtplib | Python 内置邮件发送库 |

## 项目结构

```
github-trending/
├── config.py                 # 配置文件（邮箱、定时等）
├── crawler.py                # GitHub Trending 爬虫模块
├── email_sender.py           # 邮件发送模块
├── main.py                   # 主程序入口
├── requirements.txt           # Python 依赖包
├── run_trending.bat          # Windows 任务计划调用脚本
├── setup_task.ps1            # 任务计划创建脚本
├── setup_task_with_wake.ps1  # 唤醒型任务计划脚本
├── setup_system_task.ps1     # 系统级任务计划脚本
├── 手动运行.bat              # 手动触发推送的快捷脚本
└── github_trending.log       # 运行日志文件
```

## 安装与配置

### 环境要求

- Windows 7/10/11 或 Windows Server
- Python 3.8 或更高版本
- QQ 邮箱账号（需开启 SMTP 服务）

### 安装步骤

#### 1. 安装 Python

如果尚未安装 Python，请从 [Python 官网](https://www.python.org/downloads/) 下载并安装。安装时请勾选 "Add Python to PATH" 选项。

#### 2. 克隆或下载项目

```bash
git clone https://github.com/Liu-Qing-song/Github-daily-trending.git
cd Github-daily-trending
```

或直接将项目文件夹下载到本地。

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置邮箱

打开 `config.py` 文件，修改以下配置：

```python
# 邮箱配置
SMTP_SERVER = "smtp.qq.com"        # SMTP 服务器
SMTP_PORT = 465                     # SMTP 端口（QQ邮箱使用 SSL）

SENDER_EMAIL = "your_qq@qq.com"     # 你的 QQ 邮箱
SENDER_PASSWORD = "your_auth_code"  # 邮箱授权码（非登录密码！）
RECEIVER_EMAIL = "your_qq@qq.com"  # 收件人邮箱

# 定时配置
PUSH_HOUR = 9                       # 推送小时（24小时制）
PUSH_MINUTE = 0                     # 推送分钟

# 爬虫配置
TOP_N = 10                          # 获取项目数量
```

**如何获取 QQ 邮箱授权码：**

1. 登录 [QQ 邮箱网页版](https://mail.qq.com/)
2. 点击「设置」→「账户」
3. 找到「POP3/SMTP 服务」，点击「开启」
4. 按照提示发送短信验证
5. 获取授权码并填写到配置文件中

## 使用方法

### 方式一：手动运行

```bash
python main.py --once
```

这将立即执行一次推送任务，发送邮件到配置的收件人邮箱。

### 方式二：启动定时服务

```bash
python main.py
```

程序将保持运行，每天早上 9:00 自动执行推送任务。

### 方式三：Windows 任务计划（推荐）

#### 方法 A：手动创建任务计划

1. 按 `Win + R`，输入 `taskschd.msc`，打开任务计划程序
2. 点击「创建基本任务」
3. 设置任务名称：`GitHub Trending Daily Push`
4. 触发器：每天 → 早上 9:00
5. 操作：启动程序 → 选择 `run_trending.bat`
6. 完成创建

#### 方法 B：使用脚本创建

以管理员身份打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy Bypass -File setup_task.ps1
```

#### 方法 C：手动触发测试

双击 `手动运行.bat` 即可立即测试发送邮件。

### 命令说明

| 命令 | 说明 |
|------|------|
| `python main.py` | 启动定时服务 |
| `python main.py --once` | 执行一次推送 |
| `python main.py --help` | 查看帮助信息 |

## 常见问题

### Q1: 邮件发送失败，提示 "SMTPAuthenticationError"

**原因**：邮箱授权码不正确或已过期。

**解决方法**：
1. 登录 QQ邮箱 → 设置 → 账户
2. 检查 POP3/SMTP 服务是否开启
3. 重新获取授权码并更新 `config.py`

### Q2: 任务计划没有执行

**可能原因**：
1. 任务计划被删除
2. 电脑在推送时间处于关机状态
3. 任务计划设置为了"仅在用户登录时运行"

**解决方法**：
1. 重新创建任务计划
2. 确保电脑在 9:00 处于开机状态
3. 修改任务计划属性，设置为"不管是否登录都要运行"

### Q3: 收到邮件但内容为空或显示异常

**可能原因**：GitHub 页面结构发生变化。

**解决方法**：
1. 手动运行 `python crawler.py` 查看抓取结果
2. 如有问题，可能是 GitHub 页面改版，需要更新爬虫代码

### Q4: 切换 Windows 用户后任务不执行

**原因**：当前任务是以当前用户身份运行的。

**解决方法**：
1. 使用管理员权限重新创建系统级任务
2. 或保持当前用户登录状态，不要切换用户

### Q5: 电脑休眠/睡眠时任务不执行

**原因**：休眠状态下任务无法执行。

**解决方法**：
1. 使用 `setup_task_with_wake.ps1` 重新创建任务（支持唤醒电脑）
2. 确保电脑连接电源，且电源设置中允许唤醒定时器
3. 或调整电脑使用习惯，避免在推送时间休眠

### Q6: 如何修改推送时间

修改 `config.py` 中的时间配置：

```python
PUSH_HOUR = 10    # 改为上午 10 点
PUSH_MINUTE = 30 # 30 分
```

修改后需要重新创建任务计划。

### Q7: 如何修改推送数量

修改 `config.py`：

```python
TOP_N = 20  # 获取前 20 个项目
```

## 进阶配置

### 修改 GitHub Trending 筛选条件

目前默认获取所有语言的 Trending 页面。如需修改（例如只获取 Python 项目），需要修改 `crawler.py` 中的 `TRENDING_URL`：

```python
# Python 项目的 Trending 页面
TRENDING_URL = "https://github.com/trending?since=weekly&spoken_language_code="
```

### 添加多个收件人

修改 `email_sender.py` 中的发送逻辑：

```python
# 添加多个收件人
receiver_list = ["user1@qq.com", "user2@qq.com"]
for receiver in receiver_list:
    # 发送邮件逻辑
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交问题

如果发现 bug 或有新功能建议，请提交 Issue。描述请包含：
- 详细的问题描述
- 复现步骤（如适用）
- 预期行为和实际行为
- 环境信息（操作系统、Python 版本等）

### 提交代码

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 许可证

本项目仅供个人学习交流使用，请勿用于商业用途。

## 联系方式

如有问题，请在 GitHub 仓库中提交 Issue。

---

祝使用愉快！每天早上9点准时查收 GitHub 热门项目推送！ 🚀
