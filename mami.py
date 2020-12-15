#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 13:36:38 2020

@author: sara

Play Super Mastermind with random clue and any number of spaces and colors.
"""

# Make random hidden code for Super Mastermind
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
        

# Prompt for guess
def get_guess(pegs = 4, colors = 6):
    allowed = [str(number) for number in list(range(colors))]
    reply = "no"
    while not reply == "":
        guess = []
        counter = 0
        while len(guess) < pegs:
            number = input("Type the color (number between 0 and {colors}) of peg no. {peg}: ".format(peg = counter + 1, colors = colors - 1))
            if number in allowed:
                guess.append(int(number))
                counter += 1
            else:
                print("That's not a number between 0 and {}!".format(colors-1))
        reply = input("Your guess: {}. Hit enter if correct; type anything otherwise.".format(guess))
    return guess

 # Play Super Mastermind with random guess
def game():
    pegs = int(input("Type the number of pegs: "))
    colors = int(input("Type the number of colors: "))
    code = make_code(pegs,colors)
    black = 0
    guesses = []
    keys = []
    while black < pegs:
        guess = get_guess(pegs, colors)
        print("Your guesses:")
        for index in range(len(guesses)): # print previous guesses and replies
            print("Guess: {} (black pegs: {}, white pegs: {})".format(guesses[index],*keys[index]))
        guesses.append(guess)
        black, white = calculate_key(code, guess)
        keys.append([black, white])
        if black == pegs:
            print("Correct! You guessed that it was {} in {} attempts.".format(code, len(guesses)))
        else:
            print("Guess: {} (black pegs: {}, white pegs: {})".format(guess, black, white))

            
game()

    
    
    
    
    