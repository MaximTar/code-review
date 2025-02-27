# длинный процедурный код вместо разделения на функции
# захардкоженная обработка в меню [нарушение принципа разделения ответственности SOC - Separation of concerns]
# родитель напрямую изменяет состояние потомка [нарушение инкапсуляции]


def get_number(K):
    while True:
        try:
            return int(input(f"{K}"))
        except ValueError:
            print("Некорректный ввод. Введите число.")

class Parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def info(self):
        return f"Родитель: {self.name}, Возраст: {self.age}, Количество детей: {len(self.children)}"

    def calm_child(self, child_index):
        if 0 <= child_index < len(self.children):
            child = self.children[child_index]
            # fixme грубое нарушение принципа инкапсуляции
            child.is_calm = True
            return f"Ребёнок {child.name} успокоен."
        return "Некорректный номер ребёнка."

    def feed_child(self, child_index):
        if 0 <= child_index < len(self.children):
            child = self.children[child_index]
            child.is_hungry = False
            return f"Ребёнок {child.name} накормлен."
        return "Некорректный номер ребёнка."

class Child:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.is_calm = False  # состояние спокойствия
        self.is_hungry = True  # состояние голода

    def info(self):
        calm_state = "спокойный" if self.is_calm else "неспокойный"
        hunger_state = "голодный" if self.is_hungry else "сытый"
        return f"Ребёнок: {self.name}, Возраст: {self.age}, Состояние: {calm_state}, {hunger_state}"

# Ввод данных о родителях и детях
parents = []
N = get_number("Введите количество родителей: ")

for i in range(N):
    parent_name = input(f"Введите имя {i + 1}-го родителя: ")
    parent_age = get_number(f"Введите возраст {i + 1}-го родителя: ")
    parent = Parent(parent_name, parent_age)

    num_children = get_number(f"Введите количество детей у {parent_name}: ")
    for j in range(num_children):
        child_name = input(f"  Имя {j + 1}-го ребёнка: ")
        while True:
            child_age = get_number(f"  Возраст {j + 1}-го ребёнка: ")
            if child_age >= parent_age:
                print("Ошибка: возраст ребёнка не может быть больше или равен возрасту родителя. Попробуйте снова.")
            else:
                break
        parent.add_child(Child(child_name, child_age))

    parents.append(parent)

# Меню взаимодействия
while True:
    print("\nМеню:")
    print("1) Сообщить информацию о родителе с номером k")
    print("2) Сообщить информацию о всех детях для заданного родителя k")
    print("3) Выполнить действие с ребенком (успокоить или накормить)")
    print("4) Выход")
    choice = get_number("Ваш выбор: ")

    if choice == 1:
        k = get_number("Введите номер родителя: ") - 1
        if 0 <= k < len(parents):
            print(parents[k].info())
        else:
            print("Некорректный номер родителя.")

    elif choice == 2:
        k = get_number("Введите номер родителя: ") - 1
        if 0 <= k < len(parents):
            for idx, child in enumerate(parents[k].children):
                print(f"{idx + 1}. {child.info()}")
        else:
            print("Некорректный номер родителя.")

    elif choice == 3:
        k = get_number("Введите номер родителя: ") - 1
        if 0 <= k < len(parents):
            child_index = get_number("Введите номер ребёнка: ") - 1
            action = input("Введите действие (успокоить/накормить): ").lower()
            if action == "успокоить":
                print(parents[k].calm_child(child_index))
            elif action == "накормить":
                print(parents[k].feed_child(child_index))
            else:
                print("Некорректное действие.")
        else:
            print("Некорректный номер родителя.")

    elif choice == 4:
        print("Выход из программы.")
        break

    else:
        print("Некорректный выбор. Попробуйте снова.")
