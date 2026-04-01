"""
GitHub Trending 爬虫模块
用于抓取GitHub Trending页面的项目信息
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

from config import TRENDING_URL, HEADERS, TOP_N

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GitHubTrendingCrawler:
    """GitHub Trending 爬虫类"""
    
    def __init__(self):
        self.url = TRENDING_URL
        self.headers = HEADERS
        self.top_n = TOP_N
    
    def fetch_page(self) -> str:
        """
        获取GitHub Trending页面HTML内容
        
        Returns:
            HTML页面内容
        """
        try:
            logger.info(f"正在获取GitHub Trending页面: {self.url}")
            response = requests.get(
                self.url,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            logger.info("页面获取成功")
            return response.text
        except requests.RequestException as e:
            logger.error(f"获取页面失败: {e}")
            raise
    
    def parse_repositories(self, html: str) -> List[Dict]:
        """
        解析HTML，提取仓库信息
        
        Args:
            html: 页面HTML内容
            
        Returns:
            仓库信息列表，每个仓库包含以下字段：
            - rank: 排名
            - name: 仓库名称
            - url: 仓库链接
            - description: 项目描述
            - language: 主要编程语言
            - stars: 星标数
            - stars_today: 今日新增星标
            - forks: 分支数
        """
        soup = BeautifulSoup(html, 'html.parser')
        repositories = []
        
        # GitHub Trending页面的仓库选择器
        # 查找所有article标签，每个代表一个仓库
        articles = soup.find_all('article', class_='Box-row')
        
        logger.info(f"找到 {len(articles)} 个仓库")
        
        for rank, article in enumerate(articles[:self.top_n], 1):
            try:
                repo_info = self._parse_repository(article, rank)
                if repo_info:
                    repositories.append(repo_info)
            except Exception as e:
                logger.warning(f"解析第 {rank} 个仓库时出错: {e}")
                continue
        
        logger.info(f"成功解析 {len(repositories)} 个仓库信息")
        return repositories
    
    def _parse_repository(self, article, rank: int) -> Dict:
        """
        解析单个仓库的信息
        
        Args:
            article: BeautifulSoup article元素
            rank: 排名
            
        Returns:
            仓库信息字典
        """
        # 获取仓库名称和链接
        # 仓库链接在h2 > a中
        h2_tag = article.find('h2')
        if not h2_tag:
            return None
            
        a_tag = h2_tag.find('a')
        if not a_tag:
            return None
        
        # 提取仓库名称（去除空白字符）
        repo_name = a_tag.get_text(strip=True).replace('\n', '').replace(' ', '')
        repo_url = f"https://github.com{a_tag.get('href', '')}"
        
        # 获取项目描述
        description = ""
        # 描述在p标签中，class包含col-9
        desc_p = article.find('p', class_=lambda x: x and 'col-9' in x)
        if desc_p:
            description = desc_p.get_text(strip=True)
        
        # 获取编程语言
        language = "Unknown"
        # 语言在span中，itemprop="programmingLanguage"
        lang_span = article.find('span', {'itemprop': 'programmingLanguage'})
        if lang_span:
            language = lang_span.get_text(strip=True)
        
        # 获取星标数和今日新增
        stars = "0"
        stars_today = "0"
        
        # 查找所有包含数字和星标的span
        all_spans = article.find_all('span', class_=lambda x: x and 'd-inline-block' in x)
        
        for span in all_spans:
            text = span.get_text(strip=True)
            # 查找总星标数（包含星标图标）
            if 'star' in text.lower() and 'today' not in text.lower():
                # 提取数字
                num_text = ''.join([c for c in text if c.isdigit() or c == ','])
                if num_text:
                    stars = num_text
            # 查找今日新增
            elif 'today' in text.lower():
                # 提取今日新增数字
                num_text = ''.join([c for c in text if c.isdigit() or c in [',', '+']])
                if num_text:
                    stars_today = num_text
        
        # 如果没有找到今日新增，尝试其他选择器
        if stars_today == "0":
            today_span = article.find('span', class_=lambda x: x and 'today' in str(x).lower())
            if today_span:
                text = today_span.get_text(strip=True)
                num_text = ''.join([c for c in text if c.isdigit() or c in [',', '+']])
                if num_text:
                    stars_today = num_text
        
        # 获取分支数
        forks = "0"
        # 查找包含fork的span
        for span in all_spans:
            text = span.get_text(strip=True)
            if 'fork' in text.lower():
                num_text = ''.join([c for c in text if c.isdigit() or c == ','])
                if num_text:
                    forks = num_text
                    break
        
        # 如果星标数为0，尝试从链接的href属性获取（GitHub新界面）
        if stars == "0":
            # 查找包含星标链接的a标签
            star_links = article.find_all('a', href=lambda x: x and 'stargazers' in x)
            for link in star_links:
                text = link.get_text(strip=True)
                num_text = ''.join([c for c in text if c.isdigit() or c == ','])
                if num_text:
                    stars = num_text
                    break
        
        # 如果分支数为0，尝试从链接获取
        if forks == "0":
            fork_links = article.find_all('a', href=lambda x: x and 'forks' in x)
            for link in fork_links:
                text = link.get_text(strip=True)
                num_text = ''.join([c for c in text if c.isdigit() or c == ','])
                if num_text:
                    forks = num_text
                    break
        
        return {
            'rank': rank,
            'name': repo_name,
            'url': repo_url,
            'description': description or "暂无描述",
            'language': language,
            'stars': stars,
            'stars_today': stars_today,
            'forks': forks
        }
    
    def get_trending_repositories(self) -> List[Dict]:
        """
        获取GitHub Trending仓库列表（主入口）
        
        Returns:
            仓库信息列表
        """
        html = self.fetch_page()
        return self.parse_repositories(html)


if __name__ == "__main__":
    # 测试爬虫
    crawler = GitHubTrendingCrawler()
    try:
        repos = crawler.get_trending_repositories()
        print(f"\n成功获取 {len(repos)} 个Trending仓库:\n")
        for repo in repos:
            print(f"[{repo['rank']}] {repo['name']}")
            print(f"    链接: {repo['url']}")
            print(f"    描述: {repo['description']}")
            print(f"    语言: {repo['language']}")
            print(f"    星标: {repo['stars']} (今日 +{repo['stars_today']})")
            print(f"    分支: {repo['forks']}")
            print()
    except Exception as e:
        logger.error(f"测试失败: {e}")
