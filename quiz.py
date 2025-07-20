import json


def quiz_menu():
    while True:
        print("\n=== Quiz Menu ===")
        print("1. Take Quiz")  # 测验
        print("2. Search Questions")  # 搜索题目
        print("3. Exit to Main Menu")  # 退出至主菜单
        choice = input("Enter your choice (1-3) : ")  # FIXME
        # choice = utils.get_input(提示词,可能的选项)

        if choice == "1":  # 测验
            # TODO: take_quiz()
            print("Take Quiz")
        elif choice == "2":  # 搜索题目
            # TODO: search_questions()
            print("Search Questions")
        elif choice == "3":  # 退出至主菜单
            break


def load_questions():  # 加载问题
    try:
        with open("data/question.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        # questions_num = len(questions)
        # 验证data结构
        for question in questions:
            # 验证每个question中是否都有 "question", "options", "correct_answer"
            if not all(key in question for key in ["question", "options", "correct_answer"]):  # 生成器表达式 返回值是bool序列
                # print("Invalid question format")
                raise ValueError("Invalid question format")  # 抛出错误，终止程序
            # 验证每个question的选项是否都有4个
            if len(question["options"]) != 4:
                raise ValueError("Each question must have 4 options")
        return questions

    except FileNotFoundError:  # 文件路径错误
        print("Error: Questions file not found")
        return []
    except json.JSONDecodeError:  # 不符合json格式
        print("Error: Invalid JSON format")
        return []
    except Exception as e:  # 其他错误 TODO: 细化报错类型
        print(f"Error loading questions: {e}")
        return []
