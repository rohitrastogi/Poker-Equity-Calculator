import pytest
import parallel as util

def test_reduce_process_results():
    q = util.mp.Queue()
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
    q.put(None)

    results = (
    [
        [4, 8, 12, 16],
        [8, 12, 16, 20],
        [12, 16, 20, 24], 
    ],
    [8, 12, 16, 20])

    assert(util.reduce_process_results(q) == results)
