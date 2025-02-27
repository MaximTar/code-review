import random
import tkinter as tk
from tkinter import messagebox

def gen_question(): # создание вопросов
    # fixme можем использовать list comprehension
    questions = []
    for _ in range(5):
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        # fixme зачем тут строка?
        questions.append(f'{num1} * {num2}')

    return questions

def check_answers(): # проверка ответов
    corr_count = 0 # кол-во правильных ответов
    # fixme зачем тут enumerate?
    # fixme глобальная переменная questions
    for i, (question, answer) in enumerate(zip(questions, answers_entries)):
        # fixme этого можно было избежать
        question = question.split()
        num1, num2 = int(question[0]), int(question[2])
        corr_answer = num1 * num2 # правильный ответ
        user_answer = answer.get() # ответ пользователя

        # fixme NIT можем обойтись без try-except
        try:
            user_answer = int(user_answer)
        except ValueError:
            result_labels[i].config(text='Неправильно!', fg='red')
            continue

        if user_answer == corr_answer:
            result_labels[i].config(text='Правильно!', fg='green')
            corr_count += 1
        else:
            result_labels[i].config(text='Неправильно!', fg='red')

    messagebox.showinfo('Результаты', f'{corr_count} правильных ответов из 5')

window = tk.Tk() # создаем окно приложения
window.title('Тест по таблице умножения')

questions = gen_question() # создаем вопросы
answers_entries = [] # ответы пользователя
result_labels = [] # результаты

for i, question in enumerate(questions):
    # fixme этого можно было избежать
    question = question.split()
    num1, num2 = int(question[0]), int(question[2])
    question_label = tk.Label(window, text = f'{num1} * {num2} = ')
    question_label.grid(row=i, column=0, padx=20, pady=5) # расположение

    answers_entry = tk.Entry(window, width=10) # окно ввода
    answers_entry.grid(row=i, column=1, padx=5, pady=5) # расположение
    answers_entries.append(answers_entry) # добавляем ответы пользователя в список

    result_label = tk.Label(window, text='')
    result_label.grid(row=i, column=2, padx=5, pady=5)
    result_labels.append(result_label)

button = tk.Button(window, text='Проверка', command=check_answers) # кнопка проверки
button.grid(row=6, column=0, columnspan=3, pady=10)

window.mainloop() # запускаем окно программы
