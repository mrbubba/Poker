__author__ = 'mark'

class Pot(object):
    """The pot object will drive and track the betting action for each round of
        play.

    Attributes:

        pot(int):   total amount of chips in the middle(another words all chips
                    not currently in player.stack)
        init_increment(int):  bet increment at the start of each betting round
        increment(int):  current bet increment for this round of betting
        bet(int):  the current bet
        side_pot(int):  the amount of chips in the current pot
        seats(list):  list of seats currently in the pot not all in
        all_in(list):  list of seats in the current pot that are all in
        active(bool):  set to true when the pot needs to act
        utg(int):  position that is first to act preflop
        first(int):  position of first to act after the flop
        table(obj):  the table object


    methods:

        betting_round:  the main method of pot.  Will be called by dealer to
                        let pot know its time for a round of betting.
        set_action:     either sets player.action to true on the appropriate
                        player object, or calls dealer.deal
        set_bet_increment:  sets the bet_increment appropriately
        new_pot:  creates a new pot if a player is all in for less then the
                    current bet(if two or more players are in for the higher amount)

    """

    def __init__(self, pot, init_increment, increment, seats, all_in, bet, utg, first, table):
        self.pot = pot
        self.init_increment = init_increment
        self.increment = increment
        self.seats = seats
        self.all_in = all_in
        self.bet = bet
        self.utg = utg
        self.first = first
        self.table = table

    def betting_round(self):
        """we need a round of betting.  Must appropriately tell players to act,
        create new pot, tell dealer to act, or if all but one player has folded
        award the pot to the remaining player and notify the table to start a
        new hand.
        """

        # if no community cards have been dealt
        # first to act(fta) is under the gun
        if not self.table.community_cards:
            fta = self.table.under_the_gun
        else:
            fta = self.first
        # set fta players action to True
        self.table.seats[fta].player.action = True
        # create an increment (next to act nta) to move the action
        # around the table
        nta = fta +1
        if nta == len(self.seats):
            nta = 0

