"""
配置文件模板 - GitHub Trending 邮件推送
请复制此文件为 config.py 并填写你的邮箱配置信息
"""

# ==================== 邮箱配置 ====================
# QQ邮箱配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465  # QQ邮箱使用SSL端口

# 发件人邮箱（你的QQ邮箱）
SENDER_EMAIL = "your_qq@qq.com"

# 邮箱授权码（不是登录密码！需要在QQ邮箱设置中开启SMTP并获取授权码）
# 获取方式：QQ邮箱 -> 设置 -> 账户 -> 开启SMTP服务 -> 获取授权码
SENDER_PASSWORD = "your_authorization_code"

# 收件人邮箱（可以是同一个邮箱）
RECEIVER_EMAIL = "your_qq@qq.com"

# ==================== 定时配置 ====================
# 每天推送时间（24小时制）
PUSH_HOUR = 9
PUSH_MINUTE = 0

# ==================== 爬虫配置 ====================
# GitHub Trending URL
TRENDING_URL = "https://github.com/trending"

# 请求头（模拟浏览器访问）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 获取项目数量
TOP_N = 10
