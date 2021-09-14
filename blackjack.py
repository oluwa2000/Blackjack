import random
class Card:
    def __init__(self,suit,rank):
        if rank == "king" or rank == "queen" or rank == "jack":
            self.rank = 10
        elif rank == "ace":
            self.rank = 1
        elif int(rank) < 2 or int(rank) > 10:
            raise ValueError 
        else:
            self.rank = int(rank)
        if suit == "club" or suit == "diamond" or suit == "spade" or suit == "heart":
            self.suit = suit
        else:
            raise ValueError

    def set_rank_11(self):
        if self.rank == "ace":
            self.rank = 11

    def set_rank_1(self):
        if self.rank == "ace":
            self.rank = 1

    def show_card(self):
        print((self.rank,self.suit))

class CardDeck:    
    def __init__(self):
        suit = ["club", "diamond", "heart", "spade"] 
        rank = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        deck = []
        self.removed = []
        self.deck = deck
        for i in range(len(suit)):
            for o in range(len(rank)):
                cards = Card(suit[i], rank[o])
                self.deck.append(cards)

    def clen(self):
        return len(self.deck)

    def removed_len(self):
        return len(self.removed)

    def __contains__(self, v):
        return v in self.removed

    def __getitem__(self, v):
        return self.deck[v]

    def select_card(self):
        x = random.choice(self.deck)
        self.removed.append(x)
        self.deck.remove(x)
        return x

    def get_removed(self):
        return self.removed

class Player:
    def __init__(self,name):
        self.name = name
        self.cards = []
        self.points = 0

    def add_card(self,card):
        self.cards.append(card)
        self.update_points(card)
        # self.update_points()
    def check_A(self):
        for i in self.cards:
            if i.rank == 1:
                return True
            else:
                return False

    def change_A(self):
        if self.check_A()  == True:
            change = input("Would you like to change Ace value (yes/no) " )
            if change.lower == "yes":
                for i in self.cards:
                    if i.rank == 1:
                        i.set_rank_11()
                    elif i.rank == 11:
                        i.set_rank_1()
            else:
                pass

    def update_points(self,card):
        self.points = self.points + card.rank
        return self.points

    def show_cards(self):
        for i in self.cards:
            i.show_card()

class Blackjack:
    def __init__(self):
        self.card_deck = CardDeck()
        self.house = Player("House")
        self.removing = self.card_deck.get_removed()
        self.players = [self.house]
        self.hold = []
        self.bust = []

    def get_deck(self):
        return self.card_deck

    def removed_cards(self):
        return self.removing

    def removed_len(self):
        return self.card_deck.removed_len()

    def house_edge(self,t):
        denominator = self.deck_len()
        count1 = 0
        count2 = 0
        if self.house in self.players and t in self.players and t.name != "House":
            if t.points > self.house.points and t.points > 16 and t.name != "House":
                x = t.points - self.house.points + 1
                y = 21 - self.house.points
                while x <= y:
                    for z in self.get_deck():
                        if z.rank == x:
                            count1 += 1
                    for n in self.removed_cards():
                        if n.rank == x:
                            count2 += 1
            elif t.points < 17:
                x = 17 - self.house.points
                y = 21 - self.house.points
                while x <= y:
                    for z in self.get_deck():
                        if z.rank == x:
                            count1 += 1
                    for n in self.removed_cards():
                        if n.rank == x:
                            count2 += 1
                    x += 1
        elif self.house in self.hold and t in self.hold:
            if t.points > self.house.points:
                count1 = 0
                count2 = 0
            else:
                count1 = denominator
                count2 = 0
        elif self.house in self.bust:
            count1 = 0
            count2 = 0
        elif self.house in self.hold and t in self.players:
            if t.points < self.house.points:
                x = 21 - self.house.points + 1
                count1 = 0
                count2 = 0
                while x <= 13:
                    for z in self.get_deck():
                        if z.rank == x:
                            count1 += 1
                    for n in self.removed_cards():
                        if n.rank == x:
                            count2 += 1
                    x += 1
        else:
            x = 21 - t.points + 1
            count1 = 0
            count2 = 0
            while x <= 13:
                for z in self.get_deck():
                    if z.rank == x:
                        count1 += 1
                for n in self.removed_cards():
                    if n.rank == x:
                        count2 += 1
                x += 1

        probability = (count1-count2)/denominator
        if probability == 0:
            return "The House has no edge"
        else:           
            return "The current house edge over " + t.name + " is " + str(round(probability,3))

    def deck_len(self):
        return self.card_deck.clen()

    def get_players(self):
        return self.players

    def add_player(self,names):
        self.players.append(Player(names))

    def black_jack(self,V):
        if V.point == 21:
            return True 

    def Hold(self,v):
        self.hold.append(v)
        self.players.remove(v)

    def Bust(self,v):
        self.bust.append(v)
        self.players.remove(v)

    def playing(self):
        return len(self.players)

    def deal(self):
        for i in self.players:  
            if i.name != "House":
                    print(self.house_edge(i))
                    print("")        
            if i.name == "House" and i.points > 16 and i.points < 22:
                self.Hold(i)
            else:   
                deal = input(str(i.name)+ " has " + str(i.points)+" points. Would " + str(i.name) + " like to hit? (Yes/No) ")                  
                if deal.lower() == "yes":                      
                    i.add_card(self.card_deck.select_card())
                    if i.points > 21:
                        print("")
                        print(i.name + " Has been Busted")
                        print("")
                        self.Bust(i)
                    elif i.name == "House" and i.points == 21:
                        print("")
                        print(i.name + " Has a Blackjack!!")
                        print("")
                        return 1
                    elif i.points == 21:
                        print("")
                        print(i.name + " Has a Blackjack!!")
                        print("")
                        self.Hold(i)
                    self.show_player_cards(i)
                    # i.change_A()
                else:
                    self.Hold(i)
                    self.show_player_cards(i)

    def winner(self):
        max = 0
        count = 0
        if self.house in self.bust:
            for i in self.hold:
                print(i.name + " Beat the house!!!")
                count += 1
        for i in self.hold:
            if i.points > self.house.points:
                print(i.name + " Beat the house!!!")
                count += 1
        if count == 0:
            return  self.house.name + " wins the game!!"
        else:
            return "End of Game!"


    def show_player_cards(self,i):
        # if i.name != "House":
        print(i.name)
        i.show_cards()
        print("player points = " + str(i.points))
        print("")

    def show_house_cards(self):
        for i in self.hold:
            if i.name == "House":
                print(i.name)
                i.show_cards()
                print("player points = " + str(i.points))
                print("")

def play_blackjack():
    number = input("how many players want to play? ") 
    number = int(number)
    players = []
    count = 1
    while number > 0:   
        names = input("Write player names: " )
        players.append(names)
        number -= 1
        count += 1
    current = Blackjack()
    for i in players:
        current.add_player(i)
    while current.playing() > 0:
        current.deal()
        if current.deal() == 1:
            return "House has won the game"
    print(current.winner())

print(play_blackjack())
# players = ["S","J","Ja"]
# new= Blackjack()


# for i in players:
#     new.add_player(i)

# new.deal()
# new.deal()
# print(new.removed_len())
# new.deal()
# print(new.playing())
# new.show_player_cards()




    
