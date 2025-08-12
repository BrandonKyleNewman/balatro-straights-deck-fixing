import random
from copy import deepcopy
from datetime import datetime

class Card:
    def __init__(self,rank,name,suit):
        self.rank = rank
        self.name = name
        self.suit = suit

    def print_card(self):
        print(self.rank, self.name, self.suit)

    def __lt__(self,other):
        return self.rank < other.rank
    
    def __repr__(self):
        return f"{self.rank},{self.suit}"

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
    
    def create_deck(self, suits, ranks, names):
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append(Card(rank,names[rank],suit))
        return deck
    
    def shuffle_deck(self):
        random.shuffle(self.full_deck)

    def draw_card(self):
        if len(self.full_deck):
            return self.full_deck.pop()

    def __repr__(self):
        return f"{self.full_deck}"
    
class Game:
    def __init__(self,deck,max_hands,max_discards,max_hand_size):
        self.base_deck = deck
        self.max_hands = max_hands
        self.max_discards = max_discards
        self.max_hand_size = max_hand_size
        self.hand = []
        self.deck = None
        self.final_score = 0
    
    def play_game(self):
        self.reset_game()
        hands_remaining = self.max_hands
        discards_remaining = self.max_discards
        while hands_remaining:
            self.replenish_hand()
            self.hand.sort()
            print(self.hand)
            action_taken = self.take_action(discards_remaining)
            if action_taken == "play":
                hands_remaining -= 1
            else:
                discards_remaining -= 1
    
    def reset_game(self):
        self.hand = []
        self.final_score = 0
        self.deck = deepcopy(self.base_deck)
    
    def replenish_hand(self):
        for _ in range(self.max_hand_size-len(self.hand)):
            card = self.deck.draw_card()
            if card:
                self.hand.append(card)
    
    def take_action(self, discards_remaining):
        index_straight = -1
        for i in range(len(self.hand)-4):
            if self.is_straight_starting_at_s_i(i):
                index_straight = i
        if index_straight != -1:
            score = 0
            for i in range(5):
                score += (self.hand[index_straight+i].rank + 30)
            self.final_score += (score*4)
            print("straight at " + str(index_straight) + "! " + str(self.hand) )
            self.hand = self.hand[:index_straight] + self.hand[index_straight+5:]
            return "play"
        else:
            if discards_remaining:
                num_to_discard = random.randint(1,min(5,len(self.hand)))
                while num_to_discard:
                    del self.hand[random.randint(0,len(self.hand)-1)]
                    num_to_discard -= 1
                return "discard"
            else:
                num_to_discard = random.randint(1,min(5,len(self.hand)))
                while num_to_discard:
                    idx = random.randint(0,len(self.hand)-1)
                    self.final_score += self.hand[idx].rank
                    del self.hand[idx]
                    num_to_discard -= 1
                return "play"

    def is_straight_starting_at_s_i(self, s_i):
        return self.hand[s_i+1].rank == self.hand[s_i].rank +1 and self.hand[s_i+2].rank == self.hand[s_i].rank+2 and self.hand[s_i+3].rank == self.hand[s_i].rank+3 and self.hand[s_i+4].rank == self.hand[s_i].rank+4


def generate_n_decks(n):
    all_decks = []
    for _ in range(n+1):
        curr_deck = Deck()
        curr_deck.shuffle_deck()
        num_to_remove = random.randint(3,32)
        for __ in range(num_to_remove):
            curr_deck.draw_card()
        all_decks.append(curr_deck)
    return all_decks


test_deck = generate_n_decks(1)[0]
for _ in range(100):
    g = Game(test_deck,4,2,8)
    g.play_game()
    print(g.final_score)
