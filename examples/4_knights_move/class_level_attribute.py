class Game:
    board: list[list[int | None]] = [[None for _ in range(10)] for _ in range(10)]

    def __init__(self):
        self.current_number = 1


game1 = Game()
game2 = Game()

game1.board[0][0] = "X"
print(game2.board[0][0])
