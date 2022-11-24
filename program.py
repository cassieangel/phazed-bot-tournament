from phasetype import (accumulation_cards_34, check_order_sequence, 
                       phazed_phase_type, same_colour, same_colour_no_ace)
from validplay import (check_combination_is_in_hand, start_of_player_turn)
from itertools import combinations, permutations, product, cycle
from collections import defaultdict

def same_value(group):
    if len(group) > 1:
        # find the first value that is not a wild card    
        firstvalue = group[0][0]
        if firstvalue == "A":
            firstvalue = group[1][0]
        # check if card value is the same with the first value
        for card in group:
            value = card[0]           
            if value != firstvalue:
                if value != "A":
                    return False
        return True

def same_suit(group):
    if len(group) > 1:
        # find the first suit that is not a wild card
        for card in group:
            firstsuit = card[1]
            firstvalue = card[0]
            if firstvalue != "A":
                firstsuit = firstsuit
                break
        # check if card suit is the same with the first suit
        for card in group:
            suit = card[1]
            value = card[0]
            if suit != firstsuit:
                if value != "A":
                    return False
        return True

def group_can_be_in_sequence(group):
    # sort the group of cards according to values by "234567890JQKA"
    # change 0, K, A so that they sort accordingly
    group_cardtemp = []
    for val, suit in group:
        if val == "0":
            val = "B"
        if val == "K":
            val = "Y"
        if val == "A":
            val = "Z"
        group_cardtemp += ["".join(val + suit)]
    group_cardtemp.sort()
    # change back to original values
    group_card = []
    for card in group_cardtemp:
        val = card[0]
        suit = card[-1]
        if card[:-1] == "B":
            val = "0"
        if val == "Y":
            val = "K"    
        if val == "Z":
            val = "A"
        group_card += ["".join(val + suit)]  
    # check if the sorted group card is in sequence
    index = 0    
    for index in range(1, len(group_card)):
        # find the index where the sorted group card is no longer in sequence
        if check_order_sequence(group_card[:index]) is False:
            # if there is a wild card;
            if group_card[-1][0] == "A":
                # place wild card in between the cards that has 
                #  a break of the sequence
                group_card = (group_card[:(index - 1)] + [group_card[-1]] + 
                              group_card[(index - 1):-1])
    if check_order_sequence(group_card) is True:
        return group_card    
    if check_order_sequence(group_card) is not True:
        for i in range(9):
            # cycle around the group card and check if it is in sequence
            group_card = [group_card[-1]] + group_card[:-1]
            if check_order_sequence(group_card) is True:
                return group_card
    return False    

def sort_group(group):
    '''
    sort the group according to the values in the sequence of "234567890JQKA"
    '''
    # change 0, K, A so that they sort accordingly
    group_cardtemp = []
    for val, suit in group:
        if val == "0":
            val = "B"
        if val == "K":
            val = "Y"
        if val == "A":
            val = "Z"
        group_cardtemp += ["".join(val + suit)]
    group_cardtemp.sort()
    # change back to original values
    group_card = []
    for card in group_cardtemp:
        val = card[0]
        suit = card[-1]
        if card[:-1] == "B":
            val = "0"
        if val == "Y":
            val = "K"    
        if val == "Z":
            val = "A"
        group_card += ["".join(val + suit)]
    return group_card

