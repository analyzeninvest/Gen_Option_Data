#!/usr/bin/env python


STOCK_UNIVERSE = [
    "INFY"
]

def main():
    import time
    from construct_OI_data import construct_OI_data_from_tickers
    t0 = time.time()
    pre_open = get_tickers_for_pre_open()
    construct_OI_data_from_tickers(pre_open)
    t1 = time.time()
    t = t1 - t0
    print("Execution Time: ", t)


def get_tickers_for_pre_open():
    from nsetools import Nse
    import pandas as pd
    nse = Nse()
    #all_stock_codes = nse.get_stock_codes()
    pre_moves = nse.get_preopen_nifty()
    list_of_tickers = []
    for item in pre_moves:
        list_of_tickers.append(item.get('symbol'))
    return(list_of_tickers)
    #print(len(all_stock_codes))
    

    
if __name__ == '__main__':
    main()
