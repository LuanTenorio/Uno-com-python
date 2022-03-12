import random
from time import sleep
class Deck():
    def __init__(self):
        self.cards = {}
        self.COLORS = ['red', 'green', 'blue', 'yellow', 'black']
        self.TYPECARDS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'block', 'return', 'plus 2']
        self.restardDeck()

    def restardDeck(self):
        for color in self.COLORS:
            if(color != 'black'):
                self.cards.update({color: [f'{card}:{color}' for card in self.TYPECARDS] + [f'{card}:{color}' for card in self.TYPECARDS]})
        self.cards.update({'black': []})
        for x in range(4):
            self.cards['black'].append('plus 4:black')
            self.cards['black'].append('color:black')

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
                    print('no cards')
                    return cards if(len(cards) > 0) else False
            else:
                if(len(color[1]) >= 1):
                    card = random.choice(self.cards[color[0]])
                    cards.append(card)
                    if(self.removeCard(card)):
                        return cards if(len(cards) > 0) else False
                    totcards += 1
                else:
                    if(color[0] in self.cards.keys()):
                        self.cards.pop(color[0])
                    continue
        return cards

    #a way to display text
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
        else:
            codeColor = '37'
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

    #return true if color can be played else false
    def checkIsColor(self, lastCard, curCard):
        lastCard = lastCard.split(':') if isinstance(lastCard, str) else lastCard
        curCard = curCard.split(':') if isinstance(curCard, str) else curCard
        return True if lastCard[1] == curCard[1] else False

    def checkWin(self):
        return True if len(self.cards) == 0 else False

    #verify if card/color can be played and redirect for the methods
    def redirectPurchase(self, lastCard, amtCard, lastPlus, curColor):
        if(lastCard != ''):
            lastCard = lastCard.split(':')
            help = [card for card in self.cards if (card.split(':')[1] == curColor or card.split(':')[1] == 'black') or card.split(':')[0] == lastCard[0]]
            if(len(help) > 0):
                print(f'\033[1;36mHelp\033[m')
                print(f'\033[1;36m=\033[m' * (len(self.cards) * 12))
                for x in help:
                    print(self.colorCard(x), end=' ')
                print('')
                print(f'\033[1;36m=\033[m' * (len(self.cards) * 12))
            #lenCards = len([card for card in self.cards if card.split(':')[1] == curColor or card.split(':')[0] == lastCard[0]])
            lenCards = 1

            if(lenCards == 0):
                self.buyCards()
                print(f'you don\'t have a card', end='')
                for x in range(3):
                    sleep(0.45)
                    print('.', end='')
                sleep(0.3)
                print('')
                return False
            elif 'plus' in lastCard[0] and lastPlus == False:
                return self.buyPlayCard(amtCard)
            else:
                return self.playCard(lastCard, curColor)
        else:
            return self.playCard(lastCard, curColor)


    #get the card, if she exist strip of self.cards and return card
    def playCard(self, lastCard, curColor):
        if curColor == 'yellow': lineColor = '33'
        elif curColor == 'red': lineColor = '31'
        elif curColor == 'green': lineColor = '32'
        elif curColor == 'blue': lineColor = '34'
        elif curColor == 'black': lineColor = '30'
        else: lineColor = '37'
        print(f'\033[1;{lineColor}mMy Cards\033[m')
        print(f'\033[1;{lineColor}m=\033[m' * (len(self.cards) * 12))
        for x in self.cards:
            print(self.colorCard(x), end=' ')
        print('')
        print(f'\033[1;{lineColor}m=\033[m' * (len(self.cards) * 12))
        while True:
            card = input(f'What card you want Play ({self.id})({curColor}): ')

            if(card == 'buy'):
                self.buyCards()
                return 'buy'
            print(card)
            if((len(card.split()) == 1 and ':' not in card)): #or (card.lower() == 'plus 2' or card.lower() != 'plus 4')):
                if(card.split()[0] == 'plus 4'):
                    pass
                isEqualCard = True if [effect.split(':')[0] for effect in self.cards].count(card) == 1 else False
                if(isEqualCard):
                    card = [effect for effect in self.cards if card in effect][0]
                else:
                    print('there are two more cards of the same, so say the color')
                    continue
            else:
                card = ':'.join(card.split()) if ':' not in card else card

            if (card.split(':')[1] != 'black' and lastCard[1] != 'black'):
                if(card.split(':')[1] != curColor):
                    if (card.split(':')[0] == lastCard[0]):
                        print(f'aaa')
                    else:
                        print(f'Card "{card}" is not color {lastCard[1]}')
                        continue
            if(card in self.cards): break
            else: print(f'Card "{card}" not found')
        self.cards.remove(card)
        if (self.Uno()):
            print('\033[30munoooo\033[m')
        if (self.checkWin()):
            return True
        return card

    #if you have a plus, choose between play card or buy, else buy
    def buyPlayCard(self, amtCard):
        print(self.cards)
        plus = [effect for effect in self.cards if 'plus' in effect]
        if (len(plus) >= 1):
            while True:
                card = input(f'You have card of plus effect, you wuant \033[1;38mBUY\033[m {amtCard} cards or play any card of plus({self.id})(buy/card): ')
                if(card in plus):
                    self.cards.remove(card)
                    if (self.Uno()):
                        print('\033[30munoooo\033[m')
                    if (self.checkWin()):
                        return True
                    return card
                elif(card.lower() == 'buy'.lower()):
                    self.buyCards(amtCard)
                    return False
                else:
                    print('Card not found')
        else:
            print(f'You don`t have card of plus, then you will buy {amtCard} cards', end='')
            for x in range(3):
                sleep(0.45)
                print('.',end='')
            sleep(0.3)
            print('')
            return False

    def buyCards(self, len=1):
        self.cards += self.deck.getCards(len)

    def Uno(self):
        print('unoooo')
        for x in range(3):
            print(len(self.cards))
        isUno = True if len(self.cards) == 1 else False
        self.uno = isUno
        return isUno

