def no_of_natural_cards(group):
    '''
    find the number of natural cards in the group
    '''
    tally = 0
    for card in group:
        firstvalue = card[0]
        if firstvalue == "A":
            tally = tally
        else:
            tally += 1       
    return tally

def check_order_sequence(group):
    '''
    check if the cards in the group forms a sequence
    '''    
    correct_sequence = "234567890JQK234567890JQK"
    sequence = ""      
    # add first value to sequence
    firstvalue = group[0][0]
    # but.. if first value is a wild card; find the first value by moving
    #  backwards from the first natural card in the group              
    index = 0
    temp_correct_sequence = "234567890JQK234567890JQK"
    if firstvalue == "A":
        # take next card that is not wild as the 
        #  first value "current first value"
        for card in group:    
            firstvalue = card[0]
            index += 1  
            if firstvalue != "A":
                break    
        # if no first value found; means all wild cards
        if firstvalue == "A":
            return True
        # remove last value in temporary correct sequence if value is not 
        #  the "current first value"
        while temp_correct_sequence[-1] != firstvalue:
            temp_correct_sequence = temp_correct_sequence[:-1]
        if temp_correct_sequence[-1] == firstvalue:
            # find the real first value by moving backwards from 
            #  temporary correct sequence
            firstvalue = temp_correct_sequence[-index] 
    sequence += firstvalue                                                     
    # covert wild card's value (A) into the next value of previous card
    for card in group[1:]:
        value = card[0]
        if value == "A":
            if sequence[-1] in "2345678":
                value = str(int(sequence[-1]) + 1)
            elif sequence[-1] == "9":
                value = "0"
            elif sequence[-1] == "0":
                value = "J"
            elif sequence[-1] == "J":
                value = "Q"
            elif sequence[-1] == "Q":
                value = "K"
            elif sequence[-1] == "K":  
                value = "2"
            sequence += value
        else:
            sequence += value
    if sequence in correct_sequence:
        return True
    return False

def accumulation_cards_34(group):
    '''
    check if the accumulations of cards in the group is totalling to 34
    '''
    sum_values = 0
    for card in group:
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
    if sum_values == 34:
        return True
    return False

def same_colour(group):
    '''
    check if the cards in the group has the same colour (ACE is a wild card)
    '''
    if len(group) > 1:
        # change each card's suit into colour
        group_by_colour = []
        for card in group:
            value = card[0]
            suit = card[1]
            if suit == "S" or suit == "C":
                suit = "BLACK"                            
            if suit == "H" or suit == "D":
                suit = "RED"
            group_by_colour += [(value, suit), ]
        # find first colour that is not a wild card       
        firstcolour = group_by_colour[0][1]
        for card in group_by_colour:
            value = card[0]
            colour = card[1]
            if value != "A":
                firstcolour = colour
                break       
        # checking if group is the same colour
        samecolour = True
        for card in group_by_colour:            
            value = card[0]
            colour = card[1]
            if colour != firstcolour:
                if value != "A":
                    samecolour = False
        return samecolour

def same_colour_no_ace(group):
    '''
    check if the cards in the group has the same colour (ACE is not wild card)
    '''
    if len(group) > 1:
        # change each card's suit into colour
        group_by_colour = []
        for card in group:
            value = card[0]
            suit = card[1]
            if suit == "S" or suit == "C":
                suit = "BLACK"                            
            if suit == "H" or suit == "D":
                suit = "RED"
            group_by_colour += [(value, suit), ]
        # find first colour (first card)
        for card in group_by_colour:
            value = card[0]
            colour = card[1]
            firstcolour = colour
            break
        # checking if group is the same colour
        samecolour = True
        for card in group_by_colour:
            value = card[0]
            colour = card[1]
            if colour != firstcolour:
                samecolour = False
        return samecolour

