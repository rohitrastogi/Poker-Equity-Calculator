todos:
1) add report pretty print and timing
2) command line parsing
3) experiment with enumeration vs monte-carlo
4) potentially experiment multiprocessing?
5) hook this up to a simple webapp? If I do this, should I port the lib to JS or wrap the lib in a Flask API?


Findings so far:
- input: ([[(13, 'D'), (13, 'H')],[(2, 'S'), (7, 'H')]], []) -> (Aces vs 2/7 - 87% in favor of aces)
- monte-carlo time: .36 seconds
- exhaustive enumeration: ~ 40.75 seconds (main thread)
- parallelized exhaustive enumeration (w queue implementation) : 70.96 seconds (4 processes)
- chunked parallelized exhastive enumeration (w queue implementation : 22.49 seconds (4 processes)

why parallel version is slow? [FIXED]
- cannot map workers because exhaustive enumeration board function is a generator (don't want 48C5 boards stored in an array in memory)
- need to add board to a thread safe queue (producer/consumer)
- first thought: maybe queue.put() is slower than queue.get()? Doesn't seem this way - generated boards aren't big enough to be buffered 
- ISSUE: queue.get() is as slow as 0.002340253002330428 seconds. So in a sense, parallel.py is IO/bound 

potential solutions:
- use pipes (NOT VIABLE) - pipes are used can't be used for multiple consumers/workers
- find ways to chunk board generation and map workers (IMPLEMENTED)