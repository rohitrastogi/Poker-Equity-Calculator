import constants
import itertools
import random

def generate_deck(hole_cards, board):
    flat_hole_cards = set([card for card in hand for hand in hole_cards] + board)
    return [(card, suit) for suit in constants.SUITS for card in constants.RANKS.keys() if (card, suit) not in flat_hole_cards]

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
            suit_freq[suit].append(constants.RANKS[rank])
        else:
            suit_freq[suit] = [rank]
    return rank_freq, suit_freq

def evaluate_hand(hand, board):
    rank_freq, suit_freq = populate_freqs(hand, board)
    #Sort in decreasing order by rank frequency. Break ties using increasing rank.
    sorted_rank_freqs = sorted(rank_freq.items(), key = lambda kv: ((-kv[1]), constants.RANKS[kv[0]]))
    for i, (rank, freq) in enumerate(sorted_rank_freqs):
        if freq == 4:
            return 2, get_kicker([rank], rank_freq, 1)
        elif freq == 3:
            if sorted_rank_freqs[i + 1][0] == 2:
                trips_rank = constants.RANKS[rank]
                pair_rank = constants.RANKS[sorted_rank_freqs[i+1][0]]
                return 3, constants.RANKS[rank], trips_rank, pair_rank
            else:
                return 5, constants.RANKS[rank], get_kicker([rank], rank_freq, 2)
        elif freq == 2:
            if sorted_rank_freqs[i + 1][1] == 2:
                high_pair_rank = constants.RANKS[rank]
                low_pair_rank = constants.RANKS[sorted_rank_freqs[i+1][0]]
                return 6, high_pair_rank, low_pair_rank, get_kicker([high_pair_rank, low_pair_rank], rank_freq, 1)
            else:
                return evaluate_hand_helper(hand, board, rank_freq, suit_freq, rank)
    #straights, flushes, pair, high cards
    return evaluate_hand_helper(hand, board, rank_freq, suit_freq, rank)


def evaluate_hand_helper(hand, board, rank_freq, suit_freq, rank):
    straight_kicker = detect_straight(rank_freq)
    flush_cards = detect_flush(suit_freq)
    if straight_kicker:
        if straight_kicker == 'A' and flush_cards:
            return 1, None
        elif flush_cards:
            return 2, straight_kicker
        else:
            return 4, straight_kicker
    if flush_cards:
        return 3, flush_cards
    if rank_freq[rank] == 2:
        return 6, get_kicker(constants.RANKS[rank], rank_freq, 3)
    high_card = max(hand + board, key = lambda x: constants.RANKS[x[0]])
    return 1, high_card, get_kicker(high_card, rank_freq, 4)

def get_kicker(to_remove, rank_freqs, kicker_length):
    filtered_ranks = filter(lambda x: x not in to_remove, map(lambda x: constants.RANKS[x], rank_freqs.keys()))
    return sorted(filtered_ranks, reverse = True)[:kicker_length]

def detect_straight(rank_freq):
    max_kicker = -1
    for rank in rank_freq:
        is_valid_straight = True
        upper = constants.RANKS[rank]
        lower = upper - constants.SIZE_OF_HAND + 1
        for i in range(lower, upper + 1):
            if constants.REVERSE_RANKS[i] not in rank_freq:
                is_valid_straight = False
        if is_valid_straight:
            max_kicker = max(constants.RANKS[rank], max_kicker)
    return max_kicker if max_kicker is not -1 else False

def detect_flush(suit_freqs):
    for suit in suit_freqs:
        if len(suit_freqs[suit]) >= 5:
            return sorted(suit_freqs[suit], reverse = True)[:constants.SIZE_OF_HAND]
    return False

def update_simulation_data(hole_cards, board, hand_freqs, wins):
    evaluated_hands = []
    for i, hand in enumerate(hole_cards):
        evaluated_hand = evaluate_hand(hand, board)
        evaluated_hands.append(evaluated_hand)
        hand_freqs[i][evaluated_hand[0] - 1] += 1
    winner_index = evaluated_hands.index(max(evaluated_hands))
    wins[winner_index] += 1
        
def run_simulation(hole_cards, board):
    deck = generate_deck(hole_cards, board)
    hand_freqs = []
    wins = []
    for hand in hole_cards:
        hand_freqs.append([0]* len(constants.HANDS))
        wins.append(0)
    for board in sample_decks(10000, deck, len(board)):
        update_simulation_data(hole_cards, board, hand_freqs, wins)
    print(hand_freqs)
    print(wins)
    








        