def phazed_phase_type(phase):
    '''
    Takes a phase of combination of card groups in the form of a list of lists 
    of cards, where each card is a 2-character string with the value followed 
    by the suit
    
    Returns a sorted list composed of the values indicating the type(s) of the
    combinations of card groups contained in phase, with an invalid combination 
    indicated by the empty list.
    '''       
    # output list
    result = []
    
    # COMBINATION TYPE 1
    if len(phase) == 2:
        # tally the number of set that has three cards of the same value
        tally = 0
        for group in phase:
            if len(group) == 3:
                # find the first value that is not a wild card    
                firstvalue = group[0][0]
                if firstvalue == "A":
                    firstvalue = group[1][0]              
                # check if group have at least two "natural" cards 
                if no_of_natural_cards(group) >= 2:
                    # check if card value is the same with the first value                       
                    samevalue = True
                    for card in group:
                        value = card[0]           
                        if value != firstvalue:
                            if value != "A":
                                samevalue = False                                               
                    if samevalue is True:
                        tally += 1
        if tally == 2:
            result += [1]

    # COMBINATION TYPE 2
    if len(phase) == 1:
        group = phase[0]
        if len(group) == 7:
            # find the first suit that is not a wild card
            for card in group:
                firstsuit = card[1]
                firstvalue = card[0]
                if firstvalue != "A":
                    firstsuit = firstsuit
                    break
            # check if group have at least two "natural" cards 
            if no_of_natural_cards(group) >= 2:
                # check if card suit is the same with the first suit
                samesuit = True
                for card in group:
                    suit = card[1]
                    value = card[0]
                    if suit != firstsuit:
                        if value != "A":
                            samesuit = False
                if samesuit is True:
                    result += [2] 
                    
    # COMBINATION TYPE 3
    if len(phase) == 2:
        # tally the number of set that 34-accumulations
        tally = 0
        for group in phase:           
            if accumulation_cards_34(group) is True:
                tally += 1
        if tally == 2:
            result += [3] 
                
    # COMBINATION TYPE 4
    if len(phase) == 2:
        # tally the number of set that has four cards of the same value
        tally = 0
        for group in phase:
            if len(group) == 4:
                # find the first value that is not a wild card    
                firstvalue = group[0][0]
                for card in group:
                    if firstvalue == "A":
                        firstvalue = card[0]            
                # check if group have at least two "natural" cards 
                if no_of_natural_cards(group) >= 2:
                    # check if card value is the same with the first value                       
                    samevalue = True
                    for card in group:
                        value = card[0]           
                        if value != firstvalue:
                            if value != "A":
                                samevalue = False                                               
                    if samevalue is True:
                        tally += 1
        if tally == 2:
            result += [4]
    
    # COMBINATION TYPE 5
    if len(phase) == 1:
        group = phase[0]            
        if len(group) == 8:
            # check if group have at least two "natural" cards 
            if no_of_natural_cards(group) >= 2:      
                # check if group is in order
                if check_order_sequence(group) is True:
                    result += [5]   
            
    # COMBINATION TYPE 6
    if len(phase) == 2:
        # tally the number of set that has 34-accumulations of the same colour
        tally = 0
        for group in phase:            
            if accumulation_cards_34(group) is True:
                if same_colour_no_ace(group) is True: 
                    tally += 1 
        if tally == 2:
            result += [6]
            
    # COMBINATION TYPE 7
    if len(phase) == 2:     
        # check if group has 4 cards of same value
        tally_samevalue = 0
        for group in phase:
            if len(group) == 4:
                # find the first value that is not a wild card    
                firstvalue = group[0][0]
                for card in group:
                    if firstvalue == "A":
                        firstvalue = card[0]            
                # check if group have at least two "natural" cards 
                if no_of_natural_cards(group) >= 2:
                    # check if card value is the same with the first value                       
                    samevalue = True
                    for card in group:
                        value = card[0]           
                        if value != firstvalue:
                            if value != "A":
                                samevalue = False                                               
                    if samevalue is True:
                        tally_samevalue += 1
        # check if group has 4 cards of same colour
        tally_samecolour = 0
        for group in phase:
            if len(group) == 4:
                # check if group have at least two "natural" cards 
                if no_of_natural_cards(group) >= 2:      
                    # check if group is in order
                    if check_order_sequence(group) is True:
                        # checking if group is the same colour...
                        if same_colour(group) is True:
                            tally_samecolour += 1  
        if tally_samevalue == 1 and tally_samecolour == 1:
            result += [7]
    
    return result
