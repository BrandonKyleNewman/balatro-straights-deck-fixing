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
        self.all_actions = []
    
    def play_game(self):
        self.reset_game()
        hands_remaining = self.max_hands
        discards_remaining = self.max_discards
        while hands_remaining:
            self.replenish_hand()
            self.hand.sort()
            action_taken = self.take_action(discards_remaining, "discard randomly")
            if action_taken[0] == "play":
                hands_remaining -= 1
            else:
                discards_remaining -= 1
            self.all_actions.append(action_taken)
    
    def reset_game(self):
        self.hand = []
        self.final_score = 0
        self.deck = deepcopy(self.base_deck)
    
    def replenish_hand(self):
        for _ in range(self.max_hand_size-len(self.hand)):
            card = self.deck.draw_card()
            if card:
                self.hand.append(card)
    
    def take_action(self, discards_remaining, strategy):
        index_straight = -1
        for i in range(len(self.hand)-4):
            if self.is_straight_starting_at_s_i(i):
                index_straight = i
        if index_straight != -1:
            score = 0
            for i in range(5):
                score += (self.hand[index_straight+i].rank + 30)
            self.final_score += (score*4)
            action_taken = ["play","no","yes",score*4]
            self.hand = self.hand[:index_straight] + self.hand[index_straight+5:]
            return action_taken
        else:
            if discards_remaining:
                idxes_to_discard = self.enact_strategy(strategy)
                for i in range(len(idxes_to_discard)-1,-1,-1):
                    del self.hand[i]
                return ["discard","no","no",0]
            else:
                idxes_to_discard = self.enact_strategy(strategy)
                for i in range(len(idxes_to_discard)-1,-1,-1):
                    del self.hand[i]
                self.final_score += 5
                return ["play","yes","no",5]
        
    def is_straight_starting_at_s_i(self, s_i):
        return self.hand[s_i+1].rank == self.hand[s_i].rank +1 and self.hand[s_i+2].rank == self.hand[s_i].rank+2 and self.hand[s_i+3].rank == self.hand[s_i].rank+3 and self.hand[s_i+4].rank == self.hand[s_i].rank+4
    
    def enact_strategy(self,strategy):
        idxes_to_discard = set()
        def discard_randomly():
            if len(self.hand) > 5:
                num_to_discard = random.randint(1,5)
            else:
                num_to_discard = len(self.hand)
            while num_to_discard:
                idx_to_discard = random.randint(0,len(self.hand)-1)
                if idx_to_discard not in idxes_to_discard:
                    idxes_to_discard.add(idx_to_discard)
                    num_to_discard -= 1
        if strategy == "discard randomly":
            discard_randomly()
        else:
            None
        return list(idxes_to_discard)

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
    print(g.final_score, g.all_actions)


# most likely to be a straight
# [4,5,6,7,8] is a straight
# [4,4,6,7,8] one away from a straight, non-consequtive
# [4,5,6,7,9] one away from a straight, consequtive
# 