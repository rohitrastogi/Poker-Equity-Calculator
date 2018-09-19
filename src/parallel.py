import multiprocessing as mp  
import constants
import timeit
import equity 

def chunk_generator(generator, f, args, chunk_size = 1000):
    while True:
        res = None
        temp = []
        for _ in range(chunk_size):
            try: 
                curr = [next(generator)]
                temp.append(f(*(curr + args)))
            except:
                yield temp
                raise StopIteration
        res = temp
        temp = []
        yield res 

def process(input_queue, output_queue, hole_cards, chunks):
    hand_hists, win_hist = equity.init_simulation_state(hole_cards)
    while True:
        boards = input_queue.get()
        if not boards:
            break
        if not chunks:
            equity.update_simulation_state(hole_cards, boards, hand_hists, win_hist)
        else:
            for board in boards:
                equity.update_simulation_state(hole_cards, board, hand_hists, win_hist)
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

def run_simulation_parallel(hole_cards = None, board = None, exact = False, chunks = True, verbose = False):
    boards = None
    if not hole_cards and not board:
        raise ValueError('Supply hole_cards and board lists.')
    start_time = timeit.default_timer()
    deck = equity.generate_deck(hole_cards, board)
    input_queue = mp.Queue(maxsize = 100)
    output_queue = mp.Queue(maxsize = constants.NUM_WORKERS)
    pool = mp.Pool(constants.NUM_WORKERS, initializer = process, initargs = (input_queue, output_queue, hole_cards, chunks))
    if exact and chunks:
        generator = equity.enumerate_boards(deck, len(board))
        for boards_chunk in chunk_generator(generator, equity.combine_board, [board]):
            input_queue.put(boards_chunk)
    elif exact and not chunks:
        boards = equity.enumerate_boards(deck, len(board))
    elif not exact and chunks:
        generator = equity.sample_boards(deck, len(board))
        for boards_chunk in chunk_generator(generator, equity.combine_board, [board]):
            input_queue.put(boards_chunk)
    else:
        boards = equity.sample_boards(deck, len(board))
    if boards:
        for gen_board in boards:
            print(equity.combine_board(gen_board, board))
            input_queue.put(equity.combine_board(gen_board, board))
    for _ in range(constants.NUM_WORKERS):
        #poison pill
        input_queue.put(None)
    pool.close()
    pool.join()
    hand_hists, win_hist = reduce_process_results(output_queue)
    win_perc, hand_perc = equity.calculate_equity(hand_hists, win_hist)
    end_time = timeit.default_timer()
    equity.print_results(win_perc, hand_perc, end_time - start_time, verbose)