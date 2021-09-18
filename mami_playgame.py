"""
© 2020 Sara Arklint sara@arklint.dk

Play Mastermind (as code breaker) with random hidden code and any number of spaces and colors.
"""

from mami import calculate_key
from mami import make_code

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

 # Play Super Mastermind (with computer as code maker) with random guess
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
        for index in range(len(guesses)): # print previous guesses and keys
            print("Guess: {} (black pegs: {}, white pegs: {})".format(guesses[index],*keys[index]))
        guesses.append(guess)
        black, white = calculate_key(code, guess)
        keys.append([black, white])
        if black == pegs:
            print("Correct! You guessed that it was {} in {} attempts.".format(code, len(guesses)))
        else:
            print("Guess: {} (black pegs: {}, white pegs: {})".format(guess, black, white))

            
game()