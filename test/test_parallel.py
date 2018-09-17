import pytest
import time
import multiprocessing as mp
from itertools import islice
from parallel import reduce_process_results, chunk_generator

def test_reduce_process_results():
    q = mp.Queue()
    process_1_results = (
    [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6], 
    ],
    [2, 3, 4, 5])

    process_2_results = (
    [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6], 
    ],
    [2, 3, 4, 5])

    process_3_results = (
    [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6], 
    ],
    [2, 3, 4, 5])

    process_4_results = (
    [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6], 
    ],
    [2, 3, 4, 5])
    q.put(process_1_results)
    q.put(process_2_results)
    q.put(process_3_results)
    q.put(process_4_results)
    
    #sometimes puts are slower than execution of assert so test fails
    time.sleep(.1)

    results = (
    [
        [4, 8, 12, 16],
        [8, 12, 16, 20],
        [12, 16, 20, 24], 
    ],
    [8, 12, 16, 20])

    assert(reduce_process_results(q) == results)

def test_chunk_generator():
    def test_generator():
        for i in range(5, 0, -1):
            yield i
    assert(list(islice(chunk_generator(test_generator(), 2), 3)) == [[5, 4], [3, 2], [1]])

