"""
邮件发送模块
用于发送GitHub Trending项目的邮件推送
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List, Dict
import logging
from datetime import datetime

from config import (
    SMTP_SERVER, 
    SMTP_PORT, 
    SENDER_EMAIL, 
    SENDER_PASSWORD, 
    RECEIVER_EMAIL
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailSender:
    """邮件发送类"""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.receiver_email = RECEIVER_EMAIL
    
    def _create_html_content(self, repositories: List[Dict]) -> str:
        """
        创建邮件HTML内容
        
        Args:
            repositories: 仓库信息列表
            
        Returns:
            HTML格式的邮件内容
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    color: #24292e;
                    background-color: #f6f8fa;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                    font-size: 16px;
                }}
                .content {{
                    padding: 30px;
                }}
                .repo-item {{
                    border-bottom: 1px solid #e1e4e8;
                    padding: 20px 0;
                    display: flex;
                    align-items: flex-start;
                }}
                .repo-item:last-child {{
                    border-bottom: none;
                }}
                .rank {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #0366d6;
                    min-width: 50px;
                    text-align: center;
                    margin-right: 20px;
                    line-height: 1;
                }}
                .repo-info {{
                    flex: 1;
                }}
                .repo-name {{
                    font-size: 20px;
                    font-weight: 600;
                    margin: 0 0 8px 0;
                }}
                .repo-name a {{
                    color: #0366d6;
                    text-decoration: none;
                }}
                .repo-name a:hover {{
                    text-decoration: underline;
                }}
                .repo-desc {{
                    color: #586069;
                    font-size: 14px;
                    margin: 0 0 12px 0;
                    line-height: 1.5;
                }}
                .repo-meta {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 16px;
                    font-size: 13px;
                    color: #586069;
                }}
                .meta-item {{
                    display: flex;
                    align-items: center;
                    gap: 4px;
                }}
                .language-color {{
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    display: inline-block;
                }}
                .stars-today {{
                    color: #28a745;
                    font-weight: 600;
                }}
                .footer {{
                    background-color: #f6f8fa;
                    padding: 20px 30px;
                    text-align: center;
                    font-size: 12px;
                    color: #586069;
                    border-top: 1px solid #e1e4e8;
                }}
                .github-icon {{
                    width: 20px;
                    height: 20px;
                    vertical-align: middle;
                    margin-right: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔥 GitHub Trending</h1>
                    <p>今日热门仓库排行榜 - {today}</p>
                </div>
                <div class="content">
        """
        
        # 语言颜色映射
        lang_colors = {
            'Python': '#3572A5',
            'JavaScript': '#f1e05a',
            'TypeScript': '#2b7489',
            'Java': '#b07219',
            'Go': '#00ADD8',
            'Rust': '#dea584',
            'C++': '#f34b7d',
            'C': '#555555',
            'C#': '#178600',
            'PHP': '#4F5D95',
            'Ruby': '#701516',
            'Swift': '#ffac45',
            'Kotlin': '#A97BFF',
            'HTML': '#e34c26',
            'CSS': '#563d7c',
            'Shell': '#89e051',
            'Vue': '#41b883',
            'Unknown': '#cccccc'
        }
        
        for repo in repositories:
            lang_color = lang_colors.get(repo['language'], '#cccccc')
            
            html += f"""
                    <div class="repo-item">
                        <div class="rank">#{repo['rank']}</div>
                        <div class="repo-info">
                            <h2 class="repo-name">
                                <a href="{repo['url']}" target="_blank">{repo['name']}</a>
                            </h2>
                            <p class="repo-desc">{repo['description']}</p>
                            <div class="repo-meta">
                                <span class="meta-item">
                                    <span class="language-color" style="background-color: {lang_color};"></span>
                                    {repo['language']}
                                </span>
                                <span class="meta-item">⭐ {repo['stars']}</span>
                                <span class="meta-item stars-today">📈 +{repo['stars_today']} today</span>
                                <span class="meta-item">🍴 {repo['forks']}</span>
                            </div>
                        </div>
                    </div>
            """
        
        html += """
                </div>
                <div class="footer">
                    <p>此邮件由 GitHub Trending 自动推送服务发送</p>
                    <p>每天早8点为您推送最新热门项目</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_trending_email(self, repositories: List[Dict]) -> bool:
        """
        发送GitHub Trending邮件
        
        Args:
            repositories: 仓库信息列表
            
        Returns:
            发送是否成功
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            subject = f"🔥 GitHub Trending - {today} 热门仓库Top10"
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 创建HTML内容
            html_content = self._create_html_content(repositories)
            
            # 添加HTML部分
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 连接SMTP服务器并发送
            logger.info(f"正在连接SMTP服务器: {self.smtp_server}:{self.smtp_port}")
            
            # QQ邮箱使用SSL连接
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.set_debuglevel(0)
            
            logger.info("正在登录邮箱...")
            server.login(self.sender_email, self.sender_password)
            
            logger.info(f"正在发送邮件到: {self.receiver_email}")
            server.sendmail(
                self.sender_email,
                [self.receiver_email],
                msg.as_string()
            )
            
            server.quit()
            logger.info("邮件发送成功！")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"邮箱认证失败，请检查邮箱地址和授权码是否正确: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP错误: {e}")
            return False
        except Exception as e:
            logger.error(f"发送邮件时发生错误: {e}")
            return False


if __name__ == "__main__":
    # 测试邮件发送
    test_repos = [
        {
            'rank': 1,
            'name': 'test/repo',
            'url': 'https://github.com/test/repo',
            'description': '这是一个测试仓库',
            'language': 'Python',
            'stars': '10,000',
            'stars_today': '500',
            'forks': '1,000'
        }
    ]
    
    sender = EmailSender()
    sender.send_trending_email(test_repos)
