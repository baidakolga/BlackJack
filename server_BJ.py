import random
import socket
sock = socket.socket()
sock.bind(('', 9000))
sock.listen(1)
conn, addr = sock.accept()


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
    def __init__(self):
        self.player_score = 0
        self.dealer_score = 0
        self.hand_of_player = []
        self.hand_of_dealer = []

    all_decks = []
    list_of_decks = []
    for i in deck_of_cards.keys():
        list_of_decks.append(i)
    one_deck = list_of_decks * 4

    def number_of_decks(self):
        conn.send('Введи количество колод. Максимальное количество колод - 8 '.encode('utf-8'))
        number = conn.recv(1024)
        if 1 <= int(number) <= 8:
            self.all_decks = self.one_deck * int(number)
            random.shuffle(self.all_decks)
            # print(self.all_decks)
            # print(len(self.all_decks))
        else:
            conn.send('Введено неверное количество колод. Попробуй еще!'.encode('utf-8'))

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
        conn.send(f'\nУ дилера {self.hand_of_dealer[0]} *\nУ игрока {self.hand_of_player[0]} {self.hand_of_player[1]}'.encode('utf-8'))

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
            conn.send(f'\nу дилера сумма очков {self.dealer_score}. На руках карты: '.encode('utf-8'))
        elif self.dealer_score == 21:
            conn.send(f'\nУ дилера сумма очков {self.dealer_score}. BlackJack. На руках карты: '.encode('utf-8'))
        else:
            conn.send(f'\nУ дилера сумма очков {self.dealer_score}. На руках карты: '.encode('utf-8'))
        conn.send(' '.join(self.hand_of_dealer).encode('utf-8'))

    def player_strategy(self):
        conn.send('\nЧтобы взять карту введи "hit"'.encode('utf-8'))
        act = conn.recv(1024).decode('utf-8')
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
            conn.send(f'\nУ игрока сумма очков {self.player_score}. BlackJack. На руках карты: '.encode('utf-8'))
        else:
            conn.send(f'\nУ игрока сумма очков {self.player_score}. На руках карты: '.encode('utf-8'))
        conn.send(' '.join(self.hand_of_player).encode('utf-8'))

    def result(self):
        if self.player_score > 21:
            conn.send('\nИгрок проиграл.'.encode('utf-8'))
        elif self.player_score == self.dealer_score:
            conn.send('\nНичья.'.encode('utf-8'))
        elif self.player_score == 21:
            conn.send('\nBlackJack! Игрок выиграл'.encode('utf-8'))
        elif self.player_score > self.dealer_score:
            conn.send('\nИгрок выиграл'.encode('utf-8'))
        elif self.player_score < self.dealer_score and self.dealer_score > 21:
            conn.send('\nИгрок выиграл'.encode('utf-8'))
        else:
            conn.send('\nИгрок проиграл.'.encode('utf-8'))

    def play(self):
        self.number_of_decks()
        self.distribution_of_cards()
        self.player_strategy()
        self.dealer_strategy()
        self.result()
        conn.close()


game1 = BlackJackGame()
game1.play()




