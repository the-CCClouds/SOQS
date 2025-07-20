import time
import json


def load_file_number():  #加载问题数量的函数
    file_num = len(load_question_file('question.txt'))
    return file_num


def check_question_part(question_check):
    try:
        question_check = question_check.split('.')
    except Exception as e:
        print(f'❌文件格式不对{e}')
        return False
    question_check_num = int(question_check[0])
    if question_check_num < 1:
        print('❌文档问题中的数字不对')
        return False
    return True


def check_options_part(options):
    for option in options:
        try:
            option = option.split('.')
        except Exception as e:
            print(f'❌文件格式不对{e}')
            return False
        if option[0] not in ['A', 'B', 'C', 'D']:
            print(option[0])
            print(f'❌你的格式不对')
            return False
    return True


def check_answer_part(answer):
    try:
        answer = answer.replace('：', ':')
        answer_check = answer.split(':')
        print(answer_check)
    except Exception as e:
        print(f'❌文件格式不对{e}')
        return False
    if answer_check[0] not in ['correct_answer', '答案']:
        print(answer_check[0])
        print(f'❌你的格式不对')
        return False
    return True


def load_file_first():  #首次加载问题
    try:
        file_name = input('please input file name:')
        file = open(f'D:/desktop/python/assignment/question file/{file_name}', 'r', encoding='utf-8')
    except Exception as e:
        print('❌你输入了一个错误的文件名或者文件名位置不对')
        print(e)
        return False  #尝试输入和对错误的纠正
    lines = []
    test_question = []
    idx = 0  #指针位置
    for line in file:
        line = line.strip('\n')
        lines.append(line)  #处理原文档中的空格和空行
    while idx < len(lines):
        #question的处理
        question = lines[idx]
        if not check_question_part(question):
            return False
        idx += 1
        #options的处理
        options = lines[idx:idx + 4]
        if not check_options_part(options):
            return False
        idx += 4
        #answer的处理
        answer = lines[idx]
        if not check_answer_part(answer):
            return False
        idx += 1
        test_question.append({
            'question': question,
            'options': options,
            'answer': answer
        })
    edit_question_file(test_question)
    file.close()
    print("✅ 成功添加进入")
    return test_question


def load_file_add():  #添加问题(文件形式)
    try:
        file_name = input('please input file name:')
        file = open(f'D:/desktop/python/assignment/question file/{file_name}', 'r+', encoding='utf-8')
        file.flush()
    except Exception as e:
        print('你输入了一个错误的文件名或者文件名位置不对')
        print(e)
        return False  #尝试输入和对错误的纠正
    f_num = load_file_number()
    lines = []
    test_question = []
    idx = 0  #指针位置
    for line in file:
        line = line.strip('\n')
        lines.append(line)  #处理原文档中的空格和空行
    while idx < len(lines):
        #question的处理
        parts = lines[idx].split('.', 1)
        repeat = False
        questions = load_question_file('question.txt')
        for q in questions:
            question_split = q['question'].split('.', 1)
            if parts[1].lower() == question_split[1].lower():
                repeat = True
                break
        if repeat:
            print('❌问题在文件中已经存在')
            idx += 6
            continue
        parts[0] = str(f_num + 1)
        question = '.'.join(parts)
        if not check_question_part(question):
            return False
        idx += 1
        f_num += 1
        #options的处理
        options = lines[idx:idx + 4]
        if not check_options_part(options):
            return False
        idx += 4
        #answer的处理
        answer = lines[idx]
        if not check_answer_part(answer):
            return False
        idx += 1
        test_question.append({
            'question': question,
            'options': options,
            'answer': answer
        })
        return True
    file.close()
    edit_question_file_add(test_question)
    print("✅ 成功添加进入")
    return test_question


def file_clear():  #清除文件内容
    try:
        file_name = input('please input file name:')
        file = open(f'D:/desktop/python/assignment/question file/{file_name}', 'w', encoding='utf-8')
        pass
        file.close()
    except Exception as e:
        print('❌你输入了错误的文件名或者文件位置错误')
        print(e)
    print("✅ 成功清空文件")


def load_question_file(file_name):  #加载文件变量名是文件名字
    try:
        with open(f'D:/desktop/python/assignment/question file/{file_name}', 'r', encoding='utf-8') as f:
            print("✅ 成功打开文件")
            return json.load(f)
    except Exception as e:
        print('❌题库文件不存在或者格式不对', e)
        return None


def edit_question_file(question):  #将旧内容进行覆盖
    """

    :param question:你新添加的问题变量名称
    :return: None
    """
    try:  # 先确保题库文件存在且是合法 JSON
        f = open('D:/desktop/python/assignment/question file/question.txt', 'w', encoding='utf-8')
    except Exception as e:
        print(f'❌找不到文件{e}')
        return False
    json.dump(question, f, ensure_ascii=False, indent=2)
    print("✅ 成功覆盖文件")
    return True


def edit_question_file_add(new_question):  #将新内容添加到就内容并进行合并覆盖
    """

    :param new_question:你新添加的问题变量名称
    :return: None
    """
    path = 'D:/desktop/python/assignment/question file/question.txt'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            old = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        old = []  # 文件为空或损坏时兜底

    old.extend(new_question)  # 内存里合并

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(old, f, ensure_ascii=False, indent=2)  # 一次性覆盖
    print("✅ 成功覆盖文件")
    return


