import pytest
import poker_equity as utils


def test_get_kicker_high_card():
    rank_freqs = {
        13: 1,
        12: 1,
        10: 1,
        7: 1,
        6: 1,
        3: 1, 
        2: 1
    }
    to_remove = [13]
    kicker_length = 4
    assert(utils.get_kicker(to_remove, rank_freqs, kicker_length) == [12, 10, 7, 6])

def test_get_kicker_two_pair():
    rank_freqs = {
        13: 2,
        11: 2,
        10: 1,
        2: 1
    }
    to_remove = [13, 11]
    kicker_length = 1
    assert(utils.get_kicker(to_remove, rank_freqs, kicker_length) == [10])

def test_get_kicker_quads():
    rank_freqs = {
        4: 4,
        9: 1,
        10: 1,
        2: 1,
    }
    to_remove = [4]
    kicker_length = 1
    assert(utils.get_kicker(to_remove, rank_freqs, kicker_length) == [10])

def test_detect_flush1():
    suit_freqs = {
        'H': [7, 9, 13, 2, 12],
        'S': [1],
        'D': [6]
    }
    assert(utils.detect_flush(suit_freqs) == [13, 12, 9, 7, 2])

def test_detect_flush2():
    suit_freqs = {
        'H': [7, 9, 13, 2, 12, 3],
        'S': [13]
    }
    assert(utils.detect_flush(suit_freqs) == [13, 12, 9, 7, 3])
    
def test_detect_straight_valid():
    rank_freqs = {
        10: 2,
        9: 1, 
        8: 1,
        7: 1, 
        6: 1, 
        2: 1,
    }
    assert(utils.detect_straight(rank_freqs) == 10)

def test_detect_straight_invalid():
    rank_freqs = {
        10: 3,
        9: 1, 
        7: 1, 
        6: 1, 
        2: 1,
    }
    assert(utils.detect_straight(rank_freqs) == False)

def test_evaluate_hand_high_card():
    hand = [(13, 'D'), (3, 'H')]
    board = [(10, 'S'), (9, 'H'), (7, 'S'), (12, 'C'), (2, 'C')]
    assert(utils.evaluate_hand(hand, board) == (9, 13, [12, 10, 9, 7]))

def test_evaluate_hand_pair():
    hand = [(13, 'D'), (12, 'S')]
    board = [(13, 'S'), (2, 'H'), (1, 'H'), (10, 'D'), (6, 'D')]
    assert(utils.evaluate_hand(hand, board) == (8, 13, [12, 10, 6]))

def test_evaluate_hand_two_pair():
    hand = [(13, 'D'), (12, 'D')]
    board = [(13, 'S'), (12, 'S'), (9, 'H'), (8, 'H'), (2, 'S')]
    assert(utils.evaluate_hand(hand, board) == (7, 13, 12, [9]))

def test_evaluate_hand_trips():
    hand = [(13, 'D'), (12, 'D')]
    board = [(13, 'H'), (13, 'S'), (9, 'H'), (5, 'S'), (2, 'D')]
    assert(utils.evaluate_hand(hand, board) == (6, 13, [12, 9]))

def test_evaluate_hand_straight():
    hand = [(7, 'D'), (6, 'S')]
    board = [(5, 'H'), (4, 'S'), (3, 'D'), (2, 'C'), (13, 'H')]
    assert(utils.evaluate_hand(hand, board) == (5, 7))

def test_evaluate_hand_flush():
    hand = [(13, 'S'), (12, 'S')]
    board = [(4, 'S'), (3, 'S'), (6, 'H'), (2, 'S'), (10, 'D')]
    assert(utils.evaluate_hand(hand, board) == (4, [13, 12, 4, 3, 2]))

def test_evaluate_hand_full_house():
    hand = [(13, 'S'), (12, 'S')]
    board = [(13, 'D'), (12, 'H'), (12, 'C'), (6, 'D'), (5, 'C')]
    assert(utils.evaluate_hand(hand, board) == (3, 12, 13))

def test_evaluate_hand_quads():
    hand = [(7, 'H'), (7, 'S')]
    board = [(7, 'D'), (7, 'C'), (5, 'D'), (5, 'H'), (5, 'C')]
    assert(utils.evaluate_hand(hand, board) == (2, [5]))

def test_evaluate_hand_straight_flush():
    hand = [(10, 'S'), (11, 'S')]
    board = [(9, 'S'), (8, 'S'), (7, 'S'), (6, 'S'), (5, 'H')]
    assert(utils.evaluate_hand(hand, board) == (1, 11))

def test_evaluate_hand_royal_flush():
    hand = [(13, 'S'), (12, 'S')]
    board = [(11, 'S'), (10, 'S'), (9, 'S'), (8, 'S'), (7, 'H')]
    assert(utils.evaluate_hand(hand, board) == 0)
    