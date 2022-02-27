import random
from time import sleep
class Deck():
    def __init__(self):
        self.cards = {}
        COLORS = ['red', 'green', 'blue', 'yellow', 'black']
        TYPECARDS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'block', 'return', 'plus 2']
        for color in COLORS:
            if(color != 'black'):
                self.cards.update({color: [f'{card}:{color}' for card in TYPECARDS] + [f'{card}:{color}' for card in TYPECARDS]})
        self.cards.update({'black': []})
        for x in range(4):
            self.cards['black'].append('plus 4:black')
            self.cards['black'].append('color:black')

        '''self.cards = {
            'red': ['0:red', '1:red', '2:red', '3:red', '4:red', '5:red', '6:red', '7:red', '8:red', '9:red', 'block:red', 'return:red', 'plus 2:red', '0:red', '1:red', '2:red', '3:red', '4:red', '5:red', '6:red', '7:red', '8:red', '9:red', 'block:red', 'return:red', 'plus 2:red'],
            'green': ['0:green', '1:green', '2:green', '3:green', '4:green', '5:green', '6:green', '7:green', '8:green', '9:green', 'block:green', 'return:green', 'plus 2:green', '0:green', '1:green', '2:green', '3:green', '4:green', '5:green', '6:green', '7:green', '8:green', '9:green', 'block:green', 'return:green', 'plus 2:green'],
            'blue': ['0:blue', '1:blue', '2:blue', '3:blue', '4:blue', '5:blue', '6:blue', '7:blue', '8:blue', '9:blue', 'block:blue', 'return:blue', 'plus 2:blue', '0:blue', '1:blue', '2:blue', '3:blue', '4:blue', '5:blue', '6:blue', '7:blue', '8:blue', '9:blue', 'block:blue', 'return:blue', 'plus 2:blue'],
            'yellow': ['0:yellow', '1:yellow', '2:yellow', '3:yellow', '4:yellow', '5:yellow', '6:yellow', '7:yellow', '8:yellow', '9:yellow', 'block:yellow', 'return:yellow', 'plus 2:yellow', '0:yellow', '1:yellow', '2:yellow', '3:yellow', '4:yellow', '5:yellow', '6:yellow', '7:yellow', '8:yellow', '9:yellow', 'block:yellow', 'return:yellow', 'plus 2:yellow'],
            'black': ['plus 4:black', 'color:black', 'plus 4:black', 'color:black', 'plus 4:black', 'color:black', 'plus 4:black', 'color:black']
        }'''

    #if there is card, return False else return True
    def removeCard(self, card):
        try: self.cards[card.split(':')[1]].remove(card)
        except: return True
        else: return False

    # take the card and remove from "self.cards" and if necessary remove key(color) from "self.cards", return the cards, case not have card, return False
    def getCards(self,lenCards=1):
        cards = []
        totcards = 0
        while totcards < lenCards:
            try:
                color = random.choice(list(self.cards.items()))
            except:
                    print('Sem cartas')
                    return cards if(len(cards) > 0) else False
            else:
                if(len(color[1]) >= 1):
                    card = random.choice(self.cards[color[0]])
                    cards.append(card)
                    if(self.removeCard(card)):
                        print('parou')
                        return cards if(len(cards) > 0) else False
                    totcards += 1
                else:
                    if(color[0] in self.cards.keys()):
                        self.cards.pop(color[0])
                    continue
        return cards

    def show(self, txt, color='36'):
        color = color
        print(f'\033[1;{color}m=' * 45, '\033[m')
        if isinstance(txt, str):
            if isinstance(txt, list) and len(txt) == 1:
                txt = txt[0]
            print(f'\033[1m{txt:^45}\033[m')
        else:
            i = 0
            for x in txt:
                print(f'{x:^45}')
                if i != len(txt) - 1: print('        ', f'-' * 29)
                i += 1
        print(f'\033[1;{color}m=' * 45, '\033[m')

    #colored the card conformed corlor passed
    def colorCard(self, card):
        color = card.split(':')[1]
        if(color == 'red'):
            codeColor = '31'
        elif(color == 'black'):
            codeColor = '30'
        elif (color == 'green'):
            codeColor = '32'
        elif (color == 'yellow'):
            codeColor = '33'
        elif (color == 'blue'):
            codeColor = '34'
        return f'\033[1;{codeColor}m{card}\033[m'

