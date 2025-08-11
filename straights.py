import random

class Card:
    def __init__(self,rank,name,suit):
        self.rank = rank
        self.name = name
        self.suit = suit

    def print_card(self):
        print(self.rank, self.name, self.suit)

class Deck:
    def __init__(self,
                 suits=["H","C","S","D"],
                 ranks=[2,3,4,5,6,7,8,9,10,11,12,13,14],
                 names= {
                    2: "2",
                    3: "3",
                    4: "4",
                    5: "5",
                    6: "6",
                    7: "7",
                    8: "8",
                    9: "9",
                    10: "10",
                    11: "J",
                    12: "Q",
                    13: "K",
                    14: "A",
                }):
        self.full_deck = self.create_deck(suits,ranks,names)
        self.shuffle_deck()
    
    def create_deck(self, suits, ranks, names):
        deck = []
        for suit in suits:
            for rank in ranks:
                for name in names:
                    deck.append(Card(rank,name,suit))
        return deck
    
    def shuffle_deck(self):
        random.shuffle(self.full_deck)

    def draw_card(self):
        return self.full_deck.pop().print_card()
