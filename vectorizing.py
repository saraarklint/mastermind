"""
© 2021 Sara Arklint sara@arklint.dk
Vectorized implementation (in NumPy) of Mastermind
"""
from mami import *
import numpy as np # for vectorizing
import time
starttime = time.time()

# This can be implemented better, but I don't think I'll ever use it
def make_code_vect(pegs=4, colors=6):
    """
    (int int) -> numpy.array
    
    Vectorization of make_code using NumPy
    Creates random hidden code for Mastermind
    Number of pegs and  colors is input (default pegs = 4, colors = 6)
    Returns NumPy array of shape (colors, pegs) with entries 0 or 1
    where a 1 in (r, c) interprets as peg no. r has color no. c.
    """
    code = np.zeros((colors,pegs), dtype=int)
    for peg in range(pegs):
        color = np.random.randint(0,colors)
        code[color,peg] = 1
    assert np.sum(code) == pegs
    return code
    
# I'm not sure I'll ever use this
def translate_from_vectorization(codes):
    """
    (numpy.array) -> numpy.array
    
    To help understanding/debugging vectorizations
    Translates m codes in the 0/1 format -- shape (m, colors, pegs)
    to m codes in format with enumerated colors -- shape (m, 1, pegs)
    Returns numpy array of shape (m, 1, pegs)
    
    >>> translate_from_vectorization(np.array([[[1, 0], [0, 0], [0, 1]],[[0, 0], [1, 1], [0, 0]]]))
    array([[[0, 2]],[[1, 1]]])
    """
    colors = codes.shape[1]
    # pegs = codes.shape[2]
    translation_matrix = np.arange(colors).reshape(1,colors,1)
    return np.sum(codes*translation_matrix, axis=1, keepdims=True)

# This can be implemented better, but I don't think I'll ever use it
def translate_to_vectorization(codes, colors=6):
    """
    (numpy.array int) -> numpy.array
    
    To help understanding/debugging vectorizations
    Translates m codes in format with enumerated colors -- shape (m, 1, pegs)
    to m codes in the 0/1 format -- shape (m, colors, pegs)
    Input numpy.array of shape (m, 1, pegs) and int giving no. of colors
    Returns numpy array of shape (m, colors, pegs)
    
    >>> translate_to_vectorization(np.array([[[0, 2]],[[1, 1]]]))
    array([[[1, 0], [0, 0], [0, 1]],[[0, 0], [1, 1], [0, 0]]])
    """
    pegs = codes.shape[2]
    assert np.max(codes) < colors
    reply = np.zeros((codes.shape[0],colors,pegs), dtype=int)
    for i in range(codes.shape[0]):
        for peg in range(pegs):
            reply[i, codes[i, 0, peg], peg] = 1
    return reply

def calculate_key_singular(code, guess):
    """
    input one code (ndarray shape (colors, pegs))
    input one guess (ndarray shape (colors, pegs))
    returns key encoded as black + white*(pegs+1)
    """
    assert code.shape == guess.shape
    pegs = code.shape[1]
    black = np.sum(code * guess) # black key pegs
    colors_code = np.sum(code, axis=1) # no. of pegs with each color (for code)
    colors_guess = np.sum(guess, axis=1) # no. of pegs with each color (for guess)
    blackwhite = np.sum(np.minimum(colors_code, colors_guess)) # sum of black and white key pegs
    white = blackwhite - black
    return black + white*(pegs+1)

def recover_key(number, pegs=4):
    """
    recovers key from encoding black + white*(pegs+1)
    input number
    output tuple with (black, white)
    """
    # assert type(number) == int
    # assert number >= 0
    # assert number <= pegs*(pegs+1)
    black = number % (pegs+1)
    white = number // (pegs+1)
    # assert black != (peg-1) OR white != 1
    # assert black + white < pegs+1
    return black, white

