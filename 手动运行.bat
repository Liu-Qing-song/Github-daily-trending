@echo off
chcp 65001 >nul
echo ========================================
echo GitHub Trending 邮件推送 - 手动运行
echo ========================================
cd /d "C:\Users\Z00575KC\Desktop\LQS\Others\Github daily trending"
python main.py --once
echo.
echo 按任意键退出...
pause >nul
