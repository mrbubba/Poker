__author__ = 'mark'


class Player(object):
    """The player object
    Attributes:

        name(str):  players name
        stack(int):  players current chip stack
        hole(list):  a list that holds the two private cards for the player
        equity(int):  how much the current player has put in the current round
                      of betting
        action(bool):  if true allows player to act
        table(obj);  the table object
        missed_big_blind(bool): true if the player was inactive for the last
                                big blind
        missed_small_blind(bool): true if the player was inactive for the last
                                  small blind
        dead_button(bool):  true if player is active, is the button, and has
                           missed either blind.  (Player will be inactive for
                           the hand.

     Methods:

        fold:   Removes player from all open pots(ends action for this hand),
                and sets self.action to false
        check:  Only available if pot.current_bet is 0, passes tells table to
                pass action, and sets self.action to false
        call:   transfers money from self.stack to the current pot = to the
                current_bet and sets self.action to false
        bet:    transfers money from self.stack to the current pot.  Must be
                >= pot.current_bet + pot.bet_increment.  Unless the player is
                all in for a lesser amount and sets self.action to false
        play:  Toggle seat.active to True or False
        change_seat:  Change to another available seat

    """

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hole = []
        self.equity = int()
        self.action = False
        self.table = None
        self.missed_big_blind = False
        self.missed_small_blind = False
        self.dead_button = False

    def fold(self):
        pass

    def check(self):
        pass

    def call(self):
        pass

    def bet(self):
        pass

    def play(self):
        pass