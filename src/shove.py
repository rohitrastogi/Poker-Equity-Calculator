from parse import parse
import equity
import parallel

def main():
    #a little hacky
    args = parse()
    if args.p:
        del args[p]
        parallel.run_simulation_parallel(**args)
    else:
        del args[p]
        equity.run_simulation(**args)

if __name__ == "__main__":
    main()