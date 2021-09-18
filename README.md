# mastermind
As a way of practicing my Python, I want to investigate effective algorithms for the codebreaker in generalized Mastermind,
i.e., Mastermind with *p* code pegs and *c* colors instead of 4 code pegs and 6 colors. So this is an ongoing project.

As a starting point, I have implemented Knuth's min-max algorithm from the article
 *The computer as master mind* in J. Recreation Mathematics (Vol. 9(1), 1976-77).
In the article, Knuth shows that for 4 pegs and 6 colors, his algorithm always finds the 
hidden code within 5 guesses.
One can show that 5 guesses are needed, i.e., that Knuth's algorithm is
optimal (wrt. maximum number of guesses).
A question then is whether Knuth's algorithm is optimal for other game dimensions (i.e., other numbers of pegs and colors), and if not how to improve on it.

## Don't know Mastermind?
In the standard game of 4 pegs and 6 colors, the game goes as follows:

1. The *codemaker* chooses a *hidden code* consisting of 4 pegs in order and of colors among the 6 colors (so there's $6^4 = 1296$ possibilities).
2. Then the *codebreaker* makes a *guess*, which is also 4 pegs in order and of colors among the 6 different colors.
3. The codemaker then replies with a *key*. See below for details on how the key is calculated from the hidden code and the guess.
4. 2.-3. continues until the codebreaker guesses the hidden code by using the information obtained from the received keys (and by guessing).

### Key
A *key* consists of 0-4 black and white *key pegs* that are *not* in order. 
The key describes how close the guess is to the hidden code:

* The number of *black* key pegs denotes the number of pegs in the guess of the same color and position as in the hidden code.
* The number of *white* key pegs denotes the number of pegs in the guess that have the right color but are in the wrong position when compared with the hidden code.

So the total number of black and white key pegs denotes the number of pegs in the hidden code that have the right color but are possibly in the wrong position.

Note that the key consisting of 3 black key pegs and 1 white key peg is invalid.

#### Example of calculating the key
* Hidden code: blue, blue, red, green
* Guess: red, red, blue, green (which is a great opening, btw)
* Key: 
    * 1 black key peg (1 for green in position 4)
    * 2 white key pegs (1 for blue in position *either* 1 or 2, plus 1 for red in position 3)

## Much faster implementation using NumPy
I've made two implementations of Knuth's algorithm, one using lists (which is `mami.py`) and a more recent one using NumPy ndarrays (which is `vectorizing.py`). The one in `mami.py` takes 16 minutes to run through all 1296 possible games in the standard game, while the one in `vectozing.py` does the same in 1 minute thanks to broadcasting (and by avoiding doing the same key calculation more than once).

The implementation using lists is rather intuitive, while the one using ndarrays relies on the following observations.

In a game with `colors` colors and `pegs` pegs, a code (hidden code or guess) is one-hot encoded as an ndarray of shape `(colors, pegs)`. The essential observations are then the following for 2 codes represented by ndarrays `X` and `Y`:

* `np.sum(X*Y)` gives the number of black pegs in the key calculated from `X` and `Y`,
* `np.sum(X, axis=1)` gives the number of pegs of each color for `X`,
* `np.sum(np.minimum(np.sum(X, axis=1), np.sum(Y, axis=1)))` gives the number of black and white pegs in the key calculated from `Y`.

I'll add more details on this implementation later. 

    
## Number of valid keys in generalized Mastermind
In a general game with $p$ pegs (and any non-trivial number of colors), the number of valid keys is $(p+1)(p+2)/2 - 1$, so 14 for the standard game.

One can count the number of valid keys by looking at the possible number of black key pegs separately.
With $b$ black key pegs, the allowed number of white key pegs is $0,1,\ldots, p-b$, but excluding the option with $p-1$ black key pegs and $1$ white:
$$ \left(\sum_{b=0}^p p-b+1\right) - 1
= \left( \sum_{n=1}^{p+1} n \right) -1 
= (p+1)(p+2)/2 - 1 $$

## Knuth's algorithm
One can think of a *guess* as a partitioning of the set of possible codes into one subset for each valid key (for the standard game, that's 14 subsets).
The *max error* of a guess is then the size of the largest subset in its partitioning.

To formalize:

* Let $K$ denote the set of valid key pegs. Then in the standard game, $K$ has 14 elements.
* Let $\kappa(c,g)$ denote the key calculated from code $c$ and guess $g$.
* Let $P_i$ denote the remaining possible codes at the beginning of the $i$th step.
Then $P_1$ consists of all possible codes (and is of size 1296 in the standard game),
and $P_{i+1} = \{ c\in P_i \mid \kappa(c,g_i) = k_i \}$ if $g_i$ is the guess made at the $i$th step and it's replied with key $k_i$.

Then we define the *max error* $\mu_i(g)$ of the guess $g$ at the $i$th step as:
$$ \mu_i(g) = \max_{k\in K} |\{ c\in P_i \mid \kappa(c,g) = k \}| $$

At step $i$, Knuth's algorithm chooses the next guess $g_i$ based on the current number of possible codes by choosing a guess that:

* Has the smallest max error among all 1296 codes.
That is, choose $g_i\in P_1$ such that $\mu_i(g_i)\leq\mu_i(g)$ for all $g\in P_1$.
Most likely, there are several to choose between.
* If possible, choose among the remaining possible codes.
That is, *if* such $g_i$ exists, choose $g_i\in P_i$ such that $\mu_i(g_i)\leq\mu_i(g)$ for all $g\in P_1$.
* However, if there are at most 2 remaining possible codes, then choose either of those.
That is, if $|P_i|\leq 2$, then choose $g_i\in P_i$ independently of $\mu_i$.

Note that Knuth's algorithm ensures $|P_{i+1}| \leq \mu_i(g_i)$.

Knuth's implementation (and mine) runs through the possible codes in lexicographical order, so all choices are made by choosing the option that's smallest lexicographically.

### Why is Knuth's algorithm optimal for the standard game?
For the standard game, one can run through all possible hidden codes (1296 in total) and check for each that when using Knuth's algorithm, the codebreaker guesses the hidden code with at most 5 guesses (and with 5 guesses for some hidden codes).

Now, Knuth's algorithm picks [0, 0, 1, 1]  as initial guess $g_1$, 
and this has the max error $\mu_1(g_1) = 256$.
What does this tell us? Consider a game following any strategy, and let $Q_i$ denote the remaining possible codes at the $i$th step (so before the codebreaker makes the $i$th guess $h_i$).
Assume that we are unlucky, which we actually could be, and $|Q_2| = \mu_1(h_1)$. Then at best, $|Q_2| = 256$.

For the remaining guesses, the ideal best we can do is making partitionings into subsets of equal size, i.e., achieving $|Q_{i+1}|\leq \lceil \frac{|Q_i|}{14} \rceil $ and with $|Q_{i+1}| = \lceil \frac{|Q_i|}{14} \rceil $ occuring when we're unlucky. If we keep being unlucky, this expands to $|Q_i| = \lceil \frac{|Q_2|}{14^{i-2}} \rceil$.
So even under these ideal conditions, the minimal number $n$ required to guarantee $|Q_n| = 1$ is $n=5$ as $14^3 = 196$, i.e., at least 5 guesses are needed.

### Lower bound for optimal algorithms for generalized Mastermind
For general Mastermind, let $\mu$ denote the max error of Knuth's algorithm's initial guess, and let $k$ denote the number of valid keys.
The crude analysis above tells us that any strategy requires at least $N$ guesses when $N$ denotes the smallest $n$ satisfying $ {k^{n-2}} \geq {\mu}$.

This does not that tell us that Knuth's algorithm isn't optimal in dimensions where it uses more than $N$ guesses. It just tells us that in those dimensions, it might not be optimal.


### Notes and comments on my first implementation of Knuth's algorithm
The first implementation `mami.py` uses lists to represent codes (hidden codes and guesses).

* The function `calculate_key` implements $\kappa$ specified above: it returns the *key* (number of black and white key pegs) given a *hidden code* and a *guess*. For debugging and for the fun of it, I've turned it into a game
where you play generalized Mastermind as codebreaker against the computer (with a randomized
hidden code). Run `mami_playgame.py` to play it.
* The function `best_guess` returns the best guess ($g_i$ above) given the set of remaining possibilities for the hidden
code (the `samplespace`, above $P_i$).
* The function `maximal_error` implements $\mu_i$ specified above: it calculates the maximal number of remaining possibilities after a given guess
and relative to the current samplespace $P_i$. It's used in `best_guess`.
* The function `computer_as_codebreaker` does one game simulation using Knuth's algorithm for 
the code breaker and with the hidden code as input. It returns the number of guesses it used, 
running it for all possible hidden codes (1296 for the standard game), one can check that
Knuth's algorithm in this case uses a maximum of 5 guesses.

My implementation is fast enough for playing against the computer, but way too slow when running `computer_as_codebreaker` for all possible hidden codes (almost 16 minutes for the standard game of 4 pegs and 6 colors (though I swear it was 2 minutes a couple of months ago), and 2 minutes in total for all the smaller games).
The initial implementation was made to be correct and not made to be fast, so this isn't really surprising.

## Investigating smaller game sizes
The table below describes the result of testing Knuth's algorithm on all possible hidden codes in smaller dimensions, i.e., $p\leq 4$ and $c\leq 6$. The coarse lower bound $N$ specified above is also included to compare with the number of guesses required by Knuth's algorithm. It's given me an idea for tweaking Knuth's algorithm, and I'll work on that later.

|Pegs|Colors|Guesses|Lower bound|Initial guess|Max error|Possible codes|Valid keys|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|2|2|3|3|[0, 0]|2|4|5|
|2|3|4|3|[0, 0]|4|9|5|
|2|4|4|4|[0, 1]|6|16|5|
|2|5|5|4|[0, 1]|9|25|5|
|2|6|5|4|[0, 1]|16|36|5|
|3|2|4|3|[0, 0, 0]|3|8|9|
|3|3|4|3|[0, 0, 1]|6|27|9|
|3|4|4|4|[0, 1, 2]|15|64|9|
|3|5|5|4|[0, 1, 2]|30|125|9|
|3|6|5|4|[0, 1, 2]|63|216|9|
|4|2|4|3|[0, 0, 0, 1]|4|16|14|
|4|3|4|4|[0, 0, 0, 1]|15|81|14|
|4|4|4|4|[0, 0, 1, 2]|46|256|14|
|4|5|5|4|[0, 0, 1, 1]|120|625|14|
|4|6|5|5|[0, 0, 1, 1]|256|1296|14|
