import random

deck_of_cards = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'jack': 10,
    'queen': 10,
    'king': 10,
    'ace': 1,
}


class BlackJackGame:
    all_decks = []
    list_of_decks = []
    for i in deck_of_cards.keys():
        list_of_decks.append(i)
    one_deck = list_of_decks * 4
    dealer_score = 0
    player_score = 0
    hand_of_dealer = []
    hand_of_player = []

    def number_of_decks(self):
        number = input('Введи количество колод. Максимальное количество колод - 8 ')
        if 1 <= int(number) <= 8:
            self.all_decks = self.one_deck * int(number)
            random.shuffle(self.all_decks)
            # print(self.all_decks)
            # print(len(self.all_decks))
        else:
            print('Введено неверное количество колод. Попробуй еще!')

    def distribution_of_cards(self):
        first_card_of_dealer = self.all_decks.pop()
        second_card_of_dealer = self.all_decks.pop()
        self.hand_of_dealer.append(first_card_of_dealer)
        self.hand_of_dealer.append(second_card_of_dealer)
        for item in self.hand_of_dealer:
            self.dealer_score += deck_of_cards[item]
        if self.dealer_score < 12 and 'ace' in self.hand_of_dealer:
            self.dealer_score += 10
        first_card_of_player = self.all_decks.pop()
        second_card_of_player = self.all_decks.pop()
        self.hand_of_player.append(first_card_of_player)
        self.hand_of_player.append(second_card_of_player)
        for item in self.hand_of_player:
            self.player_score += deck_of_cards[item]
        if self.player_score < 12 and 'ace' in self.hand_of_player:
            self.player_score += 10
        print(f'У дилера {self.hand_of_dealer[0]} *\nУ игрока {self.hand_of_player[0]} {self.hand_of_player[1]}')

    def ace_check(self, score, hand):
        if score < 12 and 'ace' in hand:
            score += 10

    def dealer_strategy(self):
        if self.dealer_score < 17:
            while self.dealer_score < 17:
                next_card_of_dealer = self.all_decks.pop()
                self.hand_of_dealer.append(next_card_of_dealer)
                self.dealer_score += deck_of_cards[next_card_of_dealer]
                if next_card_of_dealer == 'ace' and self.dealer_score < 12:
                    self.dealer_score += 10
            print(f'у дилера сумма очков {self.dealer_score}')
        elif self.dealer_score == 21:
            print(f'У дилера сумма очков {self.dealer_score}. BlackJack')
        else:
            print(f'У дилера сумма очков {self.dealer_score}')
        print(self.hand_of_dealer)

    def player_strategy(self):
        act = input('Чтобы взять карту введи "hit" ')
        if act == 'hit':
            next_card_of_player = self.all_decks.pop()
            self.hand_of_player.append(next_card_of_player)
            self.player_score += deck_of_cards[next_card_of_player]
            self.ace_check(self.player_score, self.hand_of_player)
            if self.player_score < 12 and 'ace' in next_card_of_player:
                self.player_score += 10
        else:
            pass
        if self.player_score == 21:
            print(f'У игрока сумма очков {self.player_score}. BlackJack')
        else:
            print(f'У игрока сумма очков {self.player_score}')
        print(self.hand_of_player)

    def result(self):
        if self.player_score > 21:
            print('Игрок проиграл.')
        elif self.player_score == self.dealer_score:
            print('Ничья.')
        elif self.player_score == 21:
            print('BlackJack! Игрок выиграл')
        elif self.player_score > self.dealer_score:
            print('Игрок выиграл')
        elif self.player_score < self.dealer_score and self.dealer_score > 21:
            print('Игрок выиграл')
        else:
            print('Игрок проиграл.')

    def clear_table(self):
        self.dealer_score = 0
        self.player_score = 0
        self.hand_of_dealer.clear()
        self.hand_of_player.clear()

    def play(self):
        self.number_of_decks()
        self.distribution_of_cards()
        self.player_strategy()
        self.dealer_strategy()
        self.result()
        self.clear_table()


game1 = BlackJackGame()
game1.play()
