__author__ = 'mark'
import random
from pot import Pot


class Table(object):
    """The table object will largely be the top level object

    Attributes:

        community_cards(list):  a list of the cards shared by all players
        seats(list):  list of seats in the game
        seats_active(int):  number of active seats
        small_blind_amount(int):  how much the small blind costs
        big_blind_amount(int):  how much the big blind costs
        ante(int):  how much the ante costs
        button(int):  indicates which seat has the button
        small_blind(int):  indicates which seat has the small blind (sub
                            of seat in self.seats)
        big_blind(int):  indicates which player has the big blind (sub of
                        seat in self.seats)
        under_the_gun(int):  first player to act pre-flop
        pots(list):  a list of all current pots
        dealer(obj):  the dealer object
        bought_button(obj):   will be the seat that bought the button, that
                            seat will pay the big and little blinds, the blinds
                            won't move for the following hand, and the small
                            blind will be utg

    Methods:

         init_hand: moves button to the next player.  Increments the
                    small_blind and big_blind attributes appropriately.  Resets
                    community_cards and pots to [].  Sets all player.hole
                    attributes []. Creates the initial pot object, deducts the
                    blinds and antes and adds them to the pot.pot. Pot inherits
                    the active seats, and button attributes as well as the
                    big_blind_amount as the initial pot.bet_increment value.
    """

    def __init__(self, seats, small_blind_amount, big_blind_amount, ante=0):
        self.community_cards = []
        self.seats = seats
        self.seats_active = 0
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        self.ante = ante
        self.button = 0
        self.small_blind = 0
        self.big_blind = 0
        self.under_the_gun = 0
        self.pots = []
        self.dealer = None
        self.bought_button = None

    def _get_active_seats(self):
        active_seat = []
        for seat in self.seats:
            if seat.active:
                active_seat.append(seat)
        return active_seat

    def set_button(self):
        """on start of game we need to randomly assign the button
        and blinds to an active seat"""
        self.button = random.randint(1, len(self.seats) - 1)
        self.seats_active = len(Table._get_active_seats(self))

        # check to make sure we've assigned the button to an active seat
        move = True
        for seat in self.seats:
            if seat.player:
                seat.player.missed_big_blind = False
                seat.player.missed_small_blind = False

        while move:
            if self.seats[self.button].active:
                move = False
            else:
                self.button += 1
                if self.button >= len(self.seats):
                    self.button = 0

        # set the small blind
        self.small_blind = self.button
        move = True
        while move:
            self.small_blind += 1
            if self.small_blind >= len(self.seats):
                self.small_blind = 0
            if self.seats[self.small_blind].active:
                move = False
            elif self.seats[self.small_blind].player:
                self.seats[self.small_blind].player.missed_small_blind = True

        # set the big blind
        self.big_blind = self.small_blind
        move = True
        while move:
            self.big_blind += 1
            if self.big_blind >= len(self.seats):
                self.big_blind = 0
            if self.seats[self.big_blind].active:
                move = False
            elif self.seats[self.big_blind].player:
                self.seats[self.big_blind].player.missed_big_blind = True

        # reset the blinds appropriately for head to head play
        active = Table._get_active_seats(self)
        if len(active) == 2:
            self.big_blind = self.small_blind
            self.small_blind = self.button

        # set utg (Under the Gun) for first round of betting (first to act)
        self.under_the_gun = self.big_blind
        move = True
        while move:

            self.under_the_gun += 1
            if self.under_the_gun >= len(self.seats):
                self.under_the_gun = 0
            if self.seats[self.under_the_gun].active:
                move = False

    def _reset_blinds(self):
        """ handles corner cases where a missed blind changes the blinds"""
        # if someone between s blind and button goes active they bought the blind
        count = self.button
        self.bought_button = None
        while count != self.small_blind:
            count += 1
            if count == len(self.seats):
                count = 0
            if self.seats[count].active:
                if self.bought_button is None:
                    self.bought_button = count
                    self.seats[count].player.missed_small_blind = False
                    self.seats[count].player.missed_big_blind = False
                else:
                    # only one player can buy the button at a time
                    self.seats[count].active = False
                    self.seats[count].player.frozen = True

        # the earliest active seat between the small and big becomes the big blind
        count = self.small_blind
        while count != self.big_blind:
            count += 1
            if count == len(self.seats):
                count = 0
            if self.seats[count].active:
                self.big_blind = count

    def _button_move(self):
        """moves the buttons and the blinds"""
        # exits game when down to a single player
        if self.seats_active == 1:
            quit()
        # correctly sets the small blind/button for head to head play
        elif self.seats_active == 2:
            move = True
            while move:
                self.big_blind += 1
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0
                if self.seats[self.big_blind].active:
                    move = False
            move = True
            while move:
                self.button += 1
                if self.button == self.big_blind:
                    self.button += 1
                if self.button >= len(self.seats):
                    self.button = 0
                if self.seats[self.button].active:
                    self.small_blind = self.button
                    self.under_the_gun = self.button
                    move = False

        # if one or more players join on a head to head game reset the button
        elif self.seats_active > 2 and self.button == self.small_blind:
            self.set_button()














        else:
            #ensures the button moves to the aprpriate seat
            move = True
            while move:
                self.button += 1
                # resets small_blind to 0 if it is greater than seats
                if self.button >= len(self.seats):
                    self.button = 0
                if self.seats[self.button].active:
                    # players that owe blinds can't play the button
                    if self.seats[self.button].player.missed_big_blind or self.seats[self.button].player.missed_small_blind:
                        self.seats[self.button].player.frozen = True
                        self.seats[self.button].active = False
                    else:
                        move = False

            # ensures that the small blind is moved to the appropriate seat
            move = True
            while move:
                self.small_blind += 1
                # resets small_blind to 0 if it is greater than seats
                if self.small_blind >= len(self.seats):
                    self.small_blind = 0
                # if seat is active ends the loop
                if self.seats[self.small_blind].active:
                    move = False
                elif not self.seats[self.small_blind].player.missed_big_blind:
                    self.seats[self.small_blind].player.missed_small_blind = True
                    move = False
                else:
                    self.seats[self.small_blind].player.missed_small_blind = True

            # ensures that the big blind is moved to the next active seat
            move = True
            while move:
                self.big_blind += 1
                # resets big_blind to 0 if it is greater than seats
                if self.big_blind >= len(self.seats):
                    self.big_blind = 0
                # if seat is active ends the loop
                if self.seats[self.big_blind].active:
                    self.seats[self.big_blind].missed_big_blind = False
                    self.seats[self.big_blind].missed_small_blind = False
                    move = False
                if not self.seats[self.big_blind].active:
                    self.seats[self.big_blind].player.missed_big_blind = True
                    self.seats[self.big_blind].player.missed_small_blind = False

            Table._reset_blinds(self)

            # if someone bought the button
            if self.bought_button:
                if self.seats[self.small_blind].active:
                    self.under_the_gun = self.small_blind
                else:
                    self.under_the_gun = self.big_blind

            else:
                # properly set utg
                move = True
                self.under_the_gun = self.big_blind
                while move:
                    self.under_the_gun += 1
                    # resets under_the_gun to 0 if it is greater than seats
                    if self.under_the_gun >= len(self.seats):
                        self.under_the_gun = 0
                    # if seat is active ends the loop
                    if self.seats[self.under_the_gun].active:
                        move = False

    def _create_pot(self):
        """creates the initial pot object with the blinds and antes"""
        bb = self.seats[self.big_blind]
        sb = self.seats[self.small_blind]
        all_in = []
        pot = 0

        # sets up first to act after the flop(sb unless head to head then bb)
        active_seats = Table._get_active_seats(self)
        if len(active_seats) == 2:
            first = self.big_blind
        else:
            first = self.small_blind

            # if active add the small blind to the pot
        if self.bought_button:
            buyer = self.seats[self.bought_button]
            buyer.player.missed_small_blind = False
            buyer.player.missed_big_blind = False
            if buyer.player.stack > self.small_blind_amount + self.big_blind_amount:
                buyer.player.equity = self.big_blind
                buyer.player.stack -= self.small_blind_amount + self.big_blind_amount
                pot += self.small_blind_amount + self.big_blind_amount

            elif buyer.player.stack >= self.big_blind_amount:
                buyer.player.equity = self.big_blind
                pot += buyer.player.stack
                buyer.player.stack = 0
                buyer.active = False
                all_in.append(buyer)
        elif sb.active:
            # if big blind was missed post it
            if sb.player.missed_big_blind:
                if sb.player.stack > self.small_blind_amount + self.big_blind_amount:
                    sb.player.stack -= self.small_blind_amount + self.big_blind_amount
                    pot += self.small_blind_amount + self.big_blind_amount
                    sb.player.equity = self.big_blind_amount
                    sb.player.missed_big_blind = False
                elif sb.player.stack > self.big_blind_amount:
                    pot += sb.player.stack
                    sb.player.stack = 0
                    sb.player.equity = self.big_blind_amount
                    sb.active = False
                    all_in.append(sb)
                    sb.player.missed_big_blind = False
                else:
                    pot += sb.player.stack
                    sb.player.equity = sb.player.stack
                    sb.player.stack = 0
                    sb.active = False
                    all_in.append(sb)
                    sb.player.missed_big_blind = False
            elif sb.player.stack > self.small_blind_amount:
                sb.player.stack -= self.small_blind_amount
                pot += self.small_blind_amount
                sb.player.equity = self.small_blind_amount
            # if small blind puts player all in put player in all_in list
            else:
                pot += sb.player.stack
                sb.player.equity = sb.player.stack
                sb.player.stack = 0
                sb.active = False
                all_in.append(sb)

        # add the big blind too the pot
        if not self.bought_button:
            if bb.player.stack > self.big_blind_amount:
                bb.player.stack -= self.big_blind_amount
                pot += self.big_blind_amount
                bb.player.equity = self.big_blind_amount
                bb.player.missed_big_blind = False
                # if big blind puts player all in put player in all_in list
            elif bb.player.stack <= self.big_blind_amount:
                pot += bb.player.stack
                bb.player.equity = bb.player.stack
                bb.player.stack = 0
                bb.active = False
                all_in.append(sb)
                bb.player.missed_big_blind = False

        # collect missing blinds from active seats
        for seat in active_seats:
            if seat.player.missed_big_blind:
                if seat.player.stack > self.big_blind:
                    seat.player.missed_big_blind = False
                    seat.player.stack -= self.big_blind_amount
                    seat.player.equity = self.big_blind_amount
                    pot += self.big_blind_amount
                else:
                    # if bb puts player all in set equity accordingly
                    # and set missed blinds to False
                    seat.player.equity = seat.player.stack
                    pot += seat.player.stack
                    seat.player.stack = 0
                    seat.active = False
                    all_in.append(seat)
                    seat.player.missed_small_blind = False
                    seat.player.missed_big_blind = False

            # rinse wash and repeat with missed small blinds
            if seat.player.missed_small_blind:
                if seat.player.stack > self.small_blind_amount:
                    seat.player.missed_small_blind = False
                    seat.player.stack -= self.small_blind_amount
                    pot += self.small_blind_amount
                    # pre-deal equity cannot exceed bb amount
                    if seat.player.equity == 0:
                        seat.player.equity = self.small_blind_amount
                else:
                    # if sb puts player all in set equity accordingly
                    # and set missed sb to False
                    if seat.player.equity == 0:
                        seat.player.equity = seat.player.stack
                    pot += seat.player.stack
                    seat.player.stack = 0
                    seat.active = False
                    all_in.append(seat)
                    seat.player.missed_small_blind = False

        # if there is an ante add it too the pot
        if self.ante > 0:
            for seat in active_seats:
                if seat.player.stack > self.ante:
                    seat.player.stack -= self.ante
                    pot += self.ante
                else:
                    # if ante puts player all in put player in all_in list
                    pot += seat.player.stack
                    seat.player.stack = 0
                    seat.active = False
                    if seat.player.equity > 0:
                        all_in.append(seat)

        # (pot, init_increment, increment, seats, all_in, bet, utg, first)
        pot = Pot(pot, self.big_blind_amount, self.big_blind_amount,
                  self.seats, all_in, self.big_blind_amount,
                  self.under_the_gun, first)
        self.pots = [pot]
        return pot

    def _reset_players(self):
        # set player attributes for start of new hand
        self.community_cards = []
        for seat in self.seats:
            if seat.player.frozen:
                seat.active = True
                seat.player.frozen = False
            if seat.player is not None:
                seat.player.hole = []
                seat.player.equity = 0

    def _remove_0_stack(self):
        """set seat to inactive for broke players"""
        for seat in self.seats:
            if seat.active and seat.player.stack == 0:
                seat.active = False

    def init_hand(self):
        """sets the table and players up for a new hand, creates a new pot,
        then calls the dealer """

        Table._reset_players(self)
        Table._remove_0_stack(self)
        Table._button_move(self)
        Table._create_pot(self)
        self.dealer.deal_hole()
