from phasetype import (check_order_sequence, phazed_phase_type, 
                       same_colour, same_colour_no_ace)
from collections import defaultdict

def start_of_player_turn(player_id, turn_history):
    '''
    check if it is the start of a player's turn
    specifically, is going to pick up a card from deck or discard pile 
    '''
    if turn_history == []:
        return True
    previous_play_player = turn_history[-1][0]
    if player_id == 0:
        if previous_play_player != 3:
            return False
    if str(player_id) in "123":
        if previous_play_player != (player_id - 1):
            return False
    return True    

def accumulation_cards(phasecombi, position_on_group_phase):
    '''
    accumulate the sum of values in card of the group in the table
    '''
    sum_values = 0
    for card in phasecombi[position_on_group_phase]:
        value = card[0]
        if value in "23456789":   
            value = int(value)
        if value == "0":
            value = 10
        if value == "J": 
            value = 11
        if value == "Q": 
            value = 12
        if value == "K": 
            value = 13
        if value == "A": 
            value = 1
        sum_values += value
    return sum_values          

def value_of_card_attempt(card_attempt):
    '''
    find the value of the card that is going to be placed in group in the table
    '''
    value_card = card_attempt[0]
    if value_card in "23456789":   
        value_card = int(value_card)
    if value_card == "0":
        value_card = 10
    if value_card == "J": 
        value_card = 11
    if value_card == "Q": 
        value_card = 12
    if value_card == "K": 
        value_card = 13
    if value_card == "A": 
        value_card = 1
    return value_card

def valid_play_accumulation(card_attempt, phasecombi, position_on_group_phase):
    '''
    check if sum of cards in group and value of card attempting to place 
    is complete or less than the lowest value required to 
    complete the accumulation
    '''
    # sum of cards in group (accu_card_table)
    accu_card_table = accumulation_cards(phasecombi, position_on_group_phase)
    # value of card attempting to place (valu_card)
    valu_card = value_of_card_attempt(card_attempt)
    if accu_card_table == 34:
        if not (accu_card_table + valu_card <= 55):
            return False
    if 34 < accu_card_table <= 55:    
        if not (accu_card_table + valu_card <= 68):
            return False
    if 55 < accu_card_table <= 76:    
        if not (accu_card_table + valu_card <= 76):
            return False
    if 76 < accu_card_table <= 81:    
        if not (accu_card_table + valu_card <= 81):
            return False
    if 81 < accu_card_table <= 84:    
        if not (accu_card_table + valu_card <= 84):
            return False
    if 84 < accu_card_table <= 86:    
        if not (accu_card_table + valu_card <= 86):
            return False 
    return True

def place_single_card(play, table, hand):
    '''
    check if placing the single card is valid on the table
    '''
    card_attempt = play[1][0]
    position_on_player = play[1][1][0]
    position_on_group_phase = play[1][1][1]
    position_on_index = play[1][1][2]
    # check if card is in hand
    if card_attempt in hand:
        # check if position of card on player is valid
        if table[position_on_player][0] is not None:
            # check if position of card on the group and index position within 
            #  the phase is valid
            phasetype = table[position_on_player][0]
            phasecombi = table[position_on_player][1]
            # PHASE TYPE 1 or PHASE TYPE 4
            if phasetype == 1 or phasetype == 4:
                # find the first value in the group that is not a wild card    
                for card in phasecombi[position_on_group_phase]:
                    firstvalue = card[0]
                    if firstvalue != "A":
                        firstvalue = firstvalue
                # check if the card the player is attempting to play is valid 
                #  using the first value obtained                
                value_card_attempt = card_attempt[0]
                if firstvalue != value_card_attempt:
                    if value_card_attempt != "A":
                        return False
            # PHASE TYPE 2
            if phasetype == 2:
                # find the first suit in the group that is not a wild card    
                for card in phasecombi[position_on_group_phase]:
                    firstvalue = card[0]
                    firstsuit = card[1]
                    if firstvalue != "A":
                        firstsuit = firstsuit
                # check if the card the player is attempting to play is 
                #  valid using the first suit obtained
                suit_card_attempt = card_attempt[1]
                value_card_attempt = card_attempt[0]
                if firstsuit != suit_card_attempt:
                    if value_card_attempt != "A":
                        return False          
            # PHASE TYPE 3 
            if phasetype == 3:    
                if valid_play_accumulation(card_attempt, phasecombi, 
                                           position_on_group_phase) is False:
                    return False
            # PHASE TYPE 5
            if phasetype == 5:
                # add card into the group of cards accordingly
                group = phasecombi[position_on_group_phase]
                new_group = (group[:position_on_index] + [card_attempt] 
                             + group[position_on_index:])
                # check if new group is a run
                if check_order_sequence(new_group) is False:
                    return False
            # PHASE TYPE 6
            if phasetype == 6:
                # check if value of card is a valid play for accumulation
                if valid_play_accumulation(card_attempt, phasecombi, 
                                           position_on_group_phase) is True:
                    # check if card added to the group is the same colour
                    group = phasecombi[position_on_group_phase]
                    new_group = (group[:position_on_index] + [card_attempt] 
                                 + group[position_on_index:])
                    if same_colour_no_ace(new_group) is False:
                        return False
            # PHASE TYPE 7
            if phasetype == 7:
                # add card into the group of cards accordingly
                group = phasecombi[position_on_group_phase]
                new_group = (group[:position_on_index] + [card_attempt] 
                             + group[position_on_index:])
                # check if new group of card is a run of the same colour 
                if check_order_sequence(new_group) is True:
                    if same_colour(new_group) is False:
                        return False
                # check if new group of card is a set of cards of same value
                else:
                    # find the first value that is not a wild card    
                    firstvalue = new_group[0][0]
                    for card in new_group:
                        if firstvalue == "A":
                            firstvalue = card[0] 
                    # check if all values in group is the same
                    samevalue = True
                    for card in new_group:
                        value = card[0]           
                        if value != firstvalue:
                            if value != "A":
                                samevalue = False  
                    if samevalue is False:
                        return False                                   
    return True                 


