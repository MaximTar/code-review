import random
from enum import Enum

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

BOARD_SIZE = 4  # теперь легко можно менять размер доски


# замена использованию строк в качестве идентификаторов
class Winner(Enum):
    PLAYER = "player"
    COMPUTER = "computer"


class Color(Enum):
    GRAY = (0.5, 0.5, 0.5, 1)
    GREEN = (0, 1, 0, 1)
    WHITE = (1, 1, 1, 1)
    RED = (1, 0, 0, 1)


# если не хочется обращаться через .value, можно сделать как-то вроде
# def get_color_value(color: Color):
#     return color.value
# background_color = get_color_value(Color.GRAY)


class Game(BoxLayout):
    knight_moves: list[tuple[int, int]] = [
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.board: list[list[int | None]] = [
            [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        self.current_position: tuple[int, int] = (0, 0)
        self.current_number: int = 1
        self.player_wins: int = 0
        self.computer_wins: int = 0

        self.create_board()
        self.update_board((0, 0))

    def create_board(self) -> None:
        self.orientation = "vertical"

        self.score_label = Label(
            text=f"Ваши победы: {self.player_wins}    Победы компьютера: {self.computer_wins}",
            size_hint_y=None,
            height=40,
        )
        self.add_widget(self.score_label)

        self.grid = GridLayout(cols=BOARD_SIZE)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                button = Button(text="", font_size=20)
                button.bind(on_press=lambda btn, pos=(i, j): self.on_button_press(pos))
                self.grid.add_widget(button)

        self.add_widget(self.grid)

    def on_button_press(self, pos: tuple[int, int]) -> None:
        if self.current_number > BOARD_SIZE * BOARD_SIZE:
            self.show_winner_popup(Winner.COMPUTER)
            return

        if self.is_valid_move(pos):
            self.update_board(pos)

            if not self.has_valid_moves():
                self.show_winner_popup(Winner.PLAYER)
            else:
                self.computer_move()

    # избавляемся от дупликации
    @staticmethod
    def is_within_bounds(x: int, y: int) -> bool:
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    # ещё
    def is_cell_free(self, x: int, y: int) -> bool:
        return self.board[x][y] is None

    # и ещё
    def is_valid_position(self, x: int, y: int) -> bool:
        return self.is_within_bounds(x, y) and self.is_cell_free(x, y)

    # и ещё чуть-чуть
    def get_new_position(self, move: tuple[int, int]) -> tuple[int, int]:
        return self.current_position[0] + move[0], self.current_position[1] + move[1]

    # и наконец
    def get_valid_moves(self) -> list[tuple[int, int]]:
        return [
            self.get_new_position(move)
            for move in self.knight_moves
            if self.is_valid_position(*self.get_new_position(move))
        ]

    def is_valid_move(self, pos: tuple[int, int]) -> bool:
        x, y = pos

        if not self.is_valid_position(x, y):
            return False

        return any(self.get_new_position(move) == (x, y) for move in self.knight_moves)

    def has_valid_moves(self):
        return len(self.get_valid_moves()) > 0

    def computer_move(self) -> None:
        valid_moves = self.get_valid_moves()

        if valid_moves:
            move = random.choice(valid_moves)
            self.update_board(move, highlight=True)

            if not self.has_valid_moves():
                self.show_winner_popup(Winner.COMPUTER)

    def update_board(self, position: tuple[int, int], highlight: bool = False) -> None:

        self.board[position[0]][position[1]] = self.current_number
        self.current_position = position
        self.current_number += 1

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                button = self.grid.children[-1 - (i * BOARD_SIZE + j)]
                button.text = (
                    str(self.board[i][j]) if not self.is_cell_free(i, j) else ""
                )
                button.background_color = Color.GRAY.value

        if highlight:
            button = self.grid.children[
                -1 - (position[0] * BOARD_SIZE + position[1])
            ]
            button.background_color = Color.GREEN.value

        for move in self.knight_moves:
            new_x, new_y = self.get_new_position(move)
            if self.is_valid_position(new_x, new_y):
                button = self.grid.children[-1 - (new_x * BOARD_SIZE + new_y)]
                button.background_color = Color.WHITE.value

    def show_winner_popup(self, winner: Winner) -> None:
        if winner == Winner.PLAYER:
            self.player_wins += 1
            text, background_color = "Вы победили!", Color.GREEN.value
        else:
            self.computer_wins += 1
            text, background_color = "Вы проиграли!", Color.RED.value

        self.score_label.text = f"Ваши победы: {self.player_wins}    Победы компьютера: {self.computer_wins}"
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=text))

        restart_button = Button(text="Продолжить", size_hint_y=None, height=40)
        restart_button.bind(on_press=self.restart_game)
        content.add_widget(restart_button)

        popup = Popup(
            title="Конец игры",
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            background_color=background_color,
            auto_dismiss=False,  # модальное окно
        )
        popup.open()

    def restart_game(self, _) -> None:
        # self.board: list[list[int | None]] = [
        #     [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        # ]
        # чтобы mypy был доволен
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.board[i][j] = None
        self.current_number = 1
        self.update_board((0, 0))
        self.parent.remove_widget(self.parent.children[0])


class GameApp(App):
    def build(self) -> Game:
        GameApp.title = "Ход конём"
        return Game()


if __name__ == "__main__":
    GameApp().run()
