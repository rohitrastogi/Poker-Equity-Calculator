import argparse
import constants

#not sure if this is the right way to go...
def exit_with_message(msg):
    print(msg)
    exit()

def validate_card(card):
    if len(card) is not 2:
        raise ValueError("A valid card consists of 1 rank and 1 suit.")
    rank = card[0]
    suit = card[1]
    if rank not in constants.RANK_TO_INT or suit not in constants.SUITS:
        raise ValueError("Rank must be one of 2345678910JQKA. Suit must be one of CDHS.")

def cards_to_tups(cards):
    return list(map(lambda x: (constants.RANK_TO_INT[x[0]], x[1]), cards))
    
class ValidateHoleCards(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) %2 is not 0:
            raise ValueError("Hole card input must include an even number of cards.")
        if len(values) < 4:
            raise ValueError("Hole card input must include at least 4 cards.")
        if len(values) > 20:
            raise ValueError("Hole card input must have 20 cards at maximum.")
        for card in values:
            validate_card(card)
        if len(values) > len(set(values)):
            raise ValueError("Hole cards must not include any duplicates.")
        setattr(namespace, self.dest, cards_to_tups(values))

class ValidateBoardCards(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) > 4:
            raise ValueError("Board card input must have 4 cards at maximum.")
        for card in values:
            validate_card(card)
        if len(values) > len(set(values)):
            raise ValueError("Board cards must not include any duplicates.")
        setattr(namespace, self.dest, cards_to_tups(values))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hole_cards', nargs = '+', action = ValidateHoleCards)
   # parser.add_argument('-b', nargs = '+', action = ValidateBoardCards)
    args = parser.parse_args()
    print(args)
main()