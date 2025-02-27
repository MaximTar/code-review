from enum import Enum


# Инкапсуляция: Parent больше не изменяет атрибуты Child напрямую
# Проверка добавления детей старше родителей
# Повторное использование: добавлен базовый класс Person для незначительного улучшения структуры


def get_number(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


class MenuOption(Enum):
    SHOW_PARENT_INFO = 1
    SHOW_CHILDREN_INFO = 2
    INTERACT_WITH_CHILD = 3
    EXIT = 4


TRANSLATIONS = {
    MenuOption.SHOW_PARENT_INFO: "Сообщить информацию о родителе с номером k",
    MenuOption.SHOW_CHILDREN_INFO: "Сообщить информацию о всех детях для заданного родителя k",
    MenuOption.INTERACT_WITH_CHILD: "Выполнить действие с ребенком (успокоить или накормить)",
    MenuOption.EXIT: "Выход",
}

GET_PARENT_NUMBER_TEXT = "Введите номер родителя: "
ERROR_PARENT_NUMBER_TEXT = "Ошибка: некорректный номер родителя."


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}, Возраст: {self.age}"


class Child(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        self.is_calm = False
        self.is_hungry = True

    def calm(self):
        self.is_calm = True

    def feed(self):
        self.is_hungry = False

    def get_status(self) -> str:
        calm_state = "спокойный" if self.is_calm else "неспокойный"
        hunger_state = "голодный" if self.is_hungry else "сытый"
        return f"Состояние: {calm_state}, {hunger_state}"

    def __str__(self):
        return f"{super().__str__()}, {self.get_status()}"


class Parent(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        self.children = []

    def add_child(self, child: Child):
        self.children.append(child)

    def get_children_info(self) -> str:
        if not self.children:
            return "Нет детей."
        return "\n".join(
            f"{idx + 1}. {child}" for idx, child in enumerate(self.children)
        )

    def interact_with_child(self, child_index: int, action: str) -> str:
        if 0 <= child_index < len(self.children):
            child = self.children[child_index]
            if action == "успокоить":
                child.calm()
                return f"{child.name} успокоен."
            if action == "накормить":
                child.feed()
                return f"{child.name} накормлен."
        return "Ошибка: некорректные данные."

    def __str__(self):
        return f"{super().__str__()}, Количество детей: {len(self.children)}"


def create_parents() -> list[Parent]:
    parents = []
    num_parents = get_number("Введите количество родителей: ")

    for i in range(num_parents):
        parent = Parent(
            input(f"Введите имя {i + 1}-го родителя: "),
            get_number(f"Введите возраст {i + 1}-го родителя: "),
        )

        for j in range(get_number(f"Введите количество детей у {parent.name}: ")):
            child_name = input(f"  Имя {j + 1}-го ребёнка: ")
            while True:
                child_age = get_number(f"  Возраст {j + 1}-го ребёнка: ")
                if child_age >= parent.age:
                    print(
                        "Ошибка: возраст ребёнка не может быть больше или равен возрасту родителя. Попробуйте снова."
                    )
                else:
                    break
            parent.add_child(Child(child_name, child_age))

        parents.append(parent)

    return parents


def show_parent_info(parents: list[Parent]):
    k = get_number(GET_PARENT_NUMBER_TEXT) - 1
    print(parents[k] if 0 <= k < len(parents) else ERROR_PARENT_NUMBER_TEXT)


def show_children_info(parents: list[Parent]):
    k = get_number(GET_PARENT_NUMBER_TEXT) - 1
    print(
        parents[k].get_children_info()
        if 0 <= k < len(parents)
        else ERROR_PARENT_NUMBER_TEXT
    )


def interact_with_child(parents: list[Parent]):
    k = get_number(GET_PARENT_NUMBER_TEXT) - 1
    if 0 <= k < len(parents):
        child_index = get_number("Введите номер ребёнка: ") - 1
        action = input("Введите действие (успокоить/накормить): ").lower()
        print(parents[k].interact_with_child(child_index, action))
    else:
        print(ERROR_PARENT_NUMBER_TEXT)


def exit_program():
    print("Выход из программы.")
    exit()


def main_menu(parents: list[Parent]):
    # можно воспользоваться паттерном
    commands = {
        MenuOption.SHOW_PARENT_INFO: lambda: show_parent_info(parents),
        MenuOption.SHOW_CHILDREN_INFO: lambda: show_children_info(parents),
        MenuOption.INTERACT_WITH_CHILD: lambda: interact_with_child(parents),
        MenuOption.EXIT: exit_program,
    }

    while True:
        print("\nМеню:")
        for option in MenuOption:
            # print(f"{option.value}) {option.name.replace('_', ' ').capitalize()}")
            print(f"{option.value}) {TRANSLATIONS[option]}")

        try:
            choice = MenuOption(get_number("Ваш выбор: "))
            match choice:
                case MenuOption.SHOW_PARENT_INFO:
                    show_parent_info(parents)
                case MenuOption.SHOW_CHILDREN_INFO:
                    show_children_info(parents)
                case MenuOption.INTERACT_WITH_CHILD:
                    interact_with_child(parents)
                case MenuOption.EXIT:
                    print("Выход из программы.")
                    break
            # если использовать паттерн
            # commands[choice]()
        except ValueError:
            print("Ошибка: некорректный выбор.")


if __name__ == "__main__":
    parents_list = create_parents()
    main_menu(parents_list)