def calculate_key_black(codes, guesses):
    """
    input m codes (ndarray shape (m, colors, pegs))
    input n guesses (ndarray shape (n, colors, pegs))
    returns ndarray shape (m,n) with no. of black key pegs
    when pairing a code with a guess
    """
    assert codes.shape[1:] == guesses.shape[1:]
    # colors = codes.shape[1]
    # pegs = codes.shape[2]
    m = codes.shape[0]
    n = guesses.shape[0]
    matrix = (codes.reshape(m,1,-1)*guesses.reshape(1,n,-1)) # broadcasting
    return np.sum(matrix, axis=2)

def calculate_key_blackwhite(codes, guesses):
    """
    input m codes (ndarray shape (m, colors, pegs))
    input n guesses (ndarray shape (n, colors, pegs))
    returns ndarray shape (m,n) with no. of black or white key pegs
    (so sum of black and white pegs)
    when pairing a code with a guess
    """
    assert codes.shape[1:] == guesses.shape[1:]
    # colors = codes.shape[1]
    pegs = codes.shape[2]
    m = codes.shape[0]
    n = guesses.shape[0]
    matrix0 = np.sum(codes.reshape(-1, pegs), axis=1).reshape(m,1,-1)
    matrix1 = np.sum(guesses.reshape(-1, pegs), axis=1).reshape(1,n,-1)
    matrix = np.minimum(matrix0, matrix1) # broadcasting
    return np.sum(matrix, axis=2)

def calculate_key(codes, guesses):
    """
    input m codes (ndarray shape (m, colors, pegs))
    input n guesses (ndarray shape (n, colors, pegs))
    returns ndarray shape (m,n) with key
    when pairing a code with a guess
    and key encoded as black + white*(pegs+1)
    """
    assert codes.shape[1:] == guesses.shape[1:]
    pegs = codes.shape[2]
    black = calculate_key_black(codes, guesses)
    blackwhite = calculate_key_blackwhite(codes, guesses)
    # white = calculate_key_blackwhite(codes, guesses) - black
    return blackwhite*(pegs+1) - black*pegs # which is white*(pegs+1) + black

