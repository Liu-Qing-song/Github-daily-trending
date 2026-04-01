"""
GitHub Trending 每日推送主程序
每天早上8点自动获取GitHub Trending项目并发送邮件
"""

import time
import schedule
import logging
from datetime import datetime

from config import PUSH_HOUR, PUSH_MINUTE
from crawler import GitHubTrendingCrawler
from email_sender import EmailSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('github_trending.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class GitHubTrendingBot:
    """GitHub Trending 推送机器人"""
    
    def __init__(self):
        self.crawler = GitHubTrendingCrawler()
        self.email_sender = EmailSender()
    
    def run_once(self) -> bool:
        """
        执行一次完整的抓取和推送流程
        
        Returns:
            执行是否成功
        """
        try:
            logger.info("=" * 60)
            logger.info("开始执行 GitHub Trending 推送任务")
            logger.info("=" * 60)
            
            # 1. 获取Trending仓库
            logger.info("步骤1: 获取GitHub Trending仓库...")
            repositories = self.crawler.get_trending_repositories()
            
            if not repositories:
                logger.error("未获取到任何仓库信息，任务终止")
                return False
            
            logger.info(f"成功获取 {len(repositories)} 个仓库")
            
            # 2. 发送邮件
            logger.info("步骤2: 发送邮件推送...")
            success = self.email_sender.send_trending_email(repositories)
            
            if success:
                logger.info("✅ 任务执行成功！")
            else:
                logger.error("❌ 邮件发送失败")
            
            logger.info("=" * 60)
            return success
            
        except Exception as e:
            logger.error(f"任务执行过程中发生错误: {e}")
            return False
    
    def scheduled_job(self):
        """定时任务入口"""
        logger.info(f"⏰ 定时任务触发 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.run_once()
    
    def start_scheduler(self):
        """启动定时调度器"""
        # 设置每天定时执行
        schedule_time = f"{PUSH_HOUR:02d}:{PUSH_MINUTE:02d}"
        schedule.every().day.at(schedule_time).do(self.scheduled_job)
        
        logger.info("=" * 60)
        logger.info("GitHub Trending 推送服务已启动")
        logger.info(f"推送时间: 每天 {schedule_time}")
        logger.info("按 Ctrl+C 停止服务")
        logger.info("=" * 60)
        
        # 立即执行一次（用于测试）
        # self.run_once()
        
        # 保持程序运行
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except KeyboardInterrupt:
                logger.info("\n服务已停止")
                break
            except Exception as e:
                logger.error(f"调度器发生错误: {e}")
                time.sleep(60)


def main():
    """主函数"""
    import sys
    
    bot = GitHubTrendingBot()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            # 只执行一次
            logger.info("执行单次任务模式")
            bot.run_once()
        elif sys.argv[1] == '--help':
            print("""
GitHub Trending 每日推送工具

用法:
  python main.py           启动定时服务（每天8点自动推送）
  python main.py --once    立即执行一次推送
  python main.py --help    显示帮助信息

配置:
  请先在 config.py 中配置你的邮箱信息：
  - SENDER_EMAIL: 发件人QQ邮箱
  - SENDER_PASSWORD: 邮箱授权码（不是登录密码！）
  - RECEIVER_EMAIL: 收件人邮箱

获取QQ邮箱授权码:
  1. 登录QQ邮箱网页版
  2. 设置 -> 账户 -> 开启SMTP服务
  3. 按照提示获取授权码
            """)
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("使用 --help 查看帮助")
    else:
        # 启动定时服务
        bot.start_scheduler()


if __name__ == "__main__":
    main()
