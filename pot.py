__author__ = 'mark'

class Pot(object):
    """The pot object will drive and track the betting action for each round of
        play.

    Attributes:

        pot(int):   total amount of chips in the middle(another words all chips
                    not currently in player.stack)
        init_incriment(int):  bet incriment at the start of each betting round
        increment(int):  current bet increment for this round of betting
        bet(int):  the current bet
        side_pot(int):  the amount of chips in the current pot
        players(list):  list of players currently in the pot not all in
        all_in(list):  list of seats in the current pot that are all in


    methods:

        betting_round:  the main method of pot.  Will be called by dealer to
                        let pot know its time for a round of betting, dealer
                        will pass the initial better to the pot.
        set_action:     either sets player.action to true on the appropriate
                        player object, or calls dealer.deal
        set_bet_increment:  sets the bet_increment appropriately
    """

    def __init__(self, pot, init_incriment, incriment, players, all_in, bet):
        self.pot = pot
        self.init_incriment = init_incriment
        self.incriment = incriment
        self.players = players
        self.all_in = all_in
        self.bet = bet