def play_phase(hand, phase_status, player_id, discard):
    '''
    CHECK if a phase can be played with the cards in hand
    '''
    playing_phase_type = phase_status[player_id] + 1
    # PHASE TYPE 1
    if playing_phase_type == 1:
        all_same_val = []
        # find sets of cards that are the same values
        for group in combinations(hand, 3):
            if same_value(group) is True:
                all_same_val += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands           
        for twogroup in combinations(all_same_val, 2):  
            if check_combination_is_in_hand(hand, twogroup) is True:
                if 1 in phazed_phase_type(twogroup):
                    return True   
    # PHASE TYPE 2
    if playing_phase_type == 2:
        for onegroup in combinations(hand, 7):
            trialphase = [list(onegroup)]
            if 2 in phazed_phase_type(trialphase):
                return True
    # PHASE TYPE 3
    if playing_phase_type == 3:
        # find sets of cards that can form a total of 34
        all_34 = []
        for r in range(1, len(hand) + 1):            
            for group in combinations(hand, r):                
                if accumulation_cards_34(group) is True:
                    all_34 += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands          
        for twogroup in combinations(all_34, 2):   
            if check_combination_is_in_hand(hand, twogroup) is True:
                if 3 in phazed_phase_type(twogroup):
                    return True    
    # PHASE TYPE 4
    if playing_phase_type == 4:
        all_same_val = []
        # find sets of cards that are the same values
        for group in combinations(hand, 4):
            if same_value(group) is True:
                all_same_val += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands           
        for twogroup in combinations(all_same_val, 2):   
            if check_combination_is_in_hand(hand, twogroup) is True:
                if 4 in phazed_phase_type(twogroup):
                    return True   
    # PHASE TYPE 5
    if playing_phase_type == 5:
        for onegroup in combinations(hand, 8):
            if group_can_be_in_sequence(onegroup) is not False:
                trialphase = [list(group_can_be_in_sequence(onegroup))]
                if 5 in phazed_phase_type(trialphase):
                    return True       
    # PHASE TYPE 6
    if playing_phase_type == 6:
        # find sets of cards that can form a total of 34
        all_34 = []
        for r in range(1, len(hand) + 1):            
            for group in combinations(hand, r):                
                if accumulation_cards_34(group) is True:
                    all_34 += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands          
        for twogroup in combinations(all_34, 2):   
            if check_combination_is_in_hand(hand, twogroup) is True:
                # check if cards are of the same colouur in each group
                if 6 in phazed_phase_type(twogroup):
                    return True        
    # PHASE TYPE 7
    if playing_phase_type == 7:
        all_same_val = []
        # find sets of cards that are the same values
        for group in combinations(hand, 4):
            if same_value(group) is True:
                all_same_val += [list(group)]
        run_same_colour = []
        # find sets of cards that are the same colour and a run
        for group in combinations(hand, 4):
            if same_colour(group) is True:
                if group_can_be_in_sequence(group) is not False:
                    run_same_colour += [list(group_can_be_in_sequence(group))]
        # check if both sets are in hand
        for prod in product(run_same_colour, all_same_val):
            if check_combination_is_in_hand(hand, prod) is True:
                if 7 in phazed_phase_type(prod):
                    return True    
    return False     

def tally_hand_by_val(hand):
    ''' 
    return a dictionary with its key: card value, its value: tally
    '''
    hand_dict = defaultdict(int)
    for card in hand:
        value = card[0]
        hand_dict[value] = hand_dict[value] + 1
    return hand_dict

def tally_hand_by_suits(hand):
    ''' 
    return a dictionary with its key: card suit, its value: tally 
    '''
    hand_dict = defaultdict(int)
    for card in hand:
        suits = card[1]
        hand_dict[suits] = hand_dict[suits] + 1
    return hand_dict

def tallyby_colour_accumu(hand):
    ''' 
    return a dictionary with its key: card colour, its value: tally 
    '''
    hand_dict = defaultdict(int)
    for card in hand:
        suits = card[1]
        # convert card value into integers
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
        # tally into dictionary
        if suits in "SC":
            hand_dict["black"] = hand_dict["black"] + value
        if suits in "DH":
            hand_dict["red"] = hand_dict["red"] + value
    return hand_dict
    
def accumulation_cards_hand(hand):
    '''
    accumulate the sum of values of card in hand
    '''
    sum_values = 0
    for card in hand:
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

