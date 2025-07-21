import json


def admin_menu():
    while True:
        print("\n==== Admin Panel ====")
        print("1. Add New Question")
        print("2. Search Questions")
        print("3. Exit Admin")
        choice = input("Enter your choice (1-3) : ")  # FIXME
        # choice = utils.get_input(提示词,可能的选项)

        if choice == '1':
            print("add_question")
            # add_question()
        elif choice == '2':
            print("search_questions")
            # search_questions()
        elif choice == '3':
            break


def add_question():
    print("\n=== Add New Question ===")
    # 输入问题，如问题内容为空直接结束
    question = input("Enter new question:").strip()
    if not question:
        print("New question cannot be empty.")
        return
    # 循环输入选项，如选项内容为空直接结束
    options = []
    for i in range(4):
        option = input(f"Enter option {chr(65 + i)}: ").strip()
        if not option:
            print("Option cannot be empty.")
            return
        options.append(option)
    # 输入正确答案
    correct_answer = input("Enter correct answer (A-D): ").strip()  # FIXME

    new_question = {
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    }

    try:
        with open('data/questions.json', 'r+') as f:  # 读写模式打开
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
