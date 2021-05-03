#!/usr/bin/env python

STOCK_OPTION_UNIVERSE = [
    "AARTIIND",
    "ACC",
    "ADANIENT",
    "ADANIPORTS",
    "ALKEM",
    "AMARAJABAT",
    "AMBUJACEM",
    "APLLTD",
    "APOLLOHOSP",
    "APOLLOTYRE",
    "ASHOKLEY",
    "ASIANPAINT",
    "AUBANK",
    "AUROPHARMA",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJAJFINSV",
    "BAJFINANCE",
    "BALKRISIND",
    "BANDHANBNK",
    "BANKBARODA",
    "BATAINDIA",
    "BEL",
    "BERGEPAINT",
    "BHARATFORG",
    "BHARTIARTL",
    "BHEL",
    "BIOCON",
    "BOSCHLTD",
    "BPCL",
    "BRITANNIA",
    "CADILAHC",
    "CANBK",
    "CHOLAFIN",
    "CIPLA",
    "COALINDIA",
    "COFORGE",
    "COLPAL",
    "CONCOR",
    "CUB",
    "CUMMINSIND",
    "DABUR",
    "DEEPAKNTR",
    "DIVISLAB",
    "DLF",
    "DRREDDY",
    "EICHERMOT",
    "ESCORTS",
    "EXIDEIND",
    "FEDERALBNK",
    "GAIL",
    "GLENMARK",
    "GMRINFRA",
    "GODREJCP",
    "GODREJPROP",
    "GRANULES",
    "GRASIM",
    "GUJGASLTD",
    "HAVELLS",
    "HCLTECH",
    "HDFC",
    "HDFCAMC",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDPETRO",
    "HINDUNILVR",
    "IBULHSGFIN",
    "ICICIBANK",
    "ICICIGI",
    "ICICIPRULI",
    "IDEA",
    "IDFCFIRSTB",
    "IGL",
    "INDIGO",
    "INDUSINDBK",
    "INDUSTOWER",
    "INFY",
    "IOC",
    "IRCTC",
    "ITC",
    "JINDALSTEL",
    "JSWSTEEL",
    "JUBLFOOD",
    "KOTAKBANK",
    "L&TFH",
    "LALPATHLAB",
    "LICHSGFIN",
    "LT",
    "LTI",
    "LTTS",
    "LUPIN",
    "M&M",
    "M&MFIN",
    "MANAPPURAM",
    "MARICO",
    "MARUTI",
    "MCDOWELL-N",
    "MFSL",
    "MGL",
    "MINDTREE",
    "MOTHERSUMI",
    "MPHASIS",
    "MRF",
    "MUTHOOTFIN",
    "NAM-INDIA",
    "NATIONALUM",
    "NAUKRI",
    "NAVINFLUOR",
    "NESTLEIND",
    "NMDC",
    "NTPC",
    "ONGC",
    "PAGEIND",
    "PEL",
    "PETRONET",
    "PFC",
    "PFIZER",
    "PIDILITIND",
    "PIIND",
    "PNB",
    "POWERGRID",
    "PVR",
    "RAMCOCEM",
    "RBLBANK",
    "RECLTD",
    "RELIANCE",
    "SAIL",
    "SBILIFE",
    "SBIN",
    "SHREECEM",
    "SIEMENS",
    "SRF",
    "SRTRANSFIN",
    "SUNPHARMA",
    "SUNTV",
    "TATACHEM",
    "TATACONSUM",
    "TATAMOTORS",
    "TATAPOWER",
    "TATASTEEL",
    "TCS",
    "TECHM",
    "TITAN",
    "TORNTPHARM",
    "TORNTPOWER",
    "TRENT",
    "TVSMOTOR",
    "UBL",
    "ULTRACEMCO",
    "UPL",
    "VEDL",
    "VOLTAS",
    "WIPRO",
    "ZEEL",
]

def make_OI_data_for_top_gainers():
    from construct_OI_data import construct_OI_data_from_tickers
    top_gainers = get_tickers_list_as_req('topGainer', 0)
    construct_OI_data_from_tickers(top_gainers)

    
def make_OI_data_for_top_loser():
    from construct_OI_data import construct_OI_data_from_tickers
    top_losers = get_tickers_list_as_req('topLoser', 0)
    construct_OI_data_from_tickers(top_losers)

    
def make_OI_data_for_premarket(max_tickers):
    from construct_OI_data import construct_OI_data_from_tickers
    pre_open = get_tickers_list_as_req('preOpen', max_tickers)
    construct_OI_data_from_tickers(pre_open)


def make_OI_full():
    from construct_OI_data import construct_OI_data_from_tickers
    construct_OI_data_from_tickers(STOCK_OPTION_UNIVERSE)

    
def get_tickers_list_as_req(condition, max_tickers):
    from nsetools import Nse
    import pandas as pd
    nse = Nse()
    #all_stock_codes = nse.get_stock_codes()
    if(condition == 'preOpen'):
        list_of_stocks_and_detial = nse.get_preopen_nifty()
    elif(condition == 'topGainer'):
        list_of_stocks_and_detial = nse.get_top_gainers()
    elif(condition == 'topLoser'):
        list_of_stocks_and_detial = nse.get_top_losers()
    list_of_tickers = []
    for item in list_of_stocks_and_detial:
        list_of_tickers.append(item.get('symbol'))
    if(max_tickers != 0):
        list_of_tickers = list_of_tickers[:max_tickers]
    return(list_of_tickers)
    #print(len(all_stock_codes))
    