def take_discard_card(player_id, phase_status, hand, discard):
    ''' 
    CHECK if discard card can be useful to play the phase
    '''
    playing_phase_type = phase_status[player_id] + 1    
    # PHASE TYPE 1
    if playing_phase_type == 1:
        # pick up if it is an ace
        if discard[0] is "A":
            return True
        # check if discard card can help to form 3 cards of same value
        for value, tally in tally_hand_by_val(hand).items():
            if discard[0] == value and tally == 2:
                return True            
        # pick up discard card if tally of values are all less than 2 
        # or only one of them is 2, and discard value is in hands
        tally_dict = defaultdict(int)
        for tally in tally_hand_by_val(hand).values():
            tally_dict[tally] += 1
        if tally_dict[2] <= 1 and (discard[0] in 
                                   tally_hand_by_val(hand).keys()):
            return True       
    # PHASE TYPE 2
    if playing_phase_type == 2:
        # pick up if it is an ace
        if discard[0] is "A":
            return True
        # find suit that has most number of cards
        tally_suit = tally_hand_by_suits(hand).items()
        tally_suit_list = []
        for each in tally_suit:
            tally_suit_list += [each]
        sorted_tally_suit = sorted(tally_suit_list, key=lambda item: item[1])
        max_suit = sorted_tally_suit[-1][0]
        # if there is two or more suit that has most number of cards
        if sorted_tally_suit[-1][1] == sorted_tally_suit[-2][1]:
            max_suit += sorted_tally_suit[-2][0]
        # take if its suit is the suit that has most number of cards
        if discard[1] in max_suit:
            return True    
    # PHASE TYPE 3
    if playing_phase_type == 3:
        # if sum of values of cards is less than 34, pick up large value cards
        if accumulation_cards_hand(hand) < 34:
            if discard[0] in "890JQK":
                return True 
    # PHASE TYPE 4
    if playing_phase_type == 4:
        # pick up if it is an ace
        if discard[0] is "A":
            return True
        # check if discard card can help to form 4 cards of same value
        for value, tally in tally_hand_by_val(hand).items():
            if discard[0] == value and tally == 3:
                return True                   
        # find tally of tally of values 
        tally_dict = defaultdict(int)
        for tally in tally_hand_by_val(hand).values():
            tally_dict[tally] += 1
        # if there are less than 2 set of cards of 3
        if tally_dict[3] < 2:
            # check if there are set of cards of 2, and value is the same, 
            #  take discard card
            if tally_dict[2] > 0 and (tally_hand_by_val(hand)[discard[0]] 
                                                                      == 2):
                return True    
    # PHASE TYPE 5
    if playing_phase_type == 5:
        # pick up if it is an ace
        if discard[0] is "A":
            return True
        # pick up if value of discard is not in hand
        if discard[0] not in tally_hand_by_val(hand).keys():
            return True  
    # PHASE TYPE 6
    if playing_phase_type == 6:
        # group card in hand based on colour
        blackcards = []
        redcards = []
        for card in hand: 
            value = card[0]
            suit = card[1]
            if suit == "C" or suit == "S":
                blackcards += [card]
            if suit == "D" or suit == "H":
                redcards += [card]
        # if discard card is red
        if discard[1] == "H" or discard[1] == "D":
            if 10 < accumulation_cards_hand(redcards) < 24:
                if discard[0] in "890JKQ":
                    return True
            if 24 <= accumulation_cards_hand(redcards) < 34:
                if discard[0] in "234567":
                    return True
            # if both sets of cards is red
            if accumulation_cards_hand(redcards) >= 34:
                if discard[0] in "90JKQ":
                    return True
        # if discard card is black      
        if discard[1] == "C" or discard[1] == "S":
            if 10 < accumulation_cards_hand(blackcards) < 24:
                if discard[0] in "890JKQ":
                    return True
            if 24 <= accumulation_cards_hand(blackcards) < 34:
                if discard[0] in "234567":
                    return True
            # if both sets of cards is black
            if accumulation_cards_hand(blackcards) >= 34:
                if discard[0] in "90JKQ":
                    return True   
    # PHASE TYPE 7
    if playing_phase_type == 7:
        # pick up if it is an ace and hand tally ace is not more than 4
        if discard[0] is "A" and tally_hand_by_val(hand)["A"] > 4:
            return False
        # check if discard card can help to form 4 cards of same value
        for value, tally in tally_hand_by_val(hand).items():
            if discard[0] == value and tally == 3:
                return True 
        for value, tally in tally_hand_by_val(hand).items():
            if discard[0] == value and tally == 2:
                return True             
        # check if discard card can help to form a run of same colour
        # group card in hand based on colour
        blackcards = []
        redcards = []
        for card in hand: 
            value = card[0]
            suit = card[1]
            if suit == "C" or suit == "S":
                blackcards += [card]
            if suit == "D" or suit == "H":
                redcards += [card]
        # if discard card is black
        if discard[1] == "C" or discard[1] == "S":
            blackcards += [discard]
            for combicard in permutations(blackcards, 4):                
                if check_order_sequence(combicard) is True:
                    return True                     
        # if discard card is red
        if discard[1] == "H" or discard[1] == "D":
            redcards += [discard]
            for combicard in permutations(redcards, 4):                
                if check_order_sequence(combicard) is True:
                    return True 
    return False
            
