# Shove

Shove is a command line utility to calculate poker hand equity written in Python. It uses Monte Carlo simulation and parallel processing to efficiently and accurately compute hand equity.

Shove can calculate hand equities for up to 10 players and works with or without a supplied board.

Run shove with `python3 src/shove.py -h`
```
Rohits-MBP-2:shove rohitrastogi$ python3 src/shove.py -h
usage: shove.py [-h] [--board [bc [bc ...]]] [--exact] [--verbose]
                [--parallel]
                [hc [hc ...]]

Calculate hand equity with supplied hole cards and optional board cards.

positional arguments:
  hc                    A list of all players' hole cards. Every player must
                        have two hole cards and you must supply cards for at
                        least players. Ex. Ad Ah 7c 2s

optional arguments:
  -h, --help            show this help message and exit
  --board [bc [bc ...]], --b [bc [bc ...]]
                        A list of all board cards. A supplied board may
                        include at most 4 cards.
  --exact, --e          Calculate hand equity exactly using exhaustive
                        enumeration. Note that exhasutive enumeration is
                        substantially slower than estimating hand equity using
                        Monte Carlo Simulation (default) and Monte Carlo
                        simulation is usually accurate within 1%.
  --verbose, --v        Receive detailed output on the probability of making
                        all possible Texas Hold'em hands.
  --parallel, --p       Parallelize hand equity computation over 4 workers.
                        Note that there is only a speed benefit of
                        parallelizing the computation if the --exact/e flag is
                        supplied, as Monte Carlo simulation is very fast on
                        the main thread.

```

Example #1: 2 players, no supplied board, Monte Carlo simulation, verbose
```
Rohits-MBP-2:shove rohitrastogi$ python3 src/shove.py Ad Ah 7c 2s --v
********************************************************************************
Time elapsed: 0.36046384200744797 seconds 

Player 1 Equity: 0.8738
Player 2 Equity: 0.1237
Chop: 0.0025

Player 1 Hand Probabilities:
High Card: 0.0
Pair: 0.3556
Two Pair: 0.4082
Three of a Kind: 0.1198
Straight: 0.0071
Flush: 0.0124
Full House: 0.0889
Four of a Kind: 0.0077
Straight Flush: 0.0002
Royal Flush: 0.0001

Player 2 Hand Probabilities:
High Card: 0.174
Pair: 0.4704
Two Pair: 0.2364
Three of a Kind: 0.0502
Straight: 0.0258
Flush: 0.019
Full House: 0.0211
Four of a Kind: 0.0016
Straight Flush: 0.0015
Royal Flush: 0.0
********************************************************************************
```

Example #2: 2 players, no supplied board, exhaustive enumeration (parallelized across 4 workers), verbose
```
********************************************************************************
Time elapsed: 24.58004917600192 seconds 

Player 1 Equity: 0.8745865220194545
Player 2 Equity: 0.12247883553387716
Chop: 0.0029346424466683485

Player 1 Hand Probabilities:
High Card: 0.0
Pair: 0.35738630523551895
Two Pair: 0.39967202085610964
Three of a Kind: 0.12624627402610752
Straight: 0.007490492342481242
Flush: 0.01428601463291565
Full House: 0.08551285285790373
Four of a Kind: 0.009122211943673554
Straight Flush: 0.00012848185836159933
Royal Flush: 0.00015534624692811557

Player 2 Hand Probabilities:
High Card: 0.1877505396238051
Pair: 0.45515282333043666
Two Pair: 0.23820536540240517
Three of a Kind: 0.047455358394303815
Straight: 0.02608999336566404
Flush: 0.019109924405946607
Full House: 0.024001579158840953
Four of a Kind: 0.0014133004419775927
Straight Flush: 0.0008047636401012904
Royal Flush: 1.635223651874901e-05
********************************************************************************
```

## Interesting things:
* Non-parallellized exhaustive enumeration run with the hole cards in the previous examples takes ~45 seconds. The parallelized version with 4 workers is roughly twice as fast.
* With 10000 iterations, the Monte Carlo simulation calculated hand equities are within .1 of the true equities calculated by enumeration. Monte Carlo simulation on a single process is  ~150x faster than exhasutive enumeration on a single process.
* Exhaustive enumeration becomes faster than Monte Carlo Simulation as the size of the supplied board increases and the number of players increase.
* I used generators in both the Monte Carlo and enumeration equity implementations to avoid storing up to 10000 sampled boards and up to 48C5 enumerated boards in memory. Because the boards were not stored in memory, I could not simply map a list of boards to a set of workers, making parallelization somewhat tricky. I used `Multiprocesing's` producer/consumer Queue to communicate between the workers. At first, I used the main process to add generated boards to the queue one-at-a-time, and the worker threads to process the generated boards. This solution was actually substantially slower than the non-parallelized exhaustive enumeration running on the main thread because of the overhead of passing messages. Specifically, get() operations in the producer/consumer queue were very slow. In my experiments, some get() operations took as long as 0.0025 seconds. To minimize the number of calls to get(), I 'batched' the generator and added lists of 1000 generated boards to the queue one at a time instead of individual boards. This allowed the workers to consume 1000 boards with 1 get() call, speeding the application up considerably.

## Todos:
* Extend Shove to take a range of cards as hole card input, instead of just 2 cards/
* ~20-25 seconds still seems slow for the parallelized exhaustive enumeration implementation. Is it possible to speed it up further?
* Extend Shove to distinguish between chopped pts between players when more than 2 player's hole cards are supplied.
* Extend Shove to dynamically choose between Monte Carlo simulation or Enumeration based on input.
* Create a React GUI to select cards (especially if range input is implemented). If I decide to do this, I can wrap this in a Flask API. Or, I could port this code to the browser since its not DB backed.