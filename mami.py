#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
© 2020 Sara Arklint sara@arklint.dk

Mastermind with any number of spaces and colors.
The computer as codebreaker against random hidden code or against all possible hidden codes.
Testing Knuth's 1976 algorithm.

"""

import json
# For checking runtime:
import time
starttime = time.time()

def make_code(pegs = 4, colors = 6):
    """
    (int int) -> lst
    
    Creates random hidden code for Mastermind
    Number of pegs and  colors is input (default pegs = 4, colors = 6)
    Returns list of length 'pegs' with items random numbers from 0 to 'colors'-1
    
    """
    import random
    code = []
    for space in range(pegs):
        code.append(random.randrange(colors))
    return code



def calculate_key(code, guess):
    """
    Calculate key (tuple) based on code and guess
    """
    black, white = 0, 0 # number of black and white pegs
    code_copy = code.copy() # make a copy so we can remove those that give pegs
    guess_copy = guess.copy() # do.
    # calculate number of black pegs:
    for index in range(len(code)): # run through the places in the hidden code
        if code[index] == guess[index]: # check for same color in same place
            code_copy.pop(index - black) # remove it so it won't give a white peg too,
            # remembering to adjust for code_copy being shorter than code
            guess_copy.pop(index - black) # mutatis mutandis
            black += 1
    # then calculate number of white pegs:
    for index in range(len(code_copy)):
    # run through the places in the hidden code that didn't give a black peg
        try:
            guess_copy.remove(code_copy[index]) # check if that color appears in the guess 
            # too, and remove it as it's now been paired up to give a white peg
            white += 1
        except ValueError:
            continue
    return black, white



def make_possible_keys(pegs=4, colors=6):
    """
    Given number of pegs and colors, returns posssible keys as list of tuples
    """
    possible_keys = []
    for black in range(pegs+1):
        for white in range(pegs+1):
            if black + white <= pegs and not (black == pegs - 1 and white == 1):
                possible_keys.append((black,white))
    return possible_keys



def make_full_samplespace(pegs=4, colors=6):
    """
    Given number of pegs and colors, returns full sample space as list of lists
    (i.e., what the hidden code may be at beginning of game)
    """
    # the samplespace will be constructed stepwise:
    # always with the right number of colors, but first with 0 pegs,
    # then 1 peg, then 2 pegs, then 3 pegs, etc.
    # make initial samplespace (corresponding to pegs = 1)
    samplespace = [[color] for color in range(colors)]
    # do while samplespace corresponds to too few pegs:
    while len(samplespace[0])< pegs:
        size = len(samplespace) # number of codes in current samplespace
        # increase current samplespace to one for 1 more number of pegs:
        for repeats in range(size): # do 'size' times, i.e., for each code in current samplespace
            code = samplespace.pop(0) # remove the (now) first code 
            for color in range(colors): #  make 'colors' new codes with one more peg
                # by adding the different colors at the end of the code and then adding them to the samplespace
                samplespace.append(code + [color])
    return samplespace
    

def maximal_error(guess, samplespace, possible_keys):
    """
    For determining the best guess (using Knuth's algorithm)
    The function that for a given guess calculates the maximal error (i.e., size 
    of preimage of a given key) associated with it relative to a given samplespace
    """
    maximum = 0
    partitioning = {key:0 for key in possible_keys}
    # for each possible key, we count the number of codes in samplespace that
    # is in the preimage of that key related to calculate_key(-,guess)
    for code in samplespace:
        partitioning[calculate_key(code,guess)] += 1
    # we find the key with the largest preimage:
    for key in possible_keys:
        maximum = max(maximum, partitioning[key])
    return maximum


def best_guess(samplespace, full_samplespace, possible_keys):
    """
    Returns the best guess given a current samplespace (using Knuth's algorithm)
    """
    if len(samplespace) < 3:
        return samplespace[0], None
    else:
        result = []
        max_error = float('inf')
        for guess in full_samplespace:
            error = maximal_error(guess, samplespace, possible_keys)
            if error < max_error:
                max_error = error
                result = guess
            elif error == max_error and guess in samplespace and result not in samplespace:
                result = guess
        return result, max_error

# def update_samplespace(samplespace, guess, key):
#     """
#     Updating a samplespace given a guess and the resulting key
#     """
#     return [code for code in samplespace if calculate_key(code, guess) == key]


def computer_as_codebreaker(hidden_code, first_guess, full_samplespace, possible_keys, pegs=4, colors=6):
    counter = 1
    guess = first_guess
    key = calculate_key(hidden_code, guess) # the codemaker's reply
    black = key[0]
    samplespace = [code for code in full_samplespace if calculate_key(code, guess) == key] # the codebreaker's new possibilites
    while black < pegs:
        # print("Guess: {}\tKey: {}".format(guess, key))
        counter += 1
        guess = best_guess(samplespace, full_samplespace, possible_keys)[0] # the codebreaker's guess
        key = calculate_key(hidden_code, guess) # the codemaker's reply
        black = key[0]
        samplespace = [code for code in samplespace if calculate_key(code, guess) == key] # the codebreaker's new possibilites
    # print("Code {} guessed in {} attempts.".format(hidden_code, counter))
    return counter

def test_game_randomized(tests, pegs=4, colors=6):
    """
    Run game with computer as code breaker a given number of times 
    with fixed number of pegs and colors against a random hidden code
    Returns maximum, minimum, and average
    Uses Knuth's algorithm
    """
    full_samplespace = make_full_samplespace(pegs, colors)
    possible_keys = make_possible_keys(pegs, colors)
    first_guess = best_guess(full_samplespace, full_samplespace, possible_keys)[0]
    maximum = 0
    minimum = float('inf')
    sum = 0
    for i in range(tests):
        times = computer_as_codebreaker(make_code(pegs, colors), first_guess, full_samplespace, possible_keys, pegs, colors)
        sum += times
        if times > maximum:
            maximum = times
        elif times < minimum:
            minimum = times
    return maximum, minimum, sum/tests

def find_maximum_number_of_guesses(pegs=4, colors=6):
    """
    Run through all possible hiden codes and return the maximal number of guesses needed 
    for the code breaker
    Uses Knuth's algorithm
    """
    result = {}
    full_samplespace = make_full_samplespace(pegs, colors)
    result['Possible codes'] = len(full_samplespace)
    possible_keys = make_possible_keys(pegs, colors)
    result['Valid keys'] = len(possible_keys)
    first_guess, max_error = best_guess(full_samplespace, full_samplespace, possible_keys)
    result['Initial guess'] = first_guess
    result['Max error'] = max_error
    guesses = 0
    for code in full_samplespace:
        times = computer_as_codebreaker(code, first_guess, full_samplespace, possible_keys, pegs, colors)
        if times > guesses:
            guesses = times
    result['Guesses'] = guesses
    return result
    
def find_lower_bound(max_error, pegs):
    """
    Returns coarse lower bound given initial guess's max error and number of pegs
    """
    valid_keys = (pegs+1)*(pegs+2)/2 - 1
    n = 1
    k = valid_keys
    while k < max_error:
        n += 1
        k *= valid_keys
    return n+2

def json_to_mdtable(headings, jsonlist):
    """
    Input list (with headings) plus list of dicts (data in json).
    Checks that headings are keys in the dicts,
    and returns string with md table of data sorted under specified headings.
    """
    for game in jsonlist:
        for heading in headings:
            if heading not in game:
                print('Issue with headings')
                return ''
    line = '|'
    for heading in headings:
        line += heading + '|'
    line += '\n'
    line += '|'
    for heading in headings:
        line += ':--:' + '|'
    line += '\n'
    for game in jsonlist:
        line += '|'
        for heading in headings:
            line += str(game[heading]) + '|'
        line += '\n'
    return line

    
# so that it won't be executed when functions are imported in mami_playgame
if __name__ == '__main__':
    
    
    # Test the smaller game sizes and send the result to output file:            
    categories = ['Pegs', 'Colors', 'Guesses', 'Initial guess', 'Max error', 
          'Possible codes', 'Valid keys', 'Lower bound', 'Knuth ok']
    results = []
    for pegs in range(2,5):
        for colors in range(2,7):
            print('Game: {} pegs, {} colors'.format(pegs, colors))
            game = find_maximum_number_of_guesses(pegs, colors)
            game['Pegs'] = pegs
            game['Colors'] = colors
            game['Lower bound'] = find_lower_bound(game['Max error'], pegs)
            game['Knuth ok'] = (game['Lower bound'] == game['Guesses'])
            results.append(game)
            print("Runtime (in seconds): {}".format(time.time()-starttime))    
    with open('mami_output.txt', 'w') as file:
        file.write(json.dumps(results))
    
    # # Make table of result in output file for md file:
    headings = ['Pegs', 'Colors', 'Guesses', 'Lower bound', 'Initial guess', 'Max error', 
                  'Possible codes', 'Valid keys']
    with open('mami_output.txt', 'r') as file:
        results = json.load(file)
        with open('mami_table.txt', 'w') as table_file:
            line = json_to_mdtable(headings, results)
            table_file.writelines(line)


    print("Runtime (in seconds): {}".format(time.time()-starttime))
    