def discard_on_table(player_id, table, discard, hand):
    ''' 
    CHECK if discard card can be put on table
    '''
    for phase, set_group in table:
        # PHASE 1
        if phase == 1:
            # check if discard card is the same value for each group
            for group in set_group:
                if same_value(group + [discard]) is True:
                    return True     
        # PHASE 2
        if phase == 2:
            # check if discard card is the same suit
            for group in set_group:
                if same_suit(group + [discard]) is True:
                    return True
        # PHASE 3
        if phase == 3:
            # check if discard card can add to form fibonacci sequence
            for group in set_group:
                # check the accumulation of cards in the group **not hands
                if accumulation_cards_hand(group) == 34:
                    if accumulation_cards_hand(hand + [discard]) == 21:
                        return True
                if accumulation_cards_hand(group) == 55:
                    if accumulation_cards_hand(hand + [discard]) == 13:
                        return True
                if accumulation_cards_hand(group) == 68:
                    if accumulation_cards_hand(hand + [discard]) == 8:
                        return True
                if accumulation_cards_hand(group) == 76:
                    if accumulation_cards_hand(hand + [discard]) == 5:
                        return True
                if accumulation_cards_hand(group) == 81:
                    if accumulation_cards_hand(hand + [discard]) == 3:
                        return True
                if accumulation_cards_hand(group) == 84:
                    if accumulation_cards_hand(hand + [discard]) == 2:
                        return True
                if accumulation_cards_hand(group) == 86:
                    if accumulation_cards_hand(hand + [discard]) == 1:
                        return True                
        # PHASE 4
        if phase == 4:
            # check if discard card is the same value for each group
            for group in set_group:
                if same_value(group + [discard]) is True:
                    return True 
        # PHASE 5
        if phase == 5:
            # check if discard card can be placed at the ends of the discard 
            for group in set_group:   
                if len(group) != 12:
                    if check_order_sequence(group + [discard]) is True:
                        return True
                    if check_order_sequence([discard] + group) is True:
                        return True
        # PHASE 6
        if phase == 6:            
            for group in set_group:
                # if discard card has same colour as the group
                if same_colour_no_ace(group + hand + [discard]) is True:
                    # check if discard card can add to form fibonacci sequence
                    # check the accumulation of cards in the group **not hands
                    if accumulation_cards_hand(group) == 34:
                        if accumulation_cards_hand(hand + [discard]) == 21:
                            return True
                    if accumulation_cards_hand(group) == 55:
                        if accumulation_cards_hand(hand + [discard]) == 13:
                            return True
                    if accumulation_cards_hand(group) == 68:
                        if accumulation_cards_hand(hand + [discard]) == 8:
                            return True
                    if accumulation_cards_hand(group) == 76:
                        if accumulation_cards_hand(hand + [discard]) == 5:
                            return True
                    if accumulation_cards_hand(group) == 81:
                        if accumulation_cards_hand(hand + [discard]) == 3:
                            return True
                    if accumulation_cards_hand(group) == 84:
                        if accumulation_cards_hand(hand + [discard]) == 2:
                            return True
                    if accumulation_cards_hand(group) == 86:
                        if accumulation_cards_hand(hand + [discard]) == 1:
                            return True  
        # PHASE 7
        if phase == 7:            
            for group in set_group:
                if same_value(group + [discard]) is True:
                    return True              
                if same_colour(group + [discard]) is True:
                    if len(group) != 12:
                        if check_order_sequence(group + [discard]) is True:
                            return True
                        if check_order_sequence([discard] + group) is True:
                            return True
    return False        

