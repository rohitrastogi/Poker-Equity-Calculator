import constants
import itertools
import random

def generate_deck(hole_cards):
    return [(card, suit) for suit in constants.SUITS for card in constants.RANKS.keys()].remove()

def enumerate_decks(deck, board_size):
    return itertools.combinations(deck, constants.MAX_BOARD_SIZE - board_size )

def sample_decks(num_samples, deck, board_size):
    for _ in num_samples:
        yield random.sample(deck, constants.MAX_BOARD_SIZE - board_size) 

def populate_freqs(hole_cards, board):
    rank_freq = {}
    suit_freq = {}
    for (rank, suit) in hole_cards + board:
        if rank in rank_freq:
            rank_freq[rank] += 1
        else:
            rank_freq[rank] = 1
        
        if suit in suit_freq:
            suit_freq[suit] += 1
        else:
            suit_freq[suit] = 1
    return rank_freq, suit_freq

def evaluate_hand(hole_cards, board):
    rank_freq, suit_freq = populate_freqs(hole_cards, board)
    sorted_freqs = sorted(rank_freq.items(), key = lambda kv: ((-kv[1]), constants.RANKS[kv[0]]))
    for i, (rank, freq) in enumerate(sorted_freqs):
        if freq == 4:
            return 2, rank
        elif freq == 3:
            if sorted_freqs[i + 1][1] == 2:
                return 3, rank
            else:
                return 5, rank
        elif freq == 2:
            if sorted_freqs[i + 1][1] == 2:
                return 6, rank
            else:
                return evaluate_hand_helper(hole_cards, board, rank_freq, suit_freq, rank)
    #straights, flushes, pair, high cards
    return evaluate_hand_helper(hole_cards, board, rank_freq, suit_freq, rank)
    
def evaluate_hand_helper(hole_cards, board, rank_freq, suit_freq, rank):
    straight_kicker = detect_straight(hole_cards, board, rank_freq)
    flush_kicker = detect_straight(hole_cards, board, suit_freq)
    if straight_kicker:
        if straight_kicker == 'A' and flush_kicker:
            return 1, None
        elif flush_kicker:
            return 2, straight_kicker
        else:
            return 4, straight_kicker
    if flush_kicker:
        return 3, flush_kicker
    if rank_freq[rank] == 2:
        return 6, rank
    return max(map(lambda x: constants.RANKS[x], suit_freq.keys()))









        
