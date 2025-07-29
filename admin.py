import json
import utils


def admin_menu():
    while True:
        print("\n==== Admin Panel ====")
        print("1. Add New Question")
        print("2. Search Questions")
        print("3. Exit Admin")
        choice = utils.get_choice(['1', '2', '3'], "Enter your choice (1-3) : ")
        # choice = input("Enter your choice (1-3) : ")

        if choice == '1':
            add_question()
        elif choice == '2':
            search_questions_admin()
        elif choice == '3':
            break


def add_question():
    print("\n=== Add New Question ===")
    # 输入问题，如问题内容为空直接结束
    question = input("Enter new question:").strip()
    if not question:
        print("-New question cannot be empty.-")
        return
    # 循环输入选项，如选项内容为空直接结束
    options = []
    for i in range(4):
        option = input(f"Enter option {chr(65 + i)}: ").strip()
        if not option:
            print("-Option cannot be empty.-")
            return
        options.append(option)
    # 输入正确答案
    correct_answer = utils.get_choice(['A', 'B', 'C', 'D'], "Enter correct answer (A-D): ")
    # correct_answer = input("Enter correct answer (A-D): ").strip()
    explanation = input("Explanation (optional): ").strip()

    new_question = {
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }

    try:
        with open('data/question.json', 'r+', encoding='utf-8') as f:  # 读写模式打开
            questions = json.load(f)
            # 检查是否有重复问题
            if any(q['question'] == question for q in questions):
                print("Error: Identical question already exists!")
                return

            questions.append(new_question)
            f.seek(0)
            json.dump(questions, f, indent=2)
            f.truncate()

        print("Question added successfully!")

    except Exception as e:
        print(f"Error saving question: {str(e)}")


def search_questions_admin():
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

        action = input("Action: (E)dit, (D)elete, (N)ext: ").upper()
        if action == 'E':
            edit_question(questions, q)
        elif action == 'D':
            delete_question(questions, q)


def edit_question(questions, question):
    print("\n=== Editing Question ===")
    print(f"Current: {question['question']}")
    new_text = input("New question (leave blank to keep): ").strip()
    if new_text:
        question['question'] = new_text

    # 编辑选项
    for i in range(4):
        print(f"Current option {chr(65 + i)}: {question['options'][i]}")
        new_opt = input(f"New option {chr(65 + i)} (leave blank to keep): ").strip()
        if new_opt:
            question['options'][i] = new_opt

    new_correct = input(f"New correct answer (current: {question['correct_answer']}): ").upper().strip()
    if new_correct in ['A', 'B', 'C', 'D']:
        question['correct_answer'] = new_correct

    # 保存更改
    with open('data/question.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2)
    print("Question updated!")


def delete_question(questions, question):
    confirm = input("Are you sure? (y/n): ").lower()
    if confirm == 'y':
        questions.remove(question)
        with open('data/question.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2)
        print("Question deleted!")