def return_phase(hand, phase_status, player_id):
    '''
    RETURN a phase with the current cards in hand
    '''
    playing_phase_type = phase_status[player_id] + 1
    # PHASE TYPE 1
    if playing_phase_type == 1:
        all_same_val = []
        # find sets of cards that are the same values
        for group in combinations(hand, 3):
            if same_value(group) is True:
                all_same_val += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands           
        for twogroup in combinations(all_same_val, 2):  
            if check_combination_is_in_hand(hand, twogroup) is True:
                if 1 in phazed_phase_type(twogroup):
                    return (1, list(twogroup))
    # PHASE TYPE 2
    if playing_phase_type == 2:
        for onegroup in combinations(hand, 7):
            trialphase = [list(onegroup)]
            if 2 in phazed_phase_type(trialphase):
                return (2, list(trialphase))
    # PHASE TYPE 3
    if playing_phase_type == 3:
        # find sets of cards that can form a total of 34
        all_34 = []
        for r in range(1, len(hand) + 1):            
            for group in combinations(hand, r):                
                if accumulation_cards_34(group) is True:
                    all_34 += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands          
        for twogroup in combinations(all_34, 2):   
            if check_combination_is_in_hand(hand, twogroup) is True:
                if 3 in phazed_phase_type(twogroup):
                    return (3, list(twogroup))
    # PHASE TYPE 4
    if playing_phase_type == 4:
        all_same_val = []
        # find sets of cards that are the same values
        for group in combinations(hand, 4):
            if same_value(group) is True:
                all_same_val += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands           
        for twogroup in combinations(all_same_val, 2):   
            if check_combination_is_in_hand(hand, twogroup) is True:
                if 4 in phazed_phase_type(twogroup):
                    return (4, list(twogroup))              
    # PHASE TYPE 5
    if playing_phase_type == 5:
        for onegroup in combinations(hand, 8):
            if group_can_be_in_sequence(onegroup) is not False:
                trialphase = [list(group_can_be_in_sequence(onegroup))]
                if 5 in phazed_phase_type(trialphase):
                    return (5, list(trialphase))       
    # PHASE TYPE 6
    if playing_phase_type == 6:
        # find sets of cards that can form a total of 34
        all_34 = []
        for r in range(1, len(hand) + 1):            
            for group in combinations(hand, r):                
                if accumulation_cards_34(group) is True:
                    all_34 += [list(group)]
        # combine 2 sets of cards and check if the cards are in hands          
        for twogroup in combinations(all_34, 2):   
            if check_combination_is_in_hand(hand, twogroup) is True:
                # check if cards are of the same colouur in each group
                if 6 in phazed_phase_type(twogroup):
                    return (6, list(twogroup))       
    # PHASE TYPE 7
    if playing_phase_type == 7:
        all_same_val = []
        # find sets of cards that are the same values
        for group in combinations(hand, 4):
            if same_value(group) is True:
                all_same_val += [list(group)]
        run_same_colour = []
        # find sets of cards that are the same colour and a run
        for group in combinations(hand, 4):
            if same_colour(group) is True:
                if group_can_be_in_sequence(group) is not False:
                    run_same_colour += [list(group_can_be_in_sequence(group))]
        # check if both sets are in hand
        for prod in product(run_same_colour, all_same_val):
            if check_combination_is_in_hand(hand, prod) is True:
                if 7 in phazed_phase_type(prod):
                    return (7, list(prod))        
    return False

