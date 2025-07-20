import json
import os


def main_menu():
    print("\n===Smart Online Quiz System ===")
    print("Welcome to Smart Online Quiz System")
    print("1. Take Quiz")  # 测验
    print("2. View Leaderboard")  # 显示排行榜
    print("3. Admin Login")  # 管理员系统
    print("4. Exit")  # 退出
    # 还需要写分支代码进入各个模块（封装还是直接写？）
    # return 返回1 or 2 or 3 or 4


def main():
    # 初始化data目录
    # 检测data目录是否存在，如果不存在新建data目录
    if not os.path.exists("data"):
        os.mkdir("data")



