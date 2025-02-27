import random
import re  # ? fixme


class Card:
    # fixme можно добавить атрибут класса
    # values = {str(i): i for i in range(2, 11)} | {"J": 10, "Q": 10, "K": 10, "A": 11}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    @property
    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11  # Значение туза может измениться позднее
        else:
            return int(self.rank)
        # fixme тогда тут будет просто
        # return Card.values[self.rank]

    def __str__(self):
        return f"{self.rank} {self.suit}"


# Класс "Колода" для генерации и перемешивания карт
class Deck:
    def __init__(self):
        suits = ["Черви", "Бубны", "Крести", "Пики"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        # fixme а тут
        # ranks = list(Card.values.keys())
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None


# Класс "Игрок" для управления картами игрока и вычисления его очков
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    @property
    def score(self):
        # fixme тут можно использовать генератор, но так тоже ок
        # total = sum(card.value for card in self.hand)
        # aces = sum(1 for card in self.hand if card.rank == 'A')
        total = 0
        aces = 0
        for card in self.hand:
            total += card.value
            if card.rank == "A":
                aces += 1
        # Обработка значений туза как 1 или 11
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def __str__(self):
        return (
            f"Карты {self.name}: "
            + ", ".join(str(card) for card in self.hand)
            + f" (Очки: {self.score})"
        )


# Основной игровой процесс
# fixme его тоже можно слегка еще разделить
def play_blackjack():
    # Создаём колоду и двух игроков (пользователь и дилер)
    deck = Deck()
    player = Player("Игрок")
    dealer = Player("Дилер")

    # Раздаём по две карты каждому игроку
    for _ in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())

    # Выводим начальные карты игрока
    print(player)
    print("Карты дилера: ", dealer.hand[0], ", ?")

    # Ход игрока: брать карту или остановиться
    while player.score < 21:
        action = input("Хотите взять карту или остановиться? (в/о): ").lower()
        if action == "в":
            player.add_card(deck.deal_card())
            print(player)
            if player.score > 21:
                print("Вы проиграли, перебор! Дилер победил.")
                return
        elif action == "о":
            break
        else:
            print(
                "Некорректный ввод. Введите 'в' для взятия карты или 'о' для остановки."
            )

    # Ход дилера (дилер добирает карты, пока у него меньше 17)
    while dealer.score < 17:
        dealer.add_card(deck.deal_card())

    print(dealer)

    # Определение победителя
    if dealer.score > 21 or player.score > dealer.score:
        print("Поздравляем, вы победили!")
    elif player.score < dealer.score:
        print("Дилер победил.")
    else:
        print("Ничья.")


# fixme добавили точку входа
if __name__ == "__main__":
    # Запуск игры
    play_blackjack()
