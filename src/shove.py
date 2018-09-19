from parse import parse 
from equity import run_simulation
from parallel import run_simulation_parallel
import argparse

def main():
    #a little hacky
    args = parse()
    if args['parallel']:
        del args['parallel']
        run_simulation_parallel(**args)
    else:
        del args['parallel']
        run_simulation(**args)

if __name__ == "__main__":
    main()