def return_cards_on_table(player_id, table, hand):
    '''
    RETURN card from hand on table 
    '''
    for card in hand:
        table_player_id = 0
        # check for every table if it is possible to place card 
        for table_player in table:
            phase = table_player[0]
            set_group = table_player[1]
            # PHASE 1
            if phase == 1:
                # check if card is the same value for each group
                group_id = 0  # keep track of which group
                for group in set_group:
                    if same_value(group + [card]) is True:                        
                        return (card, (table_player_id, group_id, len(group)))
                    group_id += 1
            # PHASE 2
            if phase == 2:
                # check if card is the same suit
                group_id = 0 
                for group in set_group:
                    if same_suit(group + [card]) is True:
                        return (card, (table_player_id, group_id, len(group)))
                    group_id += 1
            # PHASE 3
            if phase == 3:
                # check if card can add to form fibonacci sequence
                group_id = 0 
                for group in set_group:
                    # check the accumulation of cards in the group **not hands
                    if accumulation_cards_hand(group) == 34:
                        if accumulation_cards_hand(hand) == 21:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    if accumulation_cards_hand(group) == 55:
                        if accumulation_cards_hand(hand) == 13:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    if accumulation_cards_hand(group) == 68:
                        if accumulation_cards_hand(hand) == 8:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    if accumulation_cards_hand(group) == 76:
                        if accumulation_cards_hand(hand) == 5:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    if accumulation_cards_hand(group) == 81:
                        if accumulation_cards_hand(hand) == 3:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    if accumulation_cards_hand(group) == 84:
                        if accumulation_cards_hand(hand) == 2:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    if accumulation_cards_hand(group) == 86:
                        if accumulation_cards_hand(hand) == 1:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                    group_id += 1
            # PHASE 4
            if phase == 4:
                # check if card is the same value for each group
                group_id = 0 
                for group in set_group:
                    if same_value(group + [card]) is True:
                        return (card, (table_player_id, group_id, len(group)))
                    group_id += 1
            # PHASE 5
            if phase == 5:
                # check if card can be placed at the ends of the discard 
                group_id = 0 
                for group in set_group:  
                    if len(group) != 12:
                        if check_order_sequence(group + [card]) is True:
                            return (card, (table_player_id, group_id, 
                                           len(group)))
                        if check_order_sequence([card] + group) is True:
                            return (card, (table_player_id, group_id, 0))
                    group_id += 1
            # PHASE 6
            if phase == 6:  
                group_id = 0 
                for group in set_group:                    
                    # if card has same colour as the group
                    if same_colour_no_ace(group + hand) is True:
                        # check if discard card can add to form 
                        #  fibonacci sequence
                        # check the accumulation of cards in the 
                        #  group **not hands
                        if accumulation_cards_hand(group) == 34:
                            if accumulation_cards_hand(hand) == 21:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                        if accumulation_cards_hand(group) == 55:
                            if accumulation_cards_hand(hand) == 13:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                        if accumulation_cards_hand(group) == 68:
                            if accumulation_cards_hand(hand) == 8:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                        if accumulation_cards_hand(group) == 76:
                            if accumulation_cards_hand(hand) == 5:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                        if accumulation_cards_hand(group) == 81:
                            if accumulation_cards_hand(hand) == 3:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                        if accumulation_cards_hand(group) == 84:
                            if accumulation_cards_hand(hand) == 2:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                        if accumulation_cards_hand(group) == 86:
                            if accumulation_cards_hand(hand) == 1:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                    group_id += 1 
            # PHASE 7
            if phase == 7:     
                group_id = 0 
                for group in set_group:
                    if same_value(group + [card]) is True:
                        return (card, (table_player_id, group_id, len(group)))                   
                    if same_colour(group + [card]) is True:
                        # if cards does not contain all value (if contain 
                        #  all cards: there will be 12 cards in the group)
                        if len(group) != 12:
                            if check_order_sequence(group + [card]) is True:
                                return (card, (table_player_id, group_id, 
                                               len(group)))
                            if check_order_sequence([card] + group) is True:
                                return (card, (table_player_id, group_id, 0))
                    group_id += 1                         
            table_player_id += 1            
    return False

