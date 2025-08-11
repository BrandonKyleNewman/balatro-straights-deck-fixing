class Card:
    def __init__(self,rank,name,suit):
        self.rank = rank
        self.name = name
        self.suit = suit

class Deck:
    def __init__(self,suits,ranks,names):
        self.full_deck = create_deck(suits,ranks,names)
    
    def create_deck(self,suits,ranks,names):
        deck = []
        for suit in suits:
            for rank in ranks:
                for name in names:
                    deck.append(Card(rank,name,suit))