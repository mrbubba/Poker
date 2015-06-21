__author__ = 'mark'
class Analyzer(object):
    """ Analyzer object

    Methods:

        Analyze:    gets the community cards and list of pots from the dealer,
                    for each pot awards the chips to the winner/s
    """

    def __init__(self, community_cards, pots):
        self.communitty_cards = community_cards
        self.pots = pots