def useless_card(hand, phase_status, player_id):
    playing_phase = phase_status[player_id] + 1
    # PHASE 1
    if playing_phase == 1:
        sort_hand = sort_group(hand)  # sort cards in order of values
        tally_val = list(tally_hand_by_val(sort_hand).items())
        # discard card with value is tally of 1
        for i in range(1, len(tally_val) + 1):            
            if tally_val[-i][0] != "A" and tally_val[-i][1] == 1:
                card_val = tally_val[-i][0]
                for card in sort_hand:
                    if card[0] == card_val:
                        play = (5, card)
                        return play
        # if cards were all tally of > 1; 
        for i in range(1, len(tally_val) + 1):     
            # discard card with tally of 2 and not wild card 
            if tally_val[-i][0] != "A" and tally_val[-i][1] == 2:
                card_val = tally_val[-i][0]  # highest value; since it's sorted
                for card in sort_hand:
                    if card[0] == card_val:
                        play = (5, card)
                        return play               
    # PHASE 2             
    if playing_phase == 2:
        sort_hand = sort_group(hand)
        # tally by suit; smallest num of cards in front of list
        tally_suit = sorted(list(tally_hand_by_suits(sort_hand).items()), 
                            key=lambda item: item[1])
        for i in range(len(tally_suit)):   
            # check within the smallest num of cards, remove card (if not ace);
            #  check the next smallest num of cards if it is ace on the first
            card_suit = tally_suit[i][0]
            for card in sort_hand:
                if card[1] == card_suit and card[0] != "A":
                    play = (5, card)
                    return play                
    # PHASE 3             
    if playing_phase == 3:
        # removes ace (as it is not a wild card)
        for card in hand:
            if card[0] == "A":
                play = (5, card)
                return play
        # find a set of 34
        set_34 = []
        for r in range(1, len(hand) + 1):            
            for group in combinations(hand, r):                
                if accumulation_cards_34(group) is True:
                    set_34 = list(group)
                    break
        # removes all card in set_34 from hand 
        for card in set_34:
            hand.remove(card)
        # removes smaller card (less helpful to complete accumulation of 34)
        sort_hand = sort_group(hand)
        card = sort_hand[0]
        play = (5, card)
        return play    
    # PHASE 4             
    if playing_phase == 4:
        sort_hand = sort_group(hand)
        tally_val = list(tally_hand_by_val(sort_hand).items())
        # removes card that has tally of 1 and not ace
        for i in range(1, len(tally_val) + 1):            
            if tally_val[-i][0] != "A" and tally_val[-i][1] == 1:
                card_val = tally_val[-i][0]
                for card in sort_hand:
                    if card[0] == card_val:
                        play = (5, card)
                        return play                   
        # if there is no cards of tally of 1, removes cards tally of 2            
        for i in range(1, len(tally_val) + 1): 
            if tally_val[-i][0] != "A" and tally_val[-i][1] == 2:
                card_val = tally_val[-i][0]
                for card in sort_hand:
                    if card[0] == card_val:
                        play = (5, card)
                        return play   
        # if there is no cards of tally of 1 or 2, removes cards tally of 3            
        for i in range(1, len(tally_val) + 1): 
            if tally_val[-i][0] != "A" and tally_val[-i][1] == 3:
                card_val = tally_val[-i][0]
                for card in sort_hand:
                    if card[0] == card_val:
                        play = (5, card)
                        return play                         
    # PHASE 5           
    if playing_phase == 5:
        # removes card of more than 1 card of the same value
        sort_hand = sort_group(hand) 
        tally_val = list(tally_hand_by_val(sort_hand).items()) 
        for i in range(1, len(tally_val) + 1):   
            # check the value of the card of the last tally of 
            #  values (highest value)
            card_val = tally_val[-i][0]
            for card in sort_hand:
                # if card value is the same, not wild and tally is more than 1
                if (card[0] == card_val and card[0] != "A" 
                                               and tally_val[-i][1] > 1):
                    play = (5, card)
                    return play               
    # PHASE 6
    if playing_phase == 6:
        # find a set of 34 with the same colour
        set_34_colour = []
        for r in range(1, len(hand) + 1):            
            for group in combinations(hand, r):                
                if accumulation_cards_34(group) is True:
                    if same_colour_no_ace(group) is True:
                        set_34_colour = list(group)
                        break
        # remove the set of 34 in hand                
        for card in set_34_colour:
            hand.remove(card)
        # removes card with different suit
        sort_hand = sort_group(hand)
        tally_suit = sorted(list(tallyby_colour_accumu(sort_hand).items()), 
                            key=lambda item: item[1])
        for i in range(len(tally_suit)):   
            # check within the least accumulation of card by colour
            card_suit = tally_suit[i][0]
            # sort remaining hand cards by value large to small
            sort_card_large_small = sort_hand[::-1] 
            for card in sort_card_large_small:
                if card[1] in "SC" and card_suit == "black":
                    play = (5, card)
                    return play 
                if card[1] in "DH" and card_suit == "red":
                    play = (5, card)
                    return play
    # PHASE 7
    if playing_phase == 7:
        # find a set of same value card (if >= 4 cards is not possible; 
        #  find a set of 3 2 or 1)
        same_val = []
        for r in range(1, len(hand) + 1):   
            # combinations of r number of cards
            for group in combinations(hand, r):       
                if same_value(group) is True:
                    same_val = list(group) 
                    break
        # remove the set of cards of same value from hand
        for card in same_val:
            hand.remove(card)
        run_same_colour = []
        # find a set of run with same colour at least 3
        for group in combinations(hand, 3):
            if same_colour(group) is True:
                if group_can_be_in_sequence(group) is not False:
                    run_same_colour = list(group)  
                    break  
        # remove the set of cards of same colour run from hand 
        for card in run_same_colour:
            hand.remove(card) 
        # discard card with less colour cards
        red = []
        black = []
        for card in hand:
            suit = card[1]
            if suit in "SC":
                red += [card]
            if suit in "HD":
                black += [card]
        # empty; all cards in run_same_colour or same_val
        if red == [] and black == []: 
            if same_val != []:
                play = (5, same_val[-1])
                return play
            if run_same_colour != []:
                play = (5, run_same_colour[-1])
                return play
        # if there are more red card;
        if len(red) >= len(black):
            if black != []:
                play = (5, black[-1])  # removes black card
                return play
            else:  # black cards is empty
                play = (5, red[-1]) 
                return play
        # if there are more black card;
        if len(black) >= len(red):
            if red != []:
                play = (5, red[-1])  # removes red card
                return play
            else:  # red cards is empty
                play = (5, black[-1]) 
                return play
        # if hand is empty (means all cards can be used 
        #  to form same value or samecolour run)
        if hand == []:
            discardcard = sort_group(same_val)[-1]  # discard largest val card
            play = (5, discardcard)
            return play
                