class Player(Deck):
    def __init__(self, id, deck, cards):
        self.id = id
        self.deck = deck
        self.cards = cards
        self.lastToPlay = False
        self.uno = False
        self.victory = 0

    def formatCards(self):
        return ', '.join(self.cards)

    #get the card, if she exist strip of self.cards and return card
    def playCard(self):
        print('\033[1;36mMy Cards\033[m')
        print('\033[1;36m=\033[m' * (len(self.cards) * 12))
        for x in self.cards:
            print(self.colorCard(x), end=' ')
        print('')
        print('\033[1;36m=\033[m' * (len(self.cards) * 12))
        while True:
            card = input('What card you want Play: ')
            #card = self.checkCardValid(card)
            if((len(card.split()) == 1 and ':' not in card)): #or (card.lower() == 'plus 2' or card.lower() != 'plus 4')):
                isEqualCard = True if [effect.split(':')[0] for effect in self.cards].count(card) == 1 else False
                if(isEqualCard):
                    card = [effect for effect in self.cards if card in effect][0]
                else:
                    print('existe mais de uma carta igual então diga a cor dela')
            else:
                card = ':'.join(card.split()) if ':' not in card else card
            print(card)
            if(card in self.cards): break
            else: print('Carta não encontrada')
        self.cards.remove(card)
        return card

    #if you have a plus, choose between play card or buy, else buy
    def buyPlayCard(self, amtCard):
        plus = [effect for effect in self.cards if 'plus' in effect]
        if (len(plus) >= 1):
            while True:
                print(plus)
                card = input(f'you have card of plus effect, you wuant \033[1;38mBUY\033[m {amtCard} cards or play any card of plus: ')
                if(card in plus):
                    print('certo')
                    self.cards.remove(card)
                    return card
                else:
                    print('carta não encontrada')
        else:
            print(f'you don`t have card of plus, then you will buy {amtCard} cards', end='')
            for x in range(3):
                sleep(0.45)
                print('.',end='')
            sleep(0.3)
            print('')
            return False

    def buyCards(self, len=1):
        self.cards += self.deck.getCards(len)

    def Uno(self):
        self.uno = True if len(self.cards) == 1 else False

class Game(Deck):
    def __init__(self, deck, lenPlayers):
        self.deck = deck
        self.Players = [Player(x, deck, deck.getCards(7)) for x in range(lenPlayers)]
        self.curPlayer = 0
        self.direction = True
        self.lastCard = str()
        self.plus = 0
        self.sequence = []

    # skip the amount of players passed in the parameter
    def nextPlayer(self, length=1):
        sum = 1 if self.direction else -1
        for x in range(length):
            self.curPlayer += sum
            if self.curPlayer >= len(self.Players):
                self.curPlayer = 0
            elif self.curPlayer < 0:
                self.curPlayer == len(self.Players)

    #choose the card and the amount passed by the parameter, execute this function
    def specialCard(self, card, length=1):
        card = card.split(':')[0]
        if card == 'block':
            self.nextPlayer(length)
        elif card == 'return':
            for k in range(length):
                self.direction = False if self.direction == True else True
        elif card == 'plus 2':
            self.plus += length * 2
        elif card == 'plus 4':
            self.plus += length * 4

    #buy the amount of cards, passed in parameter and buy by the index  of current Player (self.curPlayer)
    def buyCard(self, plus=False, length=1):
        length = self.plus if plus else length
        self.Players[self.curPlayer].buyCards(length)
        self.plus = 0

    #play card selected of player and append adds the sequence
    def play(self):
        if(self.plus > 1):
            card = self.Players[self.curPlayer].buyPlayCard(self.plus)
            if(card == False):
                print('comprar')
                self.buyCard(length=self.plus)
            else:
                self.sequence.append(card)
                self.specialCard(card)
        else:
            card = self.sequence.append(self.Players[self.curPlayer].playCard())
        self.lastCard = card
        self.nextPlayer()

    def winPlayer(self, player):
        self.Players[player].victory += 1

    def round(self):
        self.play()
        #while True:

Deck = Deck()
Game = Game(Deck, 4)
Game.round()