import json
import random
import time
import utils
from datetime import datetime
import threading


# 全局变量用于跟踪倒计时
TIMER_ACTIVE = True
TIME_REMAINING = 300  # 5分钟 = 300秒


# 自定义超时异常
# class TimeoutError(Exception):
#     pass


def quiz_menu():
    while True:
        print("\n=== Quiz Menu ===")
        print("1. Take Quiz")  # 测验
        print("2. Search Questions")  # 搜索题目
        print("3. Exit to Main Menu")  # 退出至主菜单
        choice = utils.get_choice(['1', '2', '3'], "Enter your choice (1-3): ")
        # choice = input("Enter your choice (1-4) : ")

        if choice == '1':  # 测验
            name = input("Enter your name: ").strip()
            take_quiz(name)
        elif choice == '2':  # 搜索题目
            search_question()
        elif choice == '3':  # 退出至主菜单
            break


def load_questions():  # 加载问题
    try:
        with open("data/question.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        # questions_num = len(questions)
        # 验证data结构
        for question in questions:
            # 验证每个question中是否都有 "question", "options", "correct_answer", "explanation"
            if not all(key in question for key in ["question", "options", "correct_answer", "explanation"]):  # 生成器表达式 返回值是bool序列
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
    except Exception as e:  # 其他错误
        print(f"Error loading questions: {e}")
        return []


# 倒计时线程函数
def countdown_timer():
    global TIME_REMAINING, TIMER_ACTIVE

    # 设置提醒点：1.25分钟(75秒), 2.5分钟(150秒), 3.75分钟(225秒)
    reminders = [225, 150, 75]
    next_reminder = reminders.pop() if reminders else None

    while TIME_REMAINING > 0 and TIMER_ACTIVE:
        time.sleep(1)
        TIME_REMAINING -= 1

        # 检查是否需要提醒
        if next_reminder and TIME_REMAINING <= next_reminder:
            minutes = next_reminder // 60
            seconds = next_reminder % 60
            print(f"\n⏰ Time reminder: {minutes} minutes {seconds} seconds remaining")
            next_reminder = reminders.pop() if reminders else None

    # 时间结束
    if TIME_REMAINING <= 0 and TIMER_ACTIVE:
        print("\n⏰ Time's up! Quiz ended automatically")


# 获取超时输入
# def get_choice_with_timeout(valid_options, prompt, timeout):
#     start_time = time.time()
#     print(prompt, end='', flush=True)

    # while True:
    #     检查是否超时
    #     if time.time() - start_time > timeout:
    #         raise TimeoutError("Input timeout")

        # Windows 特定的输入检查
        # if sys.platform == "win32":
        #     import msvcrt
        #     if msvcrt.kbhit():
        #         char = msvcrt.getwch()
        #         if char in ['\r', '\n']:
        #             continue
        #         user_input = char.upper()
        #         print(user_input, end='', flush=True)
        #         if user_input in valid_options:
        #             print()  # 换行
        #             return user_input
        #         print(f"\nInvalid input. Valid options: {', '.join(valid_options)}")
        #         print(prompt, end='', flush=True)
        # else:
            # Unix
            # import select
            # rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            # if rlist:
            #     user_input = sys.stdin.readline().strip().upper()
            #     if user_input in valid_options:
            #         return user_input
            #     print(f"Invalid input. Valid options: {', '.join(valid_options)}")
            #     print(prompt, end='', flush=True)
        #
        # 避免高CPU使用率
        # time.sleep(0.05)


def take_quiz(user_name):
    global TIMER_ACTIVE, TIME_REMAINING

    # 重置计时器状态
    TIMER_ACTIVE = True
    TIME_REMAINING = 300  # 10分钟 = 600秒

    all_questions = load_questions()
    if not all_questions:
        print("No questions available. Contact admin.")
        return

    # 随机选取10道题
    quiz_questions = random.sample(all_questions, min(10, len(all_questions)))
    user_answer = []
    score = 0
    start_time = time.time()

    # 启动倒计时线程
    timer_thread = threading.Thread(target=countdown_timer)
    timer_thread.daemon = True  # 设置为守护线程
    timer_thread.start()

    print("\n=== Quiz Started ===")
    print(f"- This quiz contains {len(quiz_questions)} questions -")
    print(f"- Total time limit: 10 minutes -")

    # 如果题目少于10题，成绩不计入排行榜
    if len(quiz_questions) < 10:
        print("- Note: Less than 10 questions available, results will not be saved to leaderboard -")

    # 开始答题
    for i, q in enumerate(quiz_questions):
        # 检查时间是否用完
        if TIME_REMAINING <= 0:
            print("\n⏰ Time's up! Quiz ended")
            break

        # 在第5题完成后显示时间使用情况
        if i == 5:  # 第6题（下标为5）
            elapsed = time.time() - start_time
            elapsed_min = int(elapsed // 60)
            elapsed_sec = int(elapsed % 60)
            remaining_min = TIME_REMAINING // 60
            remaining_sec = TIME_REMAINING % 60
            print(f"\n⏱️ Time update: Completed 5 questions in {elapsed_min} minutes {elapsed_sec} seconds")
            print(f"⏱️ Time update: {remaining_min} minutes {remaining_sec} seconds remaining")

        print(f"\nQuestion {i + 1}/{len(quiz_questions)}: {q['question']}")
        for j, option in enumerate(q["options"]):
            print(f"{chr(j + 65)}. {option}")

        answer = utils.get_choice(['A', 'B', 'C', 'D'], "Your answer (A-D): ")

        user_answer.append(answer)
        if answer == q["correct_answer"]:
            score += 1
            print("✅ Correct!")
        else:
            print(f"❌ Correct answer is {q['correct_answer']}")

    # 停止计时器
    TIMER_ACTIVE = False
    end_time = time.time()
    time_elapsed = end_time - start_time

    # 确保计时线程结束
    timer_thread.join(timeout=1)

    # 计算并显示结果
    calculate_score(score, len(quiz_questions), time_elapsed)
    if len(quiz_questions) == 10:
        save_results(user_name, score * 10, utils.format_duration(time_elapsed))
    show_incorrect_answers(quiz_questions, user_answer)


def calculate_score(score, questions_num, time_elapsed):
    print("\n=== Quiz Results ===")
    score_calculated = (score / questions_num) * 100
    print(f"Score: {score_calculated:.1f}%.")

    if score_calculated >= 90:
        print("Performance: Excellent!")
    elif score_calculated >= 70:
        print("Performance: Good!")
    elif score_calculated >= 50:
        print("Performance: Fair")
    else:
        print("Performance: Needs Improvement")

    print(f"Time taken: {utils.format_duration(time_elapsed)}")  # 用时,精确到小数点后三位


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
            sorted_leaderboard = sorted(
                leaderboard,
                key=lambda x: (-x['score'], x['time'])
            )

            # 去重，同一个名字只保留最好成绩
            # unique_leaderboard = []
            # seen_names = set()
            # for entry in sorted_leaderboard:
            #     if entry['name'] not in seen_names:
            #         unique_leaderboard.append(entry)
            #         seen_names.add(entry['name'])
            # 只保留前10名
            # top_10 = unique_leaderboard[:10]

            # 只保留前10名
            top_10 = sorted_leaderboard[:10]
            f.seek(0)
            json.dump(top_10, f, indent=2)
            f.truncate()

    except Exception as e:
        print(f"Error saving results: {str(e)}")


def view_leaderboard():
    try:
        with open('data/leaderboard.json', 'r', encoding="utf-8") as f:
            leaderboard = json.load(f)

        print("\n=== Top 10 Leaderboard ===")
        print("Rank | Name         | Score | Time(s)       | Date")
        print("-" * 65)
        for i, entry in enumerate(leaderboard[:10]):
            print(f"{i + 1:2}   | {entry['name'][:12]:12} | {entry['score']:5} | {entry['time']:13} | {entry['timestamp']}")

    except FileNotFoundError:
        print("Leaderboard is empty!")
    except json.JSONDecodeError:
        print("Error: Invalid leaderboard data")
    except Exception as e:
        print(f"Error loading leaderboard data: {e}")


def show_incorrect_answers(questions, user_answers):
    print("\n=== Incorrect Answers Review ===")
    incorrect_count = 0

    for i, (q, ans) in enumerate(zip(questions, user_answers)):
        if ans != q['correct_answer']:
            incorrect_count += 1
            print(f"\nQuestion {i + 1}: {q['question']}")
            print(f"Your answer: {ans}")
            print(f"Correct answer: {q['correct_answer']}")
            print(f"Explanation: {q.get('explanation', 'No explanation available')}")

    # 如果没有错题，显示祝贺信息
    if incorrect_count == 0:
        print("Congratulations! No incorrect answers")


def search_question():
    try:
        with open('data/question.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except Exception as e:
        print(f"No questions available: {str(e)}")
        return

    keyword = input("Enter search keyword: ").lower().strip()
    if not keyword:
        print("Keyword cannot be empty!")
        return

    results = [q for q in questions if keyword in q['question'].lower()]

    print(f"\nFound {len(results)} matching questions:")
    for i, q in enumerate(results):
        print(f"\nQ{i + 1}: {q['question']}")
        for j, opt in enumerate(q['options']):
            print(f"   {chr(65 + j)}. {opt}")
        print(f"Correct: {q['correct_answer']}")

        action = input("Action: (N)ext, any other key to exit: ").strip().upper()
        if action == 'N':
            search_question()
