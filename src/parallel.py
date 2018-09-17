import multiprocessing as mp  
import equity as utils
import constants

#TODO: investigate performance of using pipes instead of queues

def process(input_queue, output_queue, hole_cards):
    hand_hists = [[0]*len(constants.HANDS) for hand in hole_cards]
    win_hist = [0] * (len(hole_cards) + 1)
    i = 0
    while True:
        i += 1
        curr = utils.timeit.default_timer()
        board = input_queue.get()
        print(utils.timeit.default_timer() - curr)
        if not board:
            break
        utils.update_simulation_state(hole_cards, board, hand_hists, win_hist)
    print(i)
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

def run_simulation_parallel(hole_cards, board):
    start_time = utils.timeit.default_timer()
    deck = utils.generate_deck(hole_cards, board)
    #TODO: experiment with input_queue size relative to the number of processes
    #discover ratio of producer(generator)/consumer(equity calculation)
    input_queue = mp.Queue(maxsize = 100)
    output_queue = mp.Queue(maxsize = 4)
    pool = mp.Pool(4, initializer = process, initargs = (input_queue, output_queue, hole_cards))
    for board in utils.enumerate_boards(deck, len(board)):
        input_queue.put(board)
    for _ in range(1):
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
run_simulation_parallel([[(13, 'D'), (13, 'H')],[(2, 'S'), (7, 'H')]], [])

