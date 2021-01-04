#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
© 2020 Sara Arklint sara@arklint.dk

Mastermind with any number of spaces and colors.
The computer as code breaker against random hidden code or against all possible hidden codes.
Testing Knuth's 1976 algorithm.

"""

# For checking runtime:
import time
starttime = time.time()

# Make random hidden code for Mastermind
# default standard Mastermind with 4 spaces and 6 colors
def make_code(pegs = 4, colors = 6):
    import random
    code = []
    for space in range(pegs):
        code.append(random.randrange(colors))
    return code
    

# Calculate key (number of black and white pegs)
def calculate_key(code, guess):
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

# # Testing calculate_key 100 times:
# for i in range(100):
#     code = make_code(4,6)            
#     guess = make_code(4,6)
#     print("{} (code)\n{} (guess)".format(code, guess))
#     print("Black pegs: {}\nWhite pegs: {}\n".format(*calculate_key(code,guess)))
        



# Posssible keys ("replies")
def make_possible_keys(pegs=4, colors=6):
    possible_keys = []
    for black in range(pegs+1):
        for white in range(pegs+1):
            if black + white <= pegs and not (black == pegs - 1 and white == 1):
                possible_keys.append((black,white))
    return possible_keys


#print(make_possible_keys())

# Full sample space (i.e., what the hidden code may be at beginning of game)
def make_full_samplespace(pegs=4, colors=6):
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
    
# print(len(make_full_samplespace()))

# For testing:
# samplespace = make_full_samplespace()

# # check that we haven't made dublicates:
# for code in samplespace:
#     if samplespace.count(code) > 1:
#         print(code)

# # check that the result looks right:        
# print(samplespace)
# print(len(samplespace))

# For determining the best guess (using Knuth's algorithm)
# The function that for a given guess calculates the maximal error (i.e., size 
# of preimage of a given key) associated with it relative to a given samplespace:
def maximal_error(guess, samplespace, possible_keys):
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

# print(maximal_error(make_code(),samplespace, make_possible_keys()))

# The function that returns the best guess given a current samplespace
# using Knuth's algorithm
def best_guess(samplespace, full_samplespace, possible_keys):
    if len(samplespace) < 3:
        return samplespace[0]
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
        return result
    
# print(best_guess(samplespace, samplespace, make_possible_keys()))

# Updating a samplespace given a guess and the resulting key:
def update_samplespace(samplespace, guess, key):
    return [code for code in samplespace if calculate_key(code, guess) == key]

# print(update_samplespace(samplespace, make_code(), (3,0)))

def computer_as_codebreaker(hidden_code, first_guess, full_samplespace, possible_keys, pegs=4, colors=6):
    # full_samplespace = make_full_samplespace(pegs, colors)
    # possible_keys = make_possible_keys(pegs, colors)
    # hidden_code = make_code(pegs, colors)
    counter = 1
    guess = first_guess
    key = calculate_key(hidden_code, guess) # the code maker's reply
    black = key[0]
    samplespace = update_samplespace(full_samplespace, guess, key) # the code breaker's new possibilites
    while black < pegs:
        # print("Guess: {}\tKey: {}".format(guess, key))
        counter += 1
        guess = best_guess(samplespace, full_samplespace, possible_keys) # the code breaker's guess
        key = calculate_key(hidden_code, guess) # the code maker's reply
        black = key[0]
        samplespace = update_samplespace(samplespace, guess, key) # the code breaker's new possibilites
    # print("Code {} guessed in {} attempts.".format(code, counter))
    return counter

# Run game with computer as code breaker a given number of times with fixed number of pegs and colors
# against a random hidden code
# Returns maximum, minimum, and average
# Uses Knuth's algorithm
def test_game_randomized(tests, pegs=4, colors=6):
    full_samplespace = make_full_samplespace(pegs, colors)
    possible_keys = make_possible_keys(pegs, colors)
    first_guess = best_guess(full_samplespace, full_samplespace, possible_keys)
    maximum = 0
    minimum = float('inf')
    sum = 0
    for i in range(tests):
        times = computer_as_codebreaker(make_code(pegs, colors), first_guess, full_samplespace, possible_keys, pegs, colors)
        print("Pegs: {}, Colors: {}, Runtime (in seconds): {}".format(pegs, colors, time.time()-starttime))
        sum += times
        if times > maximum:
            maximum = times
        elif times < minimum:
            minimum = times
    return maximum, minimum, sum/tests

# Run through all possible hiden codes and return the maximal number of guesses needed for the code breaker
# Uses Knuth's algorithm
def find_maximum_number_of_guesses(pegs=4, colors=6):
    full_samplespace = make_full_samplespace(pegs, colors)
    possible_keys = make_possible_keys(pegs, colors)
    first_guess = best_guess(full_samplespace, full_samplespace, possible_keys)
    maximum = 0
    for code in full_samplespace:
        times = computer_as_codebreaker(code, first_guess, full_samplespace, possible_keys, pegs, colors)
        if times > maximum:
            maximum = times
    return maximum


if __name__ == '__main__': # so that it won't be executed when functions are imported in mami_playgame
    # Test the smaller game sizes and send the result to output file:    
    # with open('mami_output.txt','w') as output_file:
    #     for pegs in range(2,5,1):
    #         for colors in range(2,7,1):
    #             if pegs == 4 and colors == 6:
    #                 break
    #             else:
    #                 output_file.writelines("GAME\n{}\n{}\n{}\n".format(pegs, colors, find_maximum_number_of_guesses(pegs,colors)))
    #                 print("Pegs: {}, Colors: {}, Runtime (in seconds): {}".format(pegs, colors, time.time()-starttime))

    for pegs in range(2,5,1):
        for colors in range(2,7,1):
            print("Pegs: {}\tColors: {}\tMaximum: {}\tMinimum: {}\tAverage: {}".format(pegs,colors,*test_game_randomized(100,pegs,colors)))
    
    
    # Make table of result in output file for md file:
    # with open('mami_table.txt', 'w') as table_file:
    #     table_file.writelines("Pegs|Colors|Maximum\n---:|---:|---:")
    #     with open('mami_output.txt', 'r') as output_file:
    #         counter = 0
    #         for line in output_file.readlines():
    #             if line == "GAME\n":
    #                 table_file.writelines("\n")
    #             else:
    #                 counter += 1
    #                 table_file.writelines(line[:-1])
    #                 if counter % 3 == 0:
    #                     continue # table_file.writelines("\n")
    #                 else:
    #                     table_file.writelines("|")
                    
            
    print("Runtime (in seconds): {}".format(time.time()-starttime))
    