def search_file(keyword):  #搜索基础
    questions = load_question_file('question.txt')
    result = []
    try:
        for q in questions:
            if keyword.lower() in q['question'].lower():
                result.append(q)
    except Exception as e:
        print(f'❌问题文件内没有内容{e}')
    return result


def search_file_main():  #搜索主题
    keyword = input('please input keyword:')
    questions = search_file(keyword)
    search_result = []
    if questions:
        print(f'✅成功搜索到{len(questions)}道题,分别为:')
        for q in questions:
            print(q['question'])
            for opt in q['options']:
                print(opt)
            print(q['answer'])
            time.sleep(0.5)
            search_result.append({
                'question': q['question'],
                'options': q['options'],
                'answer': q['answer']
            })
        return search_result
    else:
        print('❌对不起哦在题库中没有发现这道题')
        return None


def enter_add_question():  #添加新问题(输入添加)
    questions = load_question_file('question.txt')
    q = input('please input question:')
    q = f'{str(load_file_number())}.{q}'
    repeat = False
    for q in questions:
        question_split = q['question'].split('.', 1)
        if q.lower() == question_split[1].lower():
            repeat = True
            break
    if repeat:
        print('❌你输入了一个重复的问题请重试')
        return False
    i = 1
    options = []
    while i <= 4:
        for letter in ['A', 'B', 'C', 'D']:
            opt = input(f'please input {letter}\toption:')
            opt = f'{opt}\n'
            options.append(opt.lower())
            i += 1
    answer = input('please input answer:').upper()
    if answer not in ['A', 'B', 'C', 'D']:
        print('you entered wrong answer')
        return False
    new_add = [
        {
            'question': q,
            'options': options,
            'answer': answer
        }
    ]
    edit_question_file_add(new_add)
    print("✅ 成功添加新问题")
    return True


def ask_replace_question():  #询问更换哪道题目(手写)
    select_question = search_file_main()
    try:
        select_question_num = int(input(
            f'please input which question number you want to replace:\nif you want to replace the first question,enter 1 others is same'))
    except Exception as e:
        print(f'you enter a wrong number{e}')
    replace_question = select_question[select_question_num - 1]
    r_q_s = replace_question['question']
    r_q_s = r_q_s.split('.', maxsplit=1)
    q_num = r_q_s[0]
    print(f'你选择的题目题号是{q_num}')
    return q_num


def replace_question(q_num):
    question_new = input('please input new question:')
    old_question = load_question_file('question.txt')
    q_num = int(q_num)
    old_question[q_num - 1]['question'] = f"{q_num}.{question_new}"
    edit_question_file(old_question)
    print("✅ question replaced successfully")


def replace_options(q_num):
    options = []
    i = 1
    while i <= 4:
        for letter in ['A', 'B', 'C', 'D']:
            opt = input(f'please input {letter}\toption:')
            opt = f'{letter}.{opt}'
            options.append(opt)
            i += 1
    q_num = int(q_num)
    old_question = load_question_file('question.txt')
    old_question[q_num - 1]['options'] = options
    edit_question_file(old_question)
    print("✅ question replaced successfully")


def replace_answer(q_num):
    answer = input('please input answer:').upper()
    if answer not in ['A', 'B', 'C', 'D']:
        print('you entered wrong answer')
        return False
    q_num = int(q_num)
    old_question = load_question_file('question.txt')
    old_question[q_num - 1]['answer'] = answer
    edit_question_file(old_question)
    print("✅ question replaced successfully")
    return True


def replace_all(q_num):
    question_new = input('please input new question:')
    options = []
    i = 1
    while i <= 4:
        for letter in ['A', 'B', 'C', 'D']:
            opt = input(f'please input {letter}\toption:')
            opt = f'{letter}.{opt}'
            options.append(opt)
            i += 1
    answer = input('please input answer:').upper()
    if answer not in ['A', 'B', 'C', 'D']:
        print('you entered wrong answer')
        return False
    q_num = int(q_num)
    old_question = load_question_file('question.txt')
    old_question[q_num - 1]['question'] = f"{q_num}.{question_new}"
    old_question[q_num - 1]['options'] = options
    old_question[q_num - 1]['answer'] = f"答案：{answer}"
    edit_question_file(old_question)
    print("✅ question replaced successfully")
    return True


def delete_question():
    question = load_question_file('question.txt')
    for idx in range(len(question)):
        question_select = question[idx]
        print(question_select['question'])
        time.sleep(0.5)
        idx += 5
    select_num = int(input('which question you want to delete:'))
    s = ''.join(str(i) for i in range(1, len(question) + 1))
    if str(select_num) not in s:
        print('❌you entered wrong answer')
        return False
    question.pop(select_num - 1)
    edit_question_file(question)
    return True


def replace_main():
    q_num = ask_replace_question()
    print('which part you want to replace:')
    print('if you want to change question,please enter 1')
    print('if you want to change options,please enter 2')
    print('if you want to change answer,please enter 3')
    print('if you want to change all,please enter 4')
    change_answer = int(input('please input answer:'))
    if change_answer not in [1, 2, 3, 4]:
        print('you entered wrong answer')
        return False
    if change_answer == 1:
        replace_question(q_num)
        print("✅ question replaced successfully")
    if change_answer == 2:
        replace_options(q_num)
        print("✅ question replaced successfully")
    if change_answer == 3:
        replace_answer(q_num)
        print("✅ question replaced successfully")
    if change_answer == 4:
        replace_all(q_num)
        print("✅ question replaced successfully")
    return True


if __name__ == '__main__':
    file_clear()
    load_file_first()
    load_file_add()
