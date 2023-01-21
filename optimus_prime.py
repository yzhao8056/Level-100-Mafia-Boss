'''
cfr calc_strength bot

next step:
implement bluffing
1/3 of the time to bluff?
can't bluff bots are too smart

'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random 
import eval7

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.
        Arguments:
        Nothing.
        Returns:
        Nothing.
        '''
    
    def hole_list_to_key(self, hole):
        '''
        Converts a hole card list into a key that we can use to query our 
        strength dictionary
        hole: list - A list of two card strings in the engine's format (Kd, As, Th, 7d, etc.)
        '''

        card_1 = hole[0] # hole = list
        card_2 = hole[1] # card_# = str

        rank_1, suit_1 = card_1[0], card_1[1] # rank_# = char
        rank_2, suit_2 = card_2[0], card_2[1] # suit_# = char

        numeric_1, numeric_2 = self.rank_to_numeric(rank_1), self.rank_to_numeric(rank_2) # numerical

        suited = suit_1 == suit_2 # categorize
        suit_string = 's' if suited else 'o'

        if numeric_1 >= numeric_2: # keep hole cards in order
                return rank_1 + rank_2 + suit_string
        else:
            return rank_2 + rank_1 + suit_string
    
    def rank_to_numeric(self, rank):
        '''
        Method that converts our given rank as a string
        into an integer ranking
        rank: str - one of 'A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2'
        '''
        if rank.isnumeric(): # 2-9, value = self
            return int(rank)
        elif rank == 'T': # T = 10
            return 10
        elif rank == 'J': # J = 11
            return 11
        elif rank == 'Q': # Q = 12
            return 12
        elif rank == 'K': # K = 13
            return 13
        else: # A = 14 highest rank
            return 14

    def hole_strength(self, hole):
        '''
        strength of hole cards
        Args:
        hole - our hole card
        '''
        hole_strength_dictionary = {
        'AKs':0.6678,
        'AQs':0.6646,
        'AJs':0.6409,
        'ATs':0.64895,
        'A9s':0.6275,
        'A8s':0.61,
        'A7s':0.6159,
        'A6s':0.59625,
        'A5s':0.60255,
        'A4s':0.5969,
        'A3s':0.5873,
        'A2s':0.57515,
        'KQs':0.6324,
        'KJs':0.62645,
        'KTs':0.61005,
        'K9s':0.5992,
        'K8s':0.58885,
        'K7s':0.5815,
        'K6s':0.5695,
        'K5s':0.55735,
        'K4s':0.5428,
        'K3s':0.5356,
        'K2s':0.53525,
        'QJs':0.60695,
        'QTs':0.59225,
        'Q9s':0.5827,
        'Q8s':0.5644,
        'Q7s':0.5468,
        'Q6s':0.54325,
        'Q5s':0.5231,
        'Q4s':0.5105,
        'Q3s':0.50185,
        'Q2s':0.5092,
        'JTs':0.5745,
        'J9s':0.56065,
        'J8s':0.5446,
        'J7s':0.5296,
        'J6s':0.5031,
        'J5s':0.4945,
        'J4s':0.4925,
        'J3s':0.4826,
        'J2s':0.4785,
        'T9s':0.53945,
        'T8s':0.53055,
        'T7s':0.5064,
        'T6s':0.4927,
        'T5s':0.46915,
        'T4s':0.46645,
        'T3s':0.4651,
        'T2s':0.4432,
        '98s':0.51025,
        '97s':0.486,
        '96s':0.47295,
        '95s':0.45255,
        '94s':0.4369,
        '93s':0.43695,
        '92s':0.42405,
        '87s':0.4797,
        '86s':0.4605,
        '85s':0.44965,
        '84s':0.42615,
        '83s':0.4081,
        '82s':0.4007,
        '76s':0.4535,
        '75s':0.4427,
        '74s':0.42425,
        '73s':0.3969,
        '72s':0.38545,
        '65s':0.4331,
        '64s':0.4107,
        '63s':0.40625,
        '62s':0.3771,
        '54s':0.41715,
        '53s':0.3989,
        '52s':0.38365,
        '43s':0.38585,
        '42s':0.36995,
        '32s':0.3577,
        'AKo':0.6615,
        'AQo':0.63935,
        'AJo':0.63215,
        'ATo':0.6369,
        'A9o':0.6052,
        'A8o':0.58955,
        'A7o':0.58495,
        'A6o':0.57965,
        'A5o':0.57555,
        'A4o':0.56825,
        'A3o':0.561,
        'A2o':0.5468,
        'KQo':0.61225,
        'KJo':0.60565,
        'KTo':0.58485,
        'K9o':0.5796,
        'K8o':0.55725,
        'K7o':0.55635,
        'K6o':0.53585,
        'K5o':0.53475,
        'K4o':0.52785,
        'K3o':0.50945,
        'K2o':0.4991,
        'QJo':0.58255,
        'QTo':0.57175,
        'Q9o':0.556,
        'Q8o':0.53775,
        'Q7o':0.51935,
        'Q6o':0.51145,
        'Q5o':0.4926,
        'Q4o':0.49215,
        'Q3o':0.4735,
        'Q2o':0.4743,
        'JTo':0.5543,
        'J9o':0.5315,
        'J8o':0.5175,
        'J7o':0.49385,
        'J6o':0.4828,
        'J5o':0.4739,
        'J4o':0.46215,
        'J3o':0.45365,
        'J2o':0.44145,
        'T9o':0.51645,
        'T8o':0.49575,
        'T7o':0.47465,
        'T6o':0.4579,
        'T5o':0.44775,
        'T4o':0.4326,
        'T3o':0.42695,
        'T2o':0.4265,
        '98o':0.4857,
        '97o':0.45885,
        '96o':0.4492,
        '95o':0.42535,
        '94o':0.39865,
        '93o':0.4014,
        '92o':0.40565,
        '87o':0.4497,
        '86o':0.4446,
        '85o':0.4182,
        '84o':0.3899,
        '83o':0.3749,
        '82o':0.36255,
        '76o':0.4211,
        '75o':0.40305,
        '74o':0.3856,
        '73o':0.36165,
        '72o':0.34115,
        '65o':0.4036,
        '64o':0.3856,
        '63o':0.36045,
        '62o':0.3398,
        '54o':0.3789,
        '53o':0.3642,
        '52o':0.34345,
        '43o':0.3478,
        '42o':0.3407,
        '32o':0.32235,
        'AAo':0.85025,
        'KKo':0.8189,
        'QQo':0.80455,
        'JJo':0.77125,
        'TTo':0.75055,
        '99o':0.7095,
        '88o':0.6855,
        '77o':0.6537,
        '66o':0.63685,
        '55o':0.6063,
        '44o':0.57735,
        '33o':0.53335,
        '22o':0.49625
        }

        hole_strength = hole_strength_dictionary[self.hole_list_to_key(hole)] # inherent win probability
       
        return hole_strength


    def calc_strength(self, hole, iters, street_num, community = []):
        ''' 
        Using MC with iterations to evalute hand strength 
        Args: 
        hole - our hole carsd 
        iters - number of times we run MC 
        community - community cards

        '''

        deck = eval7.Deck() # deck of cards
        hole_cards = [eval7.Card(card) for card in hole] # our hole cards in eval7 friendly format


        # If the community cards are not empty, we need to remove them from the deck
        # because we don't want to draw them again in the MC
        if community != []:
            community_cards = [eval7.Card(card) for card in community]
            for card in community_cards: # removing the current community cards from the deck
                deck.cards.remove(card)

        for card in hole_cards: #r emoving our hole cards from the deck
            deck.cards.remove(card)
        
        # the score is the number of times we win, tie, or lose
        score = 0 

        for _ in range(iters): # MC the probability of winning
            deck.shuffle()

            # Let's see how many community cards we still need to draw
            if len(community) >= 5: # red river case
                # check the last community card to see if it is red
                if community[-1][1] == 'h' or community[-1][1] == 'd':
                    _COMM = 1
                else:
                    _COMM = 0
            else:
                _COMM = 5 - len(community) # number of community cards we need to draw 

            _OPP = 2 

            draw = deck.peek(_COMM + _OPP)  
            
            opp_hole = draw[:_OPP]
            alt_community = draw[_OPP:] # the community cards that we draw in the MC

            
            if community == []: # if there are no community cards, we only need to compare our hand to the opp hand
                our_hand = hole_cards + alt_community 
                opp_hand = opp_hole + alt_community

            else: 
                our_hand = hole_cards + community_cards + alt_community
                opp_hand = opp_hole + community_cards + alt_community


            our_hand_value = eval7.evaluate(our_hand)
            opp_hand_value = eval7.evaluate(opp_hand)

            if our_hand_value > opp_hand_value:
                score += 2 

            if our_hand_value == opp_hand_value:
                score += 1 

            else: 
                score += 0        

        mc_hand_strength = score/(2*iters) # real time simulation win probability 
        hole_hand_strength = self.hole_strength(hole)

        if street_num <= 5 and hole_hand_strength - mc_hand_strength >= 0.2: # hole probability only works in first five cards
            if mc_hand_strength >= 0.5: # monte carlo dynamic calculation knows more
                hand_strength = (mc_hand_strength + hole_hand_strength)/2 # tames simulation skew probability
            else:
                hand_strength = mc_hand_strength
        else:
            hand_strength = mc_hand_strength

        print('mc_hand_strength', mc_hand_strength)
        print('hole_hand_strength', hole_hand_strength)

        return hand_strength
    

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.
        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.
        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind


    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.
        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.
        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        my_cards = previous_state.hands[active]  # your cards
        opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
    

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.
        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.
        Returns:
        Your action.
        '''

        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        net_upper_raise_bound = round_state.raise_bounds()
        stacks = [my_stack, opp_stack] #keep track of our stacks

        my_action = None

        min_raise, max_raise = round_state.raise_bounds()
        pot_total = my_contribution + opp_contribution

        new_round = False

        if street < 3: # entering preflop signals new round
            new_round = True
            bluffing = False
            print('new game!')


        # raise logic 
        if street < 3: # preflop 
            raise_amount = int(my_pip + continue_cost + 0.4*(pot_total + continue_cost))
        else: # postflop
            raise_amount = int(my_pip + continue_cost + 0.75*(pot_total + continue_cost))

        if self.hole_strength(my_cards) > 0.6: # good hole cards 
            raise_amount = int(my_pip + continue_cost + 0.9*(pot_total + continue_cost))

        # ensure raises are legal
        raise_amount = max([min_raise, raise_amount]) # getting the max of the min raise and the raise amount
        raise_amount = min([max_raise, raise_amount]) # getting the min of the max raise and the raise amount
        # we want to do this so that we don't raise more than the max raise or less than the min raise

        if (RaiseAction in legal_actions and (raise_amount <= my_stack)):
            temp_action = RaiseAction(raise_amount)
        elif (CallAction in legal_actions and (continue_cost <= my_stack)):
            temp_action = CallAction()
        elif CheckAction in legal_actions:
            temp_action = CheckAction()
        else:
            temp_action = FoldAction() 

        _MONTE_CARLO_ITERS = 100
        
        # running monte carlo simulation when we have community cards vs when we don't 
        if street < 3:
            strength = self.calc_strength(my_cards, _MONTE_CARLO_ITERS, street)
        else:
            strength = self.calc_strength(my_cards, _MONTE_CARLO_ITERS, street, board_cards)

        # checks if the opponent might be bluffing
        if continue_cost > opp_contribution: # betting too much very sus
            if strength > 0.5 and random.random() < strength:
                return CallAction() # call their bluff

        if continue_cost > 0: # opponent raised
            _SCARY = 0
            if continue_cost > 6:
                _SCARY = 0.15
            if continue_cost > 15: 
                _SCARY = 0.25
            if continue_cost > 50: 
                _SCARY = 0.35

            strength = max(0, strength - _SCARY)
            pot_odds = continue_cost/(pot_total + continue_cost)

            if strength >= pot_odds: # nonnegative EV 
                if strength > 0.5 and random.random() < strength: 
                    my_action = temp_action
                    if strength > 0.95 and random.random() < strength: # if more than enough to win
                        raise_amount = my_stack # can also trick them into thinking that we're bluffing
                        raise_amount = max([min_raise, raise_amount]) 
                        raise_amount = min([max_raise, raise_amount])
                        return RaiseAction(raise_amount)
                else: 
                    my_action = CallAction()
            
            else: # negative EV
                # if street <= 3 and random.random() <= (1/3): # bluffing 1/3 of the time
                #     bluffing = True # once we're bluffing we continue to bluff
                #     raise_amount = my_stack # can also trick them into thinking that we're bluffing
                #     raise_amount = max([min_raise, raise_amount]) 
                #     raise_amount = min([max_raise, raise_amount])
                #     my_action = RaiseAction(raise_amount) # not all in to avoid suspicion

                #     print('blufffffffffffffffff')
                    
                # else: # folding 2/3 of the time
                my_action = FoldAction()
                
        else: # continue cost is 0  
            if random.random() < strength: 
                my_action = temp_action
            else: 
                my_action = CheckAction()

        return my_action
        


if __name__ == '__main__':
    run_bot(Player(), parse_args())