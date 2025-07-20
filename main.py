import json
import os


def main_menu():
    print("\n===Smart Online Quiz System ===")
    print("Welcome to Smart Online Quiz System")
    print("1. Quiz Module")  # 测验
    print("2. View Leaderboard")  # 显示排行榜
    print("3. Admin Login")  # 管理员系统
    print("4. Exit")  # 退出
    # 还需要写分支代码进入各个模块（封装还是直接写？）
    # return 返回1 or 2 or 3 or 4
    # TODO: 待封装，和quiz中的回答问题部分共用一个 判断回答是否在那部分范围内，return返回值的def。main_menu()直接return那个def
    choice = input("Enter choice (1-4): ")  # FIXME: 超出1-4范围需要检测
    return choice
    # return utils.get_input(提示词,可能的选项)


def main():
    # 初始化data目录
    # 检测data目录是否存在，如果不存在新建data目录
    if not os.path.exists("data"):
        os.mkdir("data")

    # 初始化question文件
    if not os.path.exists("data/question.json"):  # 如果不存在，以写入状态打开（自动新建），并写入空列表
        with open("data/question.json", "w") as f:
            json.dump([], f)
    # 初始化leaderboard文件
    if not os.path.exists("data/leaderboard.json"):  # 如果不存在，以写入状态打开（自动新建），并写入空列表
        with open("data/leaderboard.json", "w") as f:
            json.dump([], f)

    while True:
        # 打开主菜单
        choice = main_menu()
        if choice == '1':  # 测验
            # TODO: 进测验模块
            print("Quiz Module")
        elif choice == "2":  # 显示排行榜
            # TODO: 显示排行榜
            print("View Leaderboard")
        elif choice == "3":  # 管理员系统
            password = input("Enter Admin Password: ")  # 输密码
            if password == "PASSWORD":  # 判断密码 默认密码是"PASSWORD"
                # TODO: 进管理员系统
                print("Admin Login")
            else:  # 密码无效，返回主菜单
                print("Invalid password! Returning to main menu.")
        elif choice == "4":
            print("Exiting the system, welcome to use next time, goodbye!")
            break  # 跳出循环


if __name__ == "__main__":
    main()
