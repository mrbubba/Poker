__author__ = 'mark'
class Analyzer(object):
    """ Analyzer object

    Attributes:

       table(obj):  table object

    Methods:

        analyze:    gets the community cards and list of pots from the dealer,
                    for each pot awards the chips to the winner/s
                    If an all in player wins, analyze will reset that seats
                    active to True
    """

    def __init__(self, table):
        self.table = table
