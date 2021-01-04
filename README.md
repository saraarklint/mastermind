# mastermind
I want to use Python to investigate effective algorithms for the codebreaker in generalized Mastermind, i.e., Mastermind with n code pegs of m colors (instead of 4 code pegs of 6 colors). 
## Step 1: `calculate_key`
Step 1 is implementing the calculation of the number of black and white pegs (key pegs) given a hidden code and a guess. For debugging and for the fun of it, I've turned it into a game where you play generalized Mastermind as codebreaker against the computer (with a randomized hidden code). Run mami_playgame.py to play it.
## Step 2: Implement Knuth's algorithm
I've implemented Knuth's algorithm from his 1976 paper *The computer as master mind* in J. Recreational Mathematics (Vol. 9(1), 1976-77). Knuth shows that for 4 pegs and 6 colors, his algorithm always finds the hidden code within 5 guesses. One can show that 5 guesses are needed, i.e., that Knuth's algorithm is optimal (wrt. maximum number of guesses). The question is whether Knuth's algorithm is optimal for other game sizes (numbers of pegs and colors).

The function `best_guess` returns the best next guess given the set of remaining possibilites for the hidden code (the `samplespace`), namely by choosing a guess (preferably in the samplespace) that *"minimizes the maximum number of remaining possibilites"* (except if there are only 1 or 2 possibilites left, in which case it chooses one of them). It uses the function `maximal_error` to calculate the maximal number of remaining possibilites after a given guess and relative to the current samplespace.
### Runtime...
Finding the initial best guess with Knuth's algorithm (which in this case is 0011), takes 4-5 seconds for the standard game of  4 pegs and 6 colors, and finding the hidden code then takes less than 1 second. So it makes sense to find the initial guess, and create the full range of possible codes (1296 in the standard game) and the set of possible keys (15 in the standard game), and then pass them on to the function `computer_as_codebreaker` which then does 1 game simulation, instead of including this in the game simulation as this is something we'll want to run a substantial number of times (e.g., 1296 times to run through all possible hidden codes in the standard game).
## Step 3: Investigating
It toke a bit more than 2 minutes to test all games smaller than the standard game:

Pegs|Colors|Maximum|Initial guess|Max error|Possibilites|Keys
---:|---:|---:|--:|--:|--:|--:
2|2|3|[0, 0]|2|4|5
2|3|4|[0, 0]|4|9|5
2|4|4|[0, 1]|6|16|5
2|5|5|[0, 1]|9|25|5
2|6|5|[0, 1]|16|36|5
3|2|4|[0, 0, 0]|3|8|9
3|3|4|[0, 0, 1]|6|27|9
3|4|4|[0, 1, 2]|15|64|9
3|5|5|[0, 1, 2]|30|125|9
3|6|5|[0, 1, 2]|63|216|9
4|2|4|[0, 0, 0, 1]|4|16|14
4|3|4|[0, 0, 0, 1]|15|81|14
4|4|4|[0, 0, 1, 2]|46|256|14
4|5|5|[0, 0, 1, 1]|120|625|14

It's not really these that we are interested in, but it's a great sandbox for testing if Knuth's algorithm is optimal. To be continued...