todos:
1) add report pretty print and timing
2) command line parsing
3) experiment with enumeration vs monte-carlo
4) potentially experiment multiprocessing?
5) hook this up to a simple webapp? If I do this, should I port the lib to JS or wrap the lib in a Flask API?


Findings so far:
input: ([[(13, 'D'), (13, 'H')],[(2, 'S'), (7, 'H')]], []) -> (Aces vs 2/7 - 87% in favor of aces)
- monte-carlo time: .36 seconds
- exhaustive enumeration: ~ 40.75 seconds (main thread)
- parallelized exhaustive enumeration (w queue implementation) : 70.96 seconds (4 threads)

why parallel version is slow?
- cannot map workers because random board function is a generator
- need to add board to a thread safe queue (producer/consumer)
- queue.get() is as slow as 0.002340253002330428 seconds. So in a sense, parallel.py is IO/bound 

potential solutions:
- use pipes
- find ways to chunk board generation and map workers