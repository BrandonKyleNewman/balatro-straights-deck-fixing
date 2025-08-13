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
            was_hand_replenish_successful = self.replenish_hand()
            if not was_hand_replenish_successful:
                break
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
            else:
                return False
        return True
    
    def take_action(self, discards_remaining, strategy):
        initial_hand = deepcopy(self.hand)
        played_straight = self.can_play_straight()
        if played_straight:
            score = 30
            played_cards = []
            for idx in played_straight:
                score += self.hand[idx].rank
                played_cards.append(self.hand[idx])
                del self.hand[idx]
            self.final_score += (score*4)
            res = str(("play","yes", score*4, played_straight, played_cards, initial_hand, self.hand))
            return res
        else:
            cards = []
            if discards_remaining:
                idxes_to_discard = self.enact_strategy(strategy)
                for i in range(len(idxes_to_discard)-1,-1,-1):
                    cards.append(self.hand[i])
                    del self.hand[i]
                res = str(("discard","no","no",0, cards, initial_hand, self.hand))
                return res
            else:
                idxes_to_discard = self.enact_strategy(strategy)
                for i in range(len(idxes_to_discard)-1,-1,-1):
                    cards.append(self.hand[i])
                    del self.hand[i]
                self.final_score += 5
                res = str(("play","no",5, cards, initial_hand, self.hand))
                return res

#vector: [play or discard, is straight, value, cards_acted_on]
        
    def can_play_straight(self):
        hand_catalog = {}
        for i,card in enumerate(self.hand):
            if card.rank not in hand_catalog:
                hand_catalog[card.rank] = []
            hand_catalog[card.rank].append(i)
        for i in range(14,1,-1):
            play_hand = []
            for j in range(5):
                if i-j in hand_catalog:
                    play_hand.append(hand_catalog[i-j][0])
                if len(play_hand) == 5:
                    return play_hand
        return []

    def enact_strategy(self,strategy):
        idxes_to_discard = set()
        def discard_randomly():
            if len(self.hand) > 5:
                num_to_discard = random.randint(1,5)
            else:
                num_to_discard = random.randint(1,len(self.hand))
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

def run_simulation():
    test_deck = generate_n_decks(1)[0]
    results = {}
    for _ in range(1000):
        g = Game(test_deck,4,2,8)
        g.play_game()
        if g.final_score not in results:
            results[g.final_score] = []
        results[g.final_score].append(g.all_actions)

    print(results.keys())
    for score in range(1500,200,-1):
        if score in results:
            print(score)
            for elem in results[score]:
                for s_elem in elem:
                    print(s_elem)
                print("")
            print("------------")
            
run_simulation()
# most likely to be a straight
# [4,5,6,7,8] is a straight
# [4,4,6,7,8] one away from a straight, non-consequtive
# [4,5,6,7,9] one away from a straight, consequtive