class Game(Deck):
    def __init__(self, deck, lenPlayers):
        self.deck = deck
        self.lenPlayers = lenPlayers
        self.restartedGame()
        self.playesWin = {}
        for x in range(len(self.Players)):
            self.playesWin.update({f'Player {x}': 0})

    #resets the game and the deck so you can play again
    def restartedGame(self):
        self.deck.restardDeck()
        self.Players = [Player(x, self.deck, self.deck.getCards(30)) for x in range(self.lenPlayers)]
        self.curPlayer = 0
        self.direction = True
        self.plus = 0
        self.sequence = [self.deck.getCards(1)[0]]
        self.lastCard = self.sequence[-1]
        self.lastPlus = False
        self.curColor = self.lastCard.split(':')[1]

    # skip the amount of players passed in the parameter
    def nextPlayer(self, length=1):
        sum = 1 if self.direction else -1
        for x in range(length):
            self.curPlayer += sum
            if self.curPlayer >= len(self.Players):
                self.curPlayer = 0
            elif self.curPlayer < 0:
                self.curPlayer = len(self.Players)

    #Select the color if exist in self.deck.COLORS else return false
    def changeColor(self, color, select=True):
        color = color.split(':')[1] if color.find(':') != -1 else color
        COLOR = self.deck.COLORS.copy()
        COLOR.remove('black')
        if(select):
            if color in COLOR:
                self.curColor = color
            else:
                print('This color is not in the game')
                print(', '.join(COLOR))
                return False
        else:
            return False

    #choose the card and the amount passed by the parameter, execute this function
    def specialCard(self, card, length=1):
        card = card.split(':')[0]
        if card == 'block':
            self.nextPlayer(length)
        elif card == 'return':
            for k in range(length):
                self.direction = False if self.direction else True
        elif card == 'color':
            while True:
                color = input('Select the card color you want: ')
                if(self.changeColor(color) != False):
                    break
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
        #card = self.sequence.append(self.Players[self.curPlayer].redirectPurchase(self.sequence[-1] if len(self.sequence) >= 1 else '', self.plus))
        print(f'sequence: ', end=' ')
        for x in self.sequence:
            print(self.Players[0].colorCard(x), end=' ')
        print('')

        card = self.Players[self.curPlayer].redirectPurchase(self.sequence[-1] if len(self.sequence) >= 1 else '', self.plus, self.lastPlus, self.curColor)
        if card == True:
            self.playesWin[f'Player {self.curPlayer}'] += 1
            self.lastPlayerWin = self.curPlayer
            print(self.playesWin)
            print(self.curPlayer)
            return True
        if(card == 'buy'):
            print('buy')
        elif card == False:
            self.lastPlus = True
        else:
            self.lastCard = card
            self.curColor = self.lastCard.split(':')[1]
            self.specialCard(card)
            self.sequence.append(card)
            self.lastCard = self.sequence[-1] if len(self.sequence) >= 1 else self.lastCard
            self.changeColor(self.lastCard, False)
            self.lastPlus = False
        self.nextPlayer()

    def winPlayer(self, player):
        self.Players[player].victory += 1

    #play while nobody wins
    def round(self):
        while True:
            if self.play():
                print(self.playesWin)
                self.deck.show([f'{k}: {x} points' for k, x in self.playesWin.items()])
                print(f'Player {self.lastPlayerWin} win')
                break

Deck = Deck()
lenPlayer = 0

while True:
    try:
        lenPlayer = int(input('how much will players play?').strip())
    except:
        print('type a number')
        continue
    if lenPlayer <= 1: print('Must have at least 2 players')
    elif lenPlayer > 10: print('Must have a maximum of 10 players')
    else: break
    continue

Game = Game(Deck, lenPlayer)
Game.round()
while True:
    again = input('you want play again? (yes/no)').upper().strip()
    if again == 'YES':
        Game.restartedGame()
        Game.round()

    elif again == 'NO':
        break
