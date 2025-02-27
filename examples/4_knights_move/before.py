from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import random

class Game(BoxLayout):
    # fixme почему на уровне класса, а не объекта?
    board = ObjectProperty(None)  # Игровое поле
    current_number = 1  # Текущее число, которое будет помещено на поле
    player_wins = 0  # Количество побед игрока
    computer_wins = 0  # Количество побед компьютера
    knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]  # Возможные ходы коня в шахматах

    def __init__(self, **kwargs):  # Конструктор класса Game
        super(Game, self).__init__(**kwargs)  # Вызов конструктора родительского класса
        self.board = [[None for _ in range(10)] for _ in range(10)]  # Инициализация игрового поля размером 10x10
        self.create_board()  # Создание игрового поля
        self.current_position = (0, 0)  # Начальная позиция коня
        self.board[0][0] = self.current_number  # Помещение первого числа в левую верхнюю клетку
        self.current_number += 1  # Увеличение текущего числа
        self.update_board()  # Обновление игрового поля

    def create_board(self):  # Создание игрового поля
        self.orientation = 'vertical'  # Установка ориентации контейнера
        self.score_label = Label(text=f'Ваши победы: {self.player_wins}    Победы компьютера: {self.computer_wins}', size_hint_y=None, height=40)  # Создание метки для отображения счета
        self.add_widget(self.score_label)  # Добавление метки в контейнер
        self.grid = GridLayout(cols=10)  # Создание сетки с 10 колонками
        for i in range(10):  # Помещение в сетку кнопок
            for j in range(10):
                button = Button(text='', font_size=20)  # Создание кнопки
                button.bind(on_press=lambda btn, pos=(i, j): self.on_button_press(btn, pos))  # Привязка обработчика нажатия кнопки
                self.grid.add_widget(button)  # Добавление кнопки в сетку
        self.add_widget(self.grid)  # Добавление сетки в контейнер

    def on_button_press(self, button, pos):  # Метод для обработки нажатия кнопки
        if self.current_number > 100:  # Проверка, не превышено ли максимальное число
            self.show_winner_popup('Компьютер')  # Показ всплывающего окна с победителем
            return
        if self.is_valid_move(pos):  # Проверка, является ли ход допустимым
            self.board[pos[0]][pos[1]] = self.current_number  # Помещение числа на поле
            self.current_number += 1  # Увеличение текущего числа
            self.current_position = pos  # Обновление текущей позиции
            self.update_board()  # Обновление игрового поля
            if not self.has_valid_moves():  # Проверка, есть ли допустимые ходы
                self.show_winner_popup("Вы")  # Показ всплывающего окна с победителем
            else:
                self.computer_move()  # Ход компьютера

    def is_valid_move(self, pos):  # Проверка допустимости хода
        x, y = pos
        if x < 0 or x >= 10 or y < 0 or y >= 10:  # Проверка, находится ли позиция в пределах поля
            return False
        if self.board[x][y] is not None:  # Проверка, свободна ли клетка
            return False
        for move in self.knight_moves:  # Проверка, является ли ход допустимым для коня
            new_x, new_y = self.current_position[0] + move[0], self.current_position[1] + move[1]
            if (new_x, new_y) == (x, y):
                return True
        return False

    def has_valid_moves(self):  # Проверка наличия допустимых ходов
        for move in self.knight_moves:  # Проверка всех возможных ходов коня
            new_x, new_y = self.current_position[0] + move[0], self.current_position[1] + move[1]
            if 0 <= new_x < 10 and 0 <= new_y < 10 and self.board[new_x][new_y] is None:  # Проверка, свободна ли клетка
                return True
        return False

    def computer_move(self):  # Ход компьютера
        valid_moves = [] # Возможные ходы
        for move in self.knight_moves:  # Проверка всех возможных ходов коня
            new_x, new_y = self.current_position[0] + move[0], self.current_position[1] + move[1]
            if 0 <= new_x < 10 and 0 <= new_y < 10 and self.board[new_x][new_y] is None:  # Проверка, свободна ли клетка и не принадлежат ли координаты доске
                valid_moves.append((new_x, new_y)) # Если проверенный ход доступен, то добавляем его в список
        if valid_moves:  # Если есть допустимые ходы
            move = random.choice(valid_moves)  # Выбор случайного хода
            self.board[move[0]][move[1]] = self.current_number  # Помещение числа на поле
            self.current_number += 1  # Увеличение текущего числа
            self.current_position = move  # Обновление текущей позиции
            self.update_board(highlight_move=move)  # Обновление игрового поля с подсветкой хода
            if not self.has_valid_moves():  # Проверка, есть ли допустимые ходы
                self.show_winner_popup('Компьютер')  # Показ всплывающего окна с победителем

    def update_board(self, highlight_move=None):  # Обновление игрового поля
        for i in range(10):  # Проходим по всем кнопкам сетки
            for j in range(10):
                button = self.grid.children[-1 - (i * 10 + j)]  # Получение кнопки из сетки
                button.text = str(self.board[i][j]) if self.board[i][j] is not None else ''  # Обновление текста кнопки
                button.background_color = (0.5, 0.5, 0.5, 1)  # Сброс цвета фона
        if highlight_move:  # Подсветка последнего хода зеленым цветом
            button = self.grid.children[-1 - (highlight_move[0] * 10 + highlight_move[1])] # Получение кнопки, которую надо подсветить зеленым
            button.background_color = (0, 1, 0, 1)  # Зеленый цвет
        for move in self.knight_moves:  # Подсветка всех возможных ходов для игрока белым цветом
            new_x, new_y = self.current_position[0] + move[0], self.current_position[1] + move[1]
            if 0 <= new_x < 10 and 0 <= new_y < 10 and self.board[new_x][new_y] is None:
                button = self.grid.children[-1 - (new_x * 10 + new_y)]
                button.background_color = (1, 1, 1, 1)

    def show_winner_popup(self, winner):  # Показ всплывающего окна с победителем
        if winner == "Вы":  # Увеличение счета игрока или компьютера
            self.player_wins += 1
            text = 'Вы победили!'
            background_color = (0, 1, 0, 1)  # Красный цвет
        else:
            self.computer_wins += 1
            text = 'Вы проиграли!'
            background_color = (1, 0, 0, 1)  # Зеленый цвет

        self.score_label.text = f'Ваши победы: {self.player_wins}    Победы компьютера: {self.computer_wins}'  # Обновление текста метки счета
        content = BoxLayout(orientation='vertical')  # Создание контейнера для всплывающего окна
        content.add_widget(Label(text=text))  # Добавление метки с победителем

        restart_button = Button(text='Продолжить', size_hint_y=None, height=40)  # Создание кнопки для перезапуска игры
        restart_button.bind(on_press=self.restart_game)  # Привязка обработчика нажатия кнопки
        content.add_widget(restart_button)  # Добавление кнопки в контейнер

        popup = Popup(title='Конец игры', content=content, size_hint=(None, None), size=(400, 200), background_color=background_color)  # Создание всплывающего окна
        popup.open()  # Открытие всплывающего окна

    def restart_game(self, instance):  # Метод для перезапуска игры
        self.board = [[None for _ in range(10)] for _ in range(10)]  # Инициализация игрового поля
        self.current_number = 1  # Сброс текущего числа
        self.current_position = (0, 0)  # Сброс текущей позиции
        self.board[0][0] = self.current_number  # Помещение первого числа в левую верхнюю клетку
        self.current_number += 1  # Увеличение текущего числа
        self.update_board()  # Обновление игрового поля
        self.parent.remove_widget(self.parent.children[0])  # Закрыть всплывающее окно

class GameApp(App):  # Определение класса GameApp, наследующегося от App
    def build(self):  # Метод для создания интерфейса приложения
        GameApp.title = 'Ход конём'  # Установка заголовка окна
        return Game()  # Возврат экземпляра класса Game

if __name__ == '__main__':  # Проверка, запущен ли скрипт напрямую
    GameApp().run()  # Запуск приложения
