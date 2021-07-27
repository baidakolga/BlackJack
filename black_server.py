import random
import socket

# GAME PART

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

    def number_of_decks(self, number):
        if 1 <= int(number) <= 8:
            self.all_decks = self.one_deck * int(number)
            random.shuffle(self.all_decks)
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
        message = f'У дилера {self.hand_of_dealer[0]} *\nУ игрока {self.hand_of_player[0]} {self.hand_of_player[1]}'
        return message

    def ace_check(self, score, hand):
        if score < 12 and 'ace' in hand:
            score += 10

    def dealer_strategy(self):
        hand = ''
        score = ''
        if self.dealer_score < 17:
            while self.dealer_score < 17:
                next_card_of_dealer = self.all_decks.pop()
                self.hand_of_dealer.append(next_card_of_dealer)
                self.dealer_score += deck_of_cards[next_card_of_dealer]
                if next_card_of_dealer == 'ace' and self.dealer_score < 12:
                    self.dealer_score += 10
            score = f'у дилера сумма очков {self.dealer_score}'
        elif self.dealer_score == 21:
            score = f'У дилера сумма очков {self.dealer_score}. BlackJack'
        else:
            score = f'У дилера сумма очков {self.dealer_score}'
        hand = ' '.join(self.hand_of_dealer)
        return score, hand

    def player_strategy(self, act):
        hand = ''
        score = ''
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
            score = f'У игрока сумма очков {self.player_score}. BlackJack'
        else:
            score = f'У игрока сумма очков {self.player_score}'
        hand = ' '.join(self.hand_of_player)
        return score, hand

    def result(self):
        WIN = 'Игрок выиграл'
        BALCK_JACK = 'BlackJack! Игрок выиграл'
        LOOSE ='Игрок проиграл.'
        NONE = 'Ничья.'
        if self.player_score > 21:
            message = LOOSE
            return message
        elif self.player_score == self.dealer_score:
            message = NONE
            return message
        elif self.player_score == 21:
            message = BALCK_JACK
            return message
        elif self.player_score > self.dealer_score:
            message = WIN
            return message
        elif self.player_score < self.dealer_score and self.dealer_score > 21:
            message = WIN
            return message
        else:
            message = LOOSE
            return message

    def play(self, num, act):
        self.number_of_decks(num)
        self.distribution_of_cards()
        self.player_strategy(act)
        self.dealer_strategy()
        self.result()


# SERVER PART

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

while True:
    sock.send(b'wanna, play?')
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data.upper())

conn.close()
