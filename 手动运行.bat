@echo off
chcp 65001 >nul
echo ========================================
echo GitHub Trending 邮件推送 - 手动运行
echo ========================================
cd /d "%~dp0"
python main.py --once
echo.
echo 按任意键退出...
pause >nul
