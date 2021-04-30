#!/usr/bin/env python

MAX_TICKERS = 5

def main():
    import time, sys
    from make_OI_data_as_needed import make_OI_data_for_top_gainers
    from make_OI_data_as_needed import make_OI_data_for_top_loser
    from make_OI_data_as_needed import make_OI_data_for_premarket
    t0 = time.time()
    if(len(sys.argv))==1:
        make_OI_data_for_premarket(MAX_TICKERS)
    else:
        argument = sys.argv[1]
        if argument == "-l":
            make_OI_data_for_top_loser()
        elif argument == "-g":
            make_OI_data_for_top_gainers()
        else:
            make_OI_data_for_premarket(MAX_TICKERS)
    t1 = time.time()
    t = t1 - t0
    print("Execution Time: ", t)

    
if __name__ == '__main__':
    main()
