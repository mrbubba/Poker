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
        # are we in the middle of an active round of betting?
        # If so increment to the next active player
        for seat in self.seats:
            if seat.player.action:
                seat.player.action = False
                i = self.seats.index(seat)
                print("here we be", i, "seat ", seat.player.name)
                i += 1
                if i == len(self.seats):
                    i = 0
                    print(i)
                self.seats[i].player.action = True
                return

        # if no community cards have been dealt utg is first to act
        if not self.table.community_cards:
            self.seats[self.utg].player.action = True
        # if community cards then first is first to act.
        else:
            self.seats[self.first].player.action = True

    def betting_turn(self):
        action_moved = False
        for seat in self.seats:
            n = seat.player.name
            a = seat.player.action
            index = self.seats.index(seat)
            if a and not action_moved:
                seat.player.action = False
                index += 1
                if index == len(self.seats):
                    index = 0
                action_moved = True
                self.seats[index].player.action = True

            print("name={1} state={2} index={3}".format(len(self.seats), n, a, index))
