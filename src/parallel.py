import multiprocessing as mp  
from equity import update_simulation_state, generate_deck, enumerate_boards, calculate_equity, print_results, init_simulation_state
import constants
import timeit

def chunk_generator(generator, chunk_size = 1000):
    while True:
        res = None
        temp = []
        for _ in range(chunk_size):
            try: 
                temp.append(next(generator))
            except:
                yield temp
                raise StopIteration
        res = temp
        temp = []
        yield res 

def process(input_queue, output_queue, hole_cards, chunks):
    hand_hists, win_hist = init_simulation_state(hole_cards)
    while True:
        boards = input_queue.get()
        if not boards:
            break
        if not chunks:
            update_simulation_state(hole_cards, boards, hand_hists, win_hist)
        else:
            for board in boards:
                update_simulation_state(hole_cards, board, hand_hists, win_hist)
    output_queue.put((hand_hists, win_hist))

def reduce_process_results(queue):
    from functools import reduce
    queue_list = []
    while True:
        if queue.empty():
            break
        queue_list.append(queue.get())
    def helper(x, y):
        hand_hists1, win_hist1 = x[0], x[1]
        hand_hists2, win_hist2 = y[0], y[1]
        win_hist_sum = [first + second for first, second in zip(win_hist1, win_hist2)]
        hand_hists_sum = [[first + second for first, second in zip(hand_hists1[i], hand_hists2[i])] for i in range(len(hand_hists1))]
        return hand_hists_sum, win_hist_sum
    return reduce(helper, queue_list)

#chunks is either False or the number of chunks
def run_simulation_parallel(hole_cards, board, chunks = False, verbose = False):
    start_time = timeit.default_timer()
    deck = generate_deck(hole_cards, board)
    input_queue = mp.Queue(maxsize = 100)
    output_queue = mp.Queue(maxsize = constants.NUM_WORKERS)
    pool = mp.Pool(constants.NUM_WORKERS, initializer = process, initargs = (input_queue, output_queue, hole_cards, chunks))
    if not chunks:
        for board in enumerate_boards(deck, len(board)):
            input_queue.put(board)
    else:
        generator = enumerate_boards(deck, len(board))
        for boards in chunk_generator(generator, chunks):
            input_queue.put(boards)
    for _ in range(constants.NUM_WORKERS):
        input_queue.put(None)
    pool.close()
    pool.join()
    hand_hists, win_hist = reduce_process_results(output_queue)
    win_perc, hand_perc = calculate_equity(hand_hists, win_hist)
    end_time = timeit.default_timer()
    print_results(win_perc, hand_perc, end_time - start_time, verbose)