def number_to_vectorized_code(number, colors=6, pegs=4):
    """
    input number (should be in range(colors**pegs))
    returns ndarray shape (colors, pegs) with vectorized code
    number to code goes via colors-ary numbers
    cf. function vectorized_code_to_number
    """
    # code = np.zeros((1, 1, pegs), dtype=int)
    # assert type(number) == int
    assert number >= 0
    assert number < colors**pegs
    # numbercopy = number
    # for peg in range(pegs):
    #     code[:,:,peg] = numbercopy % colors
    #     numbercopy = numbercopy // colors
    # code = translate_to_vectorization(code, colors=colors).reshape(colors, pegs)
    # return code
    return np.fromfunction(lambda i,j: i == (number // (colors**j)) % colors,
                           (colors, pegs), dtype=int)

def make_possible_codes(colors=6, pegs=4):
    return np.fromfunction(lambda n,i,j: i == (n // (colors**j)) % colors,
                           (colors**pegs, colors, pegs), dtype=int)

def vectorized_code_to_number(code, colors=6):
    return code_to_number(vectorized_code_to_code(code), colors=colors)

def code_to_number(code, colors=6):
    assert code.shape[0] == 1
    assert np.max(code) < colors
    pegs = code.shape[1]
    translation_matrix = np.array([[colors]])**np.arange(pegs)
    return np.sum(code*translation_matrix)
    # number = 0
    # for peg in range(pegs):
    #     number += code[0,peg]*colors**peg
    # return number

def vectorized_code_to_code(code):
    colors = code.shape[0]
    # pegs = code.shape[1]
    translation_matrix = np.arange(colors).reshape(colors,1)
    return np.sum(code*translation_matrix, axis=0, keepdims=True).reshape(1,-1)

def max_error(number, colors=6, pegs=4):
    assert number < colors**pegs
    allcodes = make_possible_codes(colors, pegs)
    allkeys = calculate_key(allcodes, allcodes)
    max_error = np.max(np.unique(allkeys[number, :], return_counts=True)[1])
    return max_error


# code = make_code_vect()
# code1 = make_code_vect()
# guess = make_code_vect()
# guess1 = make_code_vect()
# guess2 = make_code_vect()
# codes = np.concatenate((code, code1))
# guesses = np.concatenate((guess, guess1, guess2))
# # assert np.sum(translate_to_vectorization(translate_from_vectorization(code))-code) == 0
# # print(codes)
# # print(guess)
# print(translate_from_vectorization(code))
# print(translate_from_vectorization(guess))
# print(calculate_key_vect(code, guess))

if __name__ == '__main__':

    # let's play a game...
    print("let's play a game")
    colors = 6
    pegs = 4
    # hiddencode = 441
    allcodes = make_possible_codes(colors, pegs)
    allkeys = calculate_key(allcodes, allcodes)
    allkeys_multidim = np.fromfunction(lambda n,m,i: i == allkeys[n,m],
                                       (colors**pegs, colors**pegs, pegs*(pegs+1)+1), dtype=int)
    maximalguesses = 0
    firstguess = np.argmin(np.max(np.sum(allkeys_multidim, axis=1), axis=1))
    verbose = False
    for hiddencode in range(colors**pegs):
        if verbose:
            print("\nhidden code:", vectorized_code_to_code(number_to_vectorized_code(hiddencode, colors, pegs)))
        attempt = 1
        if verbose:
            print("guess no. {}: {}".format(attempt, vectorized_code_to_code(number_to_vectorized_code(firstguess, colors, pegs))))
        key = allkeys[hiddencode, firstguess]
        if verbose:
            print("key no. {}: {}".format(attempt, recover_key(key)))
        possibilities = np.where(allkeys[:,firstguess] == key)[0]
        while key != pegs:
            attempt += 1
            if verbose:
                print("possibilities left: {}".format(possibilities.shape))
            if len(possibilities) <= 2:
                guess = possibilities[0]
            else:
                ixgrid = np.ix_(range(colors**pegs), possibilities, range(pegs*(pegs+1)+1)) # for restricting allkeys to possibilities
                ixgrid_onedim = np.ix_(possibilities) # for restricting maxerrors to possibilities
                errors = np.sum(allkeys_multidim[ixgrid], axis=1)
                maxerrors = np.max(errors, axis=1)
                guess = np.argmin(maxerrors) # first guess realizing min max error
                guess_poss = ixgrid_onedim[0][np.argmin(maxerrors[ixgrid_onedim])] # first guess realizing smallest max error amongst possibilities
                if maxerrors[guess] == maxerrors[guess_poss]: # check if the guess amongst possibilities realizes the min max error
                    guess = guess_poss
                # guesses = np.where(maxerrors == maxerrors.min())[0] # all guesses realizing min max error
                # guesses_poss = np.intersect1d(guesses, possibilities) # all possibilities realizes min max error
                # if len(guesses_poss) != 0: # if one of the possibilities realizes the min max error
                #     guess = guesses_poss[0] # use the first one of those as the guess instead
            if verbose:
                print("guess no. {}: {}".format(attempt, vectorized_code_to_code(number_to_vectorized_code(guess, colors, pegs))))
            key = allkeys[hiddencode, guess]
            if verbose:
                print("key no. {}: {}".format(attempt, recover_key(key)))
            possibilities = np.intersect1d(possibilities, np.where(allkeys[:,guess] == key)[0])
        if verbose:
            print("guessed in {} attempts".format(attempt))
        if attempt > maximalguesses:
            maximalguesses = attempt
        # if hiddencode % colors**2 == 0:
        #     print(hiddencode, attempt)
    print('maximal guesses: {}'.format(maximalguesses))
    print("Runtime (in seconds): {}".format(time.time() - starttime))
