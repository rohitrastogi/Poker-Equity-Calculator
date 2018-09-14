import constants
import itertools
import random


def generate_deck(hole_cards, board):
    flat_hole_cards = set([card for hand in hole_cards for card in hand] + board)
    return [(card, suit) for suit in constants.SUITS for card in constants.INT_TO_RANK.keys() if (card, suit) not in flat_hole_cards]

#exhaustively enumerate all possible boards
def enumerate_boards(deck, board_size):
    return itertools.combinations(deck, constants.MAX_BOARD_SIZE - board_size)

#generate num_samples random boards (for Monte Carlo Simulation)
def sample_boards(num_samples, deck, board_size):
    for _ in range(num_samples):
        yield random.sample(deck, constants.MAX_BOARD_SIZE - board_size) 

def populate_freqs(hole_cards, board):
    rank_freq = {}
    suit_freq = {}
    for (rank, suit) in hole_cards + list(board):
        if rank in rank_freq:
            rank_freq[rank] += 1
        else:
            rank_freq[rank] = 1
        
        if suit in suit_freq:
            suit_freq[suit].append(rank)
        else:
            suit_freq[suit] = [rank]
    return rank_freq, suit_freq

def evaluate_hand(hand, board):
    rank_freq, suit_freq = populate_freqs(hand, board)
    #Sort in decreasing order by rank frequency. Break ties using decreasing rank.
    #Example shape: [(13, 2), (12, 2), (4, 2), (10, 1)]
    sorted_rank_freqs = sorted(rank_freq.items(), key = lambda kv: ((-kv[1]), -kv[0]))
    for i, (rank, freq) in enumerate(sorted_rank_freqs):
        #quads
        if freq == 4:
            return 2, get_kicker([rank], rank_freq, 1)
        elif freq == 3:
            #full house 
            if sorted_rank_freqs[i + 1][1] == 2:
                pair_rank = sorted_rank_freqs[i+1][0]
                return 3, rank, pair_rank
            #trips
            else:
                return 6, rank, get_kicker([rank], rank_freq, 2)
        elif freq == 2:
            #two pair
            if sorted_rank_freqs[i + 1][1] == 2:
                low_pair_rank = sorted_rank_freqs[i+1][0]
                return 7, rank, low_pair_rank, get_kicker([rank, low_pair_rank], rank_freq, 1)
            #single pair or possibly a straight or flush
            else:
                return evaluate_hand_helper(hand, board, rank_freq, suit_freq, rank)
    #straights, flushes, high cards
    return evaluate_hand_helper(hand, board, rank_freq, suit_freq, rank)

def evaluate_hand_helper(hand, board, rank_freq, suit_freq, rank):
    straight_kicker = detect_straight(rank_freq)
    flush_cards = detect_flush(suit_freq)
    if straight_kicker:
        #royal flush
        if straight_kicker == constants.RANK_TO_INT['A'] and flush_cards:
            return 0, None
        #straight flush
        elif flush_cards:
            return 1, straight_kicker
        #straight
        else:
            return 5, straight_kicker
    #flush
    if flush_cards:
        return 4, flush_cards
    #single pair
    if rank_freq[rank] == 2:
        return 8, rank, get_kicker([rank], rank_freq, 3)
    high_card = max(hand + list(board), key = lambda x: x[0])
    #high card
    return 9, high_card[0], get_kicker(high_card, rank_freq, 4)

def get_kicker(to_remove, rank_freqs, kicker_length):
    filtered_ranks = filter(lambda x: x not in to_remove, rank_freqs.keys())
    return sorted(filtered_ranks, reverse = True)[:kicker_length]

#return highest card of straight if a straight is present. otherwise, return False
def detect_straight(rank_freqs):
    max_kicker = -1
    for rank in rank_freqs:
        is_valid_straight = True
        lower = rank - constants.SIZE_OF_HAND + 1
        for i in range(lower, rank + 1):
            if i not in rank_freqs:
                is_valid_straight = False
        if is_valid_straight:
            max_kicker = max(rank, max_kicker)
    return max_kicker if max_kicker is not -1 else False

#return list of top 5 cards that make a flush if a flush is present. otherwise, return False 
def detect_flush(suit_freqs):
    for suit in suit_freqs:
        if len(suit_freqs[suit]) >= 5:
            return sorted(suit_freqs[suit], reverse = True)[:constants.SIZE_OF_HAND]
    return False

def update_simulation_state(hole_cards, board, hand_freqs, wins):
    evaluated_hands = []
    for i, hand in enumerate(hole_cards):
        evaluated_hand = evaluate_hand(hand, board)
        evaluated_hands.append(evaluated_hand)
        hand_freqs[i][evaluated_hand[0]] += 1
    random.shuffle(evaluated_hands) #shuffle to randomly distribute ties
    winner_index = evaluated_hands.index(max(evaluated_hands))
    wins[winner_index] += 1

def calculate_equity(hand_freqs, wins):
    total_its = sum(wins)
    wins = [val/total_its for val in wins]
    for i, player_stats in enumerate(hand_freqs):
        for j, stat in enumerate(player_stats):
            hand_freqs[i][j] = stat/total_its
    print(wins)
    print(hand_freqs)
        
def run_simulation(hole_cards, board):
    deck = generate_deck(hole_cards, board)
    hand_freqs = []
    wins = []
    for hand in hole_cards:
        hand_freqs.append([0]* len(constants.HANDS))
        wins.append(0)
    for i, board in enumerate(sample_boards(10000, deck, len(board))):
        update_simulation_state(hole_cards, board, hand_freqs, wins)
    calculate_equity(hand_freqs, wins)
    
run_simulation([[(13, 'D'), (12, 'D')],[(10, 'D'), (9, 'D')]], [])

