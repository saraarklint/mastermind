# mastermind
I want to use Python to investigate effective algorithms for the codebreaker in generalized Mastermind, i.e., Mastermind with n code pegs of m colors (instead of 4 code pegs of 6 colors). 
## Step 1: `calculate_key`
Step 1 is implementing the calculation of the number of black and white pegs (key pegs) given a hidden code and a guess. For debugging and for the fun of it, I've turned it into a game where you play generalized Mastermind as codebreaker against the computer (with a randomized hidden code). Run mami_playgame.py to play it.
## Step 2: Implement Knuth's algorithm
I've implemented Knuth's algorithm from his 1976 paper *The computer as master mind* in J. Recreational Mathematics (Vol. 9(1), 1976-77). Knuth shows that for 4 pegs and 6 colors, his algorithm always find the hidden code within 5 guesses. One can show that 5 guesses are needed, i.e., that Knuth's algorithm optimal (wrt. maximum number of guesses). The question is whether Knuth's algorithm is optimal for other game sized (numbers of pegs and colors).

The function `best_guess` returns the best next guess given the set of remaining possibilites for the hidden code (the `samplespace`), namely by choosing a guess (preferably in the samplespace) that *"minimizes the maximum number of remaining possibilites"* (except if there are only 1 or 2 possibilites left, in which case it chooses one of them). It uses the function `maximal_error` to calculate the maximal number of remaining possibilites after a given guess and relative to the current samplespace.
### Runtime...
Finding the initial best guess with Knuth's algorithm (which, is 0011), takes 4-5 seconds for the standard game of  4 pegs and 6 colors, and finding the hidden code then takes less than 1 second. Creating the full number of possible codes (1296 in the standard game), so it makes sense to find the initial guess, and create the full range of possible codes and the set of possible keys (15 in the standard game), and then pass them one to the function `computer_as_codebreaker` which then does 1 game simulation, instead of including this in the game simulation as this is something we'll want to run a substantial number of times (e.g., 1296 times to run through all possible hidden codes in the standard game).
## Step 3: Investigating
It toke a bit more than 2 minutes to test all games smaller than the standard game:

Pegs|Colors|Maximum
---:|---:|---:
2|2|3
2|3|4
2|4|4
2|5|5
2|6|5
3|2|4
3|3|4
3|4|4
3|5|5
3|6|5
4|2|4
4|3|4
4|4|4
4|5|5

It's not really these that we are interested in, but it's a great sandbox for testing if Knuth's algorithm is optimal. To be continued...