import json
import random
import time
import utils
from datetime import datetime
import threading


# A global variable is used to track the countdown
TIMER_ACTIVE = True
TIME_REMAINING = 300  # 5 minutes = 300 seconds

def quiz_menu():
    while True:
        print("\n=== Quiz Menu ===")
        print("1. Take Quiz")
        print("2. Search Questions")
        print("3. Exit to Main Menu")
        choice = utils.get_choice(['1', '2', '3'], "Enter your choice (1-3): ")
        # choice = input("Enter your choice (1-4) : ")

        if choice == '1':  # test
            name = input("Enter your name: ").strip()
            take_quiz(name)
        elif choice == '2':  # Search questions
            search_question()
        elif choice == '3':  # Exit to the main menu
            break


def load_questions():  # 加载问题
    try:
        with open("data/question.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        # questions_num = len(questions)
        # Verify data structure
        for question in questions:
            # Verify that each question contains "question", "options", "correct_answer", and "explanation"
            if not all(key in question for key in ["question", "options", "correct_answer", "explanation"]):  # 生成器表达式 返回值是bool序列
                # print("Invalid question format")
                raise ValueError("Invalid question format")  # Throw an error and terminate the program
            # Verify that each question has 4 options
            if len(question["options"]) != 4:
                raise ValueError("Each question must have 4 options")
        return questions

    except FileNotFoundError:  # wrong file path
        print("Error: Questions file not found")
        return []
    except json.JSONDecodeError:  # Does not conform to json format
        print("Error: Invalid JSON format")
        return []
    except Exception as e:  # Other errors
        print(f"Error loading questions: {e}")
        return []


# Countdown thread function
def countdown_timer():
    global TIME_REMAINING, TIMER_ACTIVE

    # Set reminder time: 1.25 minutes (75 seconds), 2.5 minutes (150 seconds), 3.75 minutes (225 seconds)
    reminders = [225, 150, 75]
    next_reminder = reminders.pop() if reminders else None

    while TIME_REMAINING > 0 and TIMER_ACTIVE:
        time.sleep(1)
        TIME_REMAINING -= 1

        # Check if a reminder is needed
        if next_reminder and TIME_REMAINING <= next_reminder:
            minutes = next_reminder // 60
            seconds = next_reminder % 60
            print(f"\n⏰ Time reminder: {minutes} minutes {seconds} seconds remaining")
            next_reminder = reminders.pop() if reminders else None

    # end of time
    if TIME_REMAINING <= 0 and TIMER_ACTIVE:
        print("\n⏰ Time's up! Quiz ended automatically")


def take_quiz(user_name):
    global TIMER_ACTIVE, TIME_REMAINING

    # Reset timer state
    TIMER_ACTIVE = True
    TIME_REMAINING = 300  # 10 minutes = 600 seconds
    all_questions = load_questions()
    if not all_questions:
        print("No questions available. Contact admin.")
        return

    # Randomly select 10 questions
    quiz_questions = random.sample(all_questions, min(10, len(all_questions)))
    user_answer = []
    score = 0
    start_time = time.time()

    # Start the countdown thread
    timer_thread = threading.Thread(target=countdown_timer)
    timer_thread.daemon = True  # Set as daemon thread
    timer_thread.start()

    print("\n=== Quiz Started ===")
    print(f"- This quiz contains {len(quiz_questions)} questions -")
    print(f"- Total time limit: 10 minutes -")

    # If there are less than 10 questions, the score will not be included in the ranking list
    if len(quiz_questions) < 10:
        print("- Note: Less than 10 questions available, results will not be saved to leaderboard -")

    # Start answering questions
    for i, q in enumerate(quiz_questions):
        #Check if time has expired
        if TIME_REMAINING <= 0:
            print("\n⏰ Time's up! Quiz ended")
            break

        # Display time usage after question 5 is completed
        if i == 5:  # Question 6 (subscript 5)
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

    # Stop timer
    TIMER_ACTIVE = False
    end_time = time.time()
    time_elapsed = end_time - start_time

    # Ensure that the timing thread ends
    timer_thread.join(timeout=1)

    # Calculate and display the results
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
            # Only keep the top 10
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

    # If there are no mistakes, display a congratulatory message
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