def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    '''
    The function takes 
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
    
    Return 2-tuple describing the single play your player wishes to make, 
        made up of a play ID and associated play content 
    '''  
    play = ()
    # START OF A PLAYER'S TURN
    if start_of_player_turn(player_id, turn_history) is True:
        # choose to pick up card from deck or discard pile        
        # if player has not completed the phase
        if table[player_id][0] is None:
            # check if discard card can help to complete the phase.
            hand += [discard]
            if play_phase(hand, phase_status, player_id, discard) is True:
                # pick up discard card 
                play = (2, discard)
                return play
            # check if discard card can be useful            
            hand = hand[:-1]
            if take_discard_card(player_id, phase_status, hand, 
                                                         discard) is True:
                play = (2, discard)
                return play
            else:
                play = (1, None)
                return play
            
        # if player had completed a phase      
        else: 
            if discard_on_table(player_id, table, discard, hand) is True:
                play = (2, discard)
                return play
            else:
                play = (1, None)
                return play
                          
    # NOT START OF PLAYER'S TURN
    else:
        # check if it is possible to play the phase
        if play_phase(hand, phase_status, player_id, discard) is not False:
            play = (3, return_phase(hand, phase_status, player_id))
            return play
        # not possible to play a phase
        else:
            # if player has completed a phase; time to put cards on table!! =D 
            if table[player_id][0] is not None:                                   
                # continuation of previous play to put cards on table 
                #  (phase 3 and 6; for accumulations of fibonacci numbers)
                for table_id in table:                    
                    if table_id[0] == 3 or table_id[0] == 6: 
                        table_groups = table_id[1]
                        for eachgroup in table_groups:
                            # if group in table is not "complete"
                            if accumulation_cards_hand(eachgroup) not in [34, 
                                                       55, 68, 76, 81, 84, 86]:
                                # put_in; previous play, placed on the phase of
                                #  (player, group, index posiition)
                                put_in = (turn_history[-1][-1][-1][-1][-1]) 
                                new_index = int(put_in[-1]) + 1
                                # new position (player, group, index posiition)
                                new_put_in = put_in[:2] + (new_index,)
                                play = (4, (hand[0], new_put_in))                    
                                return play
                # if cards is possible to place on table
                if return_cards_on_table(player_id, table, 
                                                     hand) is not False:
                    put_card_table = return_cards_on_table(player_id, 
                                                           table, hand)
                    play = (4, (put_card_table))
                    return play                
            # DISCARDING A CARD
                # discard largest value card, player has played a phase
                sort_hand = sort_group(hand)
                play = (5, sort_hand[-1])
                return play
            # discard useless card if player has not played a phase
            if table[player_id][0] is None:
                play = useless_card(hand, phase_status, player_id)
                return play            
    return play