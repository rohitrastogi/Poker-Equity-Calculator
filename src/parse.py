import argparse
import constants

def validate_card(card):
    if len(card) is not 2:
        raise ValueError("A valid card consists of 1 rank and 1 suit.")
    rank = card[0]
    suit = card[1]
    if rank not in constants.RANK_TO_INT or suit not in constants.SUITS:
        raise ValueError("Rank must be one of 2345678910JQKA. Suit must be one of cdhs.")

def cards_to_tups(cards):
    return list(map(lambda x: (constants.RANK_TO_INT[x[0]], x[1]), cards))

def tups_to_hole(tups):
    return [tups[i:i+2] for i in range(0, len(tups), constants.MAX_HOLE_SIZE)]

#a little hacky
class ValidateCards(argparse.Action):
    cards = set()
    def __call__(self, parser, namespace, values, option_string=None):
        for card in values:
            if card in self.cards:
                raise ValueError("Input must not include duplicate cards.")
            self.cards.add(card)
            validate_card(card)
        #validate board cards
        if self.dest == 'b': 
            if len(values) > constants.MAX_BOARD_SIZE:
                raise ValueError("Board must have less than or equal to 5 cards.")
            setattr(namespace, self.dest, cards_to_tups(values))
        #validate hole cards
        else:
            if len(values) %2 != 0:
                raise ValueError("Hole card input must two cards per player.")
            if len(values) < 4:
                    raise ValueError("Hole card input must include hole cards for at least 2 players.")
            if len(values) > 20:
                    raise ValueError("Hole card input must include hole cards for at most 10 players.")
            setattr(namespace, self.dest, tups_to_hole(cards_to_tups(values)))

def parse():
    #TODO: extend command line arguments to include num_its for Monte Carlo and num_chunks for parallelized version
    parser = argparse.ArgumentParser(description='Calculate hand equity with supplied hole cards and optional board cards.')
    parser.add_argument('hole_cards', metavar = 'hc', nargs = '*', action = ValidateCards, help = 'A list of all \
    players\' hole cards. Every player must have two hole cards and you must supply cards for at least players. Ex. Ad Ah 7d 2s')
    parser.add_argument('--board', '--b', metavar = 'bc', nargs = '*', action = ValidateCards, help = 'A list of all board cards. \
    A board may include at most 5 cards per Texas Hold\'em Rules.')
    parser.add_argument('--e', '--exact', action = 'store_true', help = 'Supply --e flag if you\'d like hand equity to be calculated exactly \
    using exhaustive enumeration. Note that exhasutive enumeration is substantially slower than estimating hand equity using Monte \
    Carlo Simulation (default behavior) and Monte Carlo simulation is usually accurate within 1%.')
    parser.add_argument('--verbose', '--v', action = 'store_true', help = 'Supply --v flag if you\'d like detailed output on the probability of \
    making all Texas Hold\'em hands.')
    parser.add_argument('--p', '--parallel', action = 'store_true', help = 'Supply --p flag if you\'d like the computation to be parallelized \
    over 4 workers. Note that there is only a speed benefit of parallelizing the computation if the --e flag is supplied, as Monte \
    Carlo simulation is very fast on the main thread.')
    #convert namespace object to dictionary
    return vars(parser.parse_args())
