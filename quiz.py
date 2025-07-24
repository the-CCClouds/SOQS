import json
import random
import time
import utils
from datetime import datetime

# TODO：快速问答时长设置10s
def quiz_menu():
    while True:
        print("\n=== Quiz Menu ===")
        print("1. Take Quiz")  # 测验
        print("2. Take Quick Questions")  # 快速问答
        print("3. Search Questions")  # 搜索题目
        print("4. Exit to Main Menu")  # 退出至主菜单
        choice = utils.get_choice(['1', '2', '3', '4'], "Enter your choice (1-4): ")
        # choice = input("Enter your choice (1-4) : ")


        if choice == '1':  # 测验
            name = input("Enter your name: ").strip()
            take_quiz(name)
        elif choice == '2':  # 快速问答
            # TODO: take_quick_quiz()
            print("Take Quick Questions")
        elif choice == '3':  # 搜索题目
            # TODO: search_questions()
            print("Search Questions")
        elif choice == '4':  # 退出至主菜单
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

# 进行测试
def take_quiz(user_name):
    all_questions = load_questions()
    if not all_questions:
        print("No questions available. Contact admin.")
        return

    # 随机选取10道题
    quiz_questions = random.sample(all_questions, min(10, len(all_questions)))  # 防止题库内有题目但是小于10题
    user_answer = []
    score = 0
    start_time = time.time()

    print("\n===Quiz Started===")
    print(f"-This quiz has a total of {len(quiz_questions)} questions-") # 显示题目数量
    # 如果题目少于10题，成绩不计入排行榜
    if len(quiz_questions) < 10:
        print("-Because this quiz has less than 10 questions, the results of this quiz are not be included in the leaderboard-")
    for i, q in enumerate(quiz_questions):  # 用enumerate同时遍历索引和值
        print(f"Question {i + 1}: {q['question']}")
        for j, option in enumerate(q["options"]):
            print(f"{chr(j + 65)}. {option}")

        answer = utils.get_choice(['A', 'B', 'C', 'D'], "Your answer is(A-D): ")
        # answer = input("Your answer is(A-D): ")
        user_answer.append(answer)
        if answer == q["correct_answer"]:
            score += 1
            print("✅ Correct!")
        else:
            print(f"❌ Correct Answer is {q['correct_answer']}")

    end_time = time.time()
    time_elapsed = end_time - start_time  # FIXME
    print(type(time_elapsed))
    time_test = int(end_time - time_elapsed)  # FIXME
    print(type(time_test))

    print(user_name, score, start_time, end_time, time_elapsed, time_test)  # FIXME

    calculate_score(score, len(quiz_questions), time_elapsed)
    if len(quiz_questions) == 10:
        save_results(user_name, score * 10, utils.format_duration(time_elapsed))
        # TODO: 排行榜
        print("save result")


def calculate_score(score, questions_num, time_elapsed):
    print("\n===Quiz Result===")
    score_calculated = (score / questions_num) * 100
    print(f"Your score is {score_calculated:.1f}%.")

    if score_calculated >= 90:
        print("Your results: Excellent!")
    elif score_calculated >= 70:
        print("Your results: Good!")
    elif score_calculated >= 50:
        print("Your results: Fair")
    else:
        print("Your results: Needs Improvement")

    print(f"Your elapsed time: {utils.format_duration(time_elapsed)}")  # 用时,精确到小数点后两位

def save_results(user_name, score, time_elapsed):
    try:
        with open('data/leaderboard.json', 'r+', encoding="utf-8") as f:
            try:
                leaderboard = json.load(f)
            except json.JSONDecodeError:
                leaderboard = []

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            leaderboard.append({
                "name": user_name,
                "score": score,
                "time": time_elapsed,
                "timestamp": timestamp
            })
            # 按分数和时间排序
            leaderboard.sort(key=lambda x: (-x['score'], x['time']), reverse=True)
            # TODO: 去重
            # TODO: 只保留前10名
            f.seek(0)
            json.dump(leaderboard, f, indent=2)
            f.truncate()


    except Exception as e:
        print(f"Error saving results: {str(e)}")
