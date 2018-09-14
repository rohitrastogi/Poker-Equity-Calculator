HANDS = (
    'High Card',
    'Pair',
    'Two Pair',
    'Three of a Kind',
    'Straight',
    'Flush', 
    'Full House',
    'Four of a Kind', 
    'Straight Flush',
    'Royal Flush'
)

SUITS = ('S', 'H', 'D', 'C')

RANK_TO_INT = {
    'A': 13,
    'K': 12, 
    'Q': 11, 
    'J': 10,
    'T': 9,
    '9': 8, 
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4, 
    '4': 3, 
    '3': 2, 
    '2': 1
}

INT_TO_RANK = {v: k for k, v in RANK_TO_INT.items()}

MAX_BOARD_SIZE = 5

MAX_HOLE_SIZE = 2

SIZE_OF_HAND = 5