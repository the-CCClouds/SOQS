import json
import utils


def admin_menu():
    while True:
        print("\n==== Admin Panel ====")
        print("1. Add New Question")
        print("2. Search Questions")
        print("3. Import questions")
        print("4. Exit Admin")
        choice = utils.get_choice(['1', '2', '3', '4'], "Enter your choice (1-4) : ")
        # choice = input("Enter your choice (1-4) : ")

        if choice == '1':
            add_question()
        elif choice == '2':
            search_questions_admin()
        elif choice == '3':
            load_file_main()
        elif choice == '4':
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


def load_file_number():  # 加载问题数量的函数
    try:
        file_num = len(load_question_file('question.json'))
        return file_num
    except Exception as e:
        print('文件内没有内容')
        return 0


def load_question_file(file_name):  # 加载文件变量名是文件名字
    try:
        with open(f'data/{file_name}', 'r', encoding='utf-8')as f:
            print("✅ Successfully opened the file")
            question = json.load(f)
            return question
    except Exception as e:
        print('❌The question bank file does not exist or the format is incorrect or the content is empty', e)


def edit_question_file(question, file_name):  # 将旧内容进行覆盖
    """

    :param question:你新添加的问题变量名称
    :return: None
    """
    try:  # 先确保题库文件存在且是合法 JSON
         f = open(f'data/{file_name}', 'w', encoding='utf-8')
    except Exception as e:
        print(f'❌File not found{e}')
        return False
    json.dump(question, f, ensure_ascii=False, indent=2)
    print("✅ Successfully overwrote the file")
    return True


def edit_question_file_add(new_question, file_name):  # 将新内容添加到就内容并进行合并覆盖
    """
    :param new_question:你新添加的问题变量名称
    :return: None
    """
    path = f'data/{file_name}'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            old = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        old = []  # 文件为空或损坏时兜底
    old.extend(new_question)  # 内存里合并
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(old, f, ensure_ascii=False, indent=2)  # 一次性覆盖
    print("✅ Successfully overwrote the file")


def file_clear():  # 清除文件内容
    try:
        file_name = input('please input file name:')
        file = open(f'data/{file_name}', 'w', encoding='utf-8')
        pass
        file.close()
    except Exception as e:
        print('❌You entered the wrong file name or the file location is incorrect')
        print(e)
        return False
    print("✅ Successfully cleared the file")
    return True


def load_file_main():  # 添加问题(文件形式)
    try:
        file_name = input('please input file name:')
        file = open(f'data/{file_name}', 'r', encoding='utf-8')
        file.flush()
    except Exception as e:
        print('You entered an incorrect file name or the file name is in the wrong place')
        print(e)
        return False  # 尝试输入和对错误的纠正
    f_num = load_file_number()
    lines = []
    add_success = 0
    add_fail = 0
    test_question = []
    idx = 0  # 指针位置
    for line in file:
        line = line.strip('\n')
        lines.append(line)  # 处理原文档中的空格和空行
    if f_num > 0:
        questions = load_question_file('question.json')
    while idx < len(lines):
        # question的处理
        if f_num > 0:
            parts = lines[idx].split(':', 1)
            repeat = False
            for q in questions:
                question_split = q['question']
                if parts[1].lower() == question_split.lower():
                    repeat = True
                    break
            if repeat:
                print('❌The problem already exists in the file')
                idx += 7
                add_fail += 1
                continue
            question = parts[1]
            f_num += 1

        else:
            parts = lines[idx].split(':', 1)
            question = parts[1]
        idx += 1
        # options的处理
        options=[]
        for opt in lines[idx:idx+4]:
            opt = opt.split('.')
            opt = opt[1]
            opt=opt.strip(' ')
            options.append(opt)
        idx+=4
        # answer的处理
        answer = lines[idx]
        answer = answer.replace('：', ':')
        answer = answer.split(':')
        answer = answer[1]
        answer = answer.strip(' ')
        idx += 1
        # explanation的处理
        explanation = lines[idx]
        explanation = explanation.replace('：', ':')
        explanation = explanation.split(':')
        explanation = explanation[1]
        explanation = explanation.strip(' ')
        idx += 1
        add_success += 1
        test_question.append({
            'question': question,
            'options': options,
            'correct_answer': answer,
            'explanation': explanation
        })
    file.close()
    edit_question_file_add(test_question, 'question.json')
    print(f"✅ Successfully added {add_success} questions\n❌Failed to add {add_fail} questions")
    return True
