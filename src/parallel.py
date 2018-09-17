import multiprocessing as mp  
import equity as utils
import constants

#TODO: investigate performance of using pipes instead of queues

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
    hand_hists = [[0]*len(constants.HANDS) for hand in hole_cards]
    win_hist = [0] * (len(hole_cards) + 1)
    i = 0
    while True:
        i += 1
        boards = input_queue.get()
        if not boards:
            break
        if not chunks:
            utils.update_simulation_state(hole_cards, boards, hand_hists, win_hist)
        else:
            for board in boards:
                utils.update_simulation_state(hole_cards, board, hand_hists, win_hist)
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

def run_simulation_parallel(hole_cards, board, chunks = False):
    start_time = utils.timeit.default_timer()
    deck = utils.generate_deck(hole_cards, board)
    input_queue = mp.Queue(maxsize = 100)
    output_queue = mp.Queue(maxsize = 4)
    pool = mp.Pool(4, initializer = process, initargs = (input_queue, output_queue, hole_cards, chunks))
    if not chunks:
        for board in utils.enumerate_boards(deck, len(board)):
            input_queue.put(board)
    else:
        generator = utils.enumerate_boards(deck, len(board))
        for boards in chunk_generator(generator, 1000):
            input_queue.put(boards)
    for _ in range(4):
        input_queue.put(None)
    pool.close()
    pool.join()
    hand_hists, win_hist = reduce_process_results(output_queue)
    win_perc, hand_perc = utils.calculate_equity(hand_hists, win_hist)
    end_time = utils.timeit.default_timer()
    print("time elapsed:", str(end_time - start_time))
    print(win_perc)
    print(hand_perc)
    
#should be roughly 87% in favor of aces
run_simulation_parallel([[(13, 'D'), (13, 'H')],[(2, 'S'), (7, 'H')]], [], True)