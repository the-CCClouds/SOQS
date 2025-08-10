import json
import os
import admin
import quiz
import utils


def main_menu():
    print("\n===Smart Online Quiz System ===")
    print("Welcome to Smart Online Quiz System")
    print("1. Quiz Module")
    print("2. View Leaderboard")
    print("3. Admin Login")
    print("4. Exit")
    return utils.get_choice(['1', '2', '3', '4'], "Enter choice (1-4): ")


def main():
    # Initialize data directory
    # Check if the data directory exists, if not create a new data directory
    if not os.path.exists("data"):
        os.mkdir("data")

    # Initialize the question file
    if not os.path.exists("data/question.json"):  # 如果不存在，以写入状态打开（自动新建），并写入空列表
        with open("data/question.json", "w", encoding="utf-8") as f:
            json.dump([], f)
    # Initialize the leaderboard file
    if not os.path.exists("data/leaderboard.json"):  # 如果不存在，以写入状态打开（自动新建），并写入空列表
        with open("data/leaderboard.json", "w", encoding="utf-8") as f:
            json.dump([], f)

    while True:
        # Open main menu
        choice = main_menu()
        if choice == '1':  # test
            quiz.quiz_menu()
        elif choice == "2":  # Show leaderboard
            quiz.view_leaderboard()
        elif choice == "3":  # Administrator system
            password = input("Enter Admin Password: ")  # Enter password
            if password == "PASSWORD":  # Determine the password. The default password is "PASSWORD"
                admin.admin_menu()
            else:  # Invalid password, return to main menu
                print("-Invalid password! Returning to main menu.-")
        elif choice == "4":
            print("-Exiting the system, welcome to use next time, goodbye!-")
            break  # Break out of loop


if __name__ == "__main__":
    main()