def check_combination_is_in_hand(hand, combination):
    '''
    check if combination is in hand
    '''
    # generate dictionary for cards in hand
    hand_dict = defaultdict(int)
    for card in hand:
        hand_dict[card] = hand_dict[card] + 1
    # collect all cards in combination and generate a dictionary
    all_cards_combination = []
    all_cards_combination_dict = defaultdict(int)
    for set_of_card in combination:
        all_cards_combination += set_of_card
    for card in all_cards_combination:
        all_cards_combination_dict[card] = all_cards_combination_dict[card] + 1                
    # check if combination cards are in hand_dict
    for tally_cards in all_cards_combination_dict.items():
        if tally_cards not in hand_dict.items():
            return False    
    return True

def phazed_is_valid_play(play, player_id, table, turn_history, phase_status, 
                         hand, discard):           
    '''
    The function takes 
    play: A 2-tuple indicating the play type, and the content of the play
    player_id: An integer between 0 and 3 inclusive, indicating the ID of the 
        player attempting the play
    table: A 4-element list of phase plays for each of Players 0—3 respectively
    turn_history: A list of all turns in the hand to date, in sequence of play.
    phase_status: A 4-element list indicating the phases that each of 
        Players 0—3, respectively, have achieved in the game.
    hand: The list of cards that the current player holds in their hand, 
        each of which is in the form of a 2-element string.
    discard: The top card of the discard stack, in the form of a 2-element 
        string (e.g. '3D') or None in the case the discard pile is empty.
    
    Return True if play is valid relative to the current hand state, 
    and False otherwise. 
    '''  
    # if player plays Play 1
    if play[0] == 1:
        # check if it is the start of their turn
        if start_of_player_turn(player_id, turn_history) is True:
            return True
        
    # if player plays Play 2
    if play[0] == 2:
        # check if it is the start of their turn
        if start_of_player_turn(player_id, turn_history) is True:
            # check if pick up card is the same as the discarded card 
            if play[1] == discard:
                return True      
        
    # if player plays Play 3
    if play[0] == 3:
        # check if it is not the start of their turn 
        if start_of_player_turn(player_id, turn_history) is False:
            # check if player has not played a phase already in current hand
            if turn_history[0][0] != 3:                            
                phase_id = play[1][0]
                combination = play[1][1]
                # check if player's combination is in their hands            
                if check_combination_is_in_hand(hand, combination) is True:             
                    # check if player is playing the correct phase
                    if phase_id == phase_status[player_id] + 1:
                        # check if phase ID is the same as the combination 
                        #  phase type 
                        if phase_id in phazed_phase_type(combination):            
                            return True
    # if player plays Play 4
    if play[0] == 4:
        # check if it is not the start of their turn
        if start_of_player_turn(player_id, turn_history) is False:
            # check if card attempting to place is in their hands
            card_attempt = play[1][0]
            if card_attempt in hand:
                # check if player has played a phase already in current hand
                if phase_status[player_id] == table[player_id][0]:  
                    # check if card is valid to place to a phase on the table
                    if place_single_card(play, table, hand) is True:
                        return True   
    # if player plays Play 5
    if play[0] == 5:
        # check if it is not the start of their turn
        if start_of_player_turn(player_id, turn_history) is False:
            previous_player_discard = turn_history[-2][-1][-1]
            # check if discard is the same as play
            if previous_player_discard == play:
                return True                                        
    return False