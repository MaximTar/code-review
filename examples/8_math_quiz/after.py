import random
import tkinter as tk
from tkinter import messagebox


class MathQuiz:
    def __init__(self, master, num_questions=5):
        self.master = master
        self.master.title("Тест по таблице умножения")
        self.num_questions = num_questions

        self.questions = self.generate_questions()
        self.answers_entries = []
        self.result_labels = []

        self.create_widgets()

    def generate_questions(self):
        return [
            (random.randint(1, 9), random.randint(1, 9))
            for _ in range(self.num_questions)
        ]
        # fixme NIT если же мы всё же хотим избежать дубликатов - используем set
        # questions = set()
        # while len(questions) < self.num_questions:
        #     question = (random.randint(1, 9), random.randint(1, 9))
        #     questions.add(question)
        # return list(questions)

    def check_answers(self):
        correct_count = 0

        for (num1, num2), answer, result_label in zip(
            self.questions, self.answers_entries, self.result_labels
        ):
            correct_answer = num1 * num2
            user_answer = answer.get().strip()

            if not user_answer.isdigit():
                result_label.config(text="Неправильно!", fg="red")
                continue

            if int(user_answer) == correct_answer:
                result_label.config(text="Правильно!", fg="green")
                correct_count += 1
            else:
                result_label.config(text="Неправильно!", fg="red")

        messagebox.showinfo(
            "Результаты", f"{correct_count} правильных ответов из {self.num_questions}"
        )

    def create_widgets(self):
        for i, (num1, num2) in enumerate(self.questions):
            question_label = tk.Label(self.master, text=f"{num1} * {num2} = ")
            question_label.grid(row=i, column=0, padx=20, pady=5)

            entry = tk.Entry(self.master, width=10)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.answers_entries.append(entry)

            result_label = tk.Label(self.master, text="")
            result_label.grid(row=i, column=2, padx=5, pady=5)
            self.result_labels.append(result_label)

        check_button = tk.Button(
            self.master, text="Проверка", command=self.check_answers
        )
        check_button.grid(row=self.num_questions, column=0, columnspan=3, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    quiz = MathQuiz(root, num_questions=5)
    root.mainloop()
