#!/usr/bin/env python

TICKER = "TATASTEEL"
PROJECT_PATH = "/home/arnashree/analyzeninvest-projects/Gen_Option_Data/"
XLS_PATH = PROJECT_PATH + "Option_Data/"
LARGE_OI = 1000
SPREAD = .10

ONE_STOCK = True

LIST_OF_TICKERS = [
    #"NTPC",
    #"ICICIBANK",
    #"HDFCBANK",
    "AXISBANK",
    "GAIL",
    #"UPL",
    #"TATAMOTORS",
    #"INDUSINDBK",
    #"BPCL"
    #"TATAMOTORS",
    #"TCS",
    #"IOC",
    "ONGC",
    #"SUNPHARMA",
    #"INFY",
    #"SBIN",
    #"PNB", #
    #"IBULHSGFIN",
    #"LICHSGFIN",
    "TATASTEEL",
    #"YESBANK", #
    #"COALINDIA",
    #"HDFCBANK",
    #"BHEL",
    #"ABB" #
    "POWERGRID",
    "INDUSINDBK",
    "BAJAJFINSV",
    "SBILIFE",
    "HDFCLIFE"
]

def main():
    
    init_template()
    if ONE_STOCK == True:
        print("\nRunning for :" + TICKER)
        run_by_ticker(TICKER)
    else:
        for tickers in LIST_OF_TICKERS:
            print("\nRunning for :" + tickers)
            run_by_ticker(tickers)
    construct_df_from_latest_OI(PROJECT_PATH + "OI.csv")
    construct_tradable_oi()

def construct_tradable_oi():
    """
    Construct OI that is tradable.
    """
    import pandas as pd
    df_filtered_oi = pd.read_csv(PROJECT_PATH + "OI_filtered.csv")
    df_tradable_more = df_filtered_oi[df_filtered_oi["strikePrice"] > df_filtered_oi["underlyingValue"]*SPREAD]
    df_tradable_less = df_filtered_oi[df_filtered_oi["strikePrice"] < df_filtered_oi["underlyingValue"]*SPREAD]
    df_tradable = pd.concat([df_tradable_less, df_tradable_more])
    print(df_tradable)

    
    
def init_template():
    """
    Make the init templates
    """
    import os
    import pandas as pd
    oi_path = PROJECT_PATH + "OI.csv"
    if os.path.exists(oi_path):
        os.remove(oi_path)
    template = {
	"PutCall":[],
	"strikePrice":[],
	"expiryDate":[],
	"underlying":[],
	"identifier":[],
	"openInterest":[],
	"changeinOpenInterest":[],
	"pchangeinOpenInterest":[],
	"totalTradedVolume":[],
	"impliedVolatility":[],
	"lastPrice":[],
	"change":[],
	"pChange":[],
	"totalBuyQuantity":[],
	"totalSellQuantity":[],
	"bidQty":[],
	"bidprice":[],
	"askQty":[],
	"askPrice":[],
	"underlyingValue":[]
    }
    df_template = pd.DataFrame(data=template)
    df_template.to_csv(oi_path, index=False)

    
def construct_df_from_latest_OI(oi_csv):
    """
    Filter the OI.csv file
    """
    import pandas as pd
    import re
    df_oi = pd.read_csv(oi_csv)
    #print(df_oi)
    df_oi_chopped = df_oi.drop([
        "strikePrice",
        "expiryDate",
        "underlying",
        "identifier",
        "openInterest",
        "changeinOpenInterest",
        "pchangeinOpenInterest",
        "totalTradedVolume",
        "impliedVolatility",
        "lastPrice",
        "change",
        "pChange",
        "totalBuyQuantity",
        "totalSellQuantity",
        "bidQty",
        "bidprice",
        "askQty",
        "askPrice",
        "underlyingValue"], axis=1)
    #print(df_oi_chopped)
    PE_CE_array = []
    PE_CE_array_filtered = []
    for column in df_oi_chopped.columns:
        PE_CE_array = df_oi_chopped[column]
        PE_CE_array_temp = []
        print(PE_CE_array)
        for elem in PE_CE_array:
            match = re.search("^([P|C]E)", str(elem))
            if match:
                PE_CE_array_temp.append(match.group(1))
        PE_CE_array_filtered.extend(PE_CE_array_temp)
    #print(PE_CE_array_filtered)
    PE_CE_dict = {"PutCall" : PE_CE_array_filtered}
    df_oi_required = pd.DataFrame(data=PE_CE_dict)
    df_oi_required = pd.concat([
        df_oi_required,
        df_oi["underlying"].reindex(df_oi_required.index),
        df_oi["expiryDate"].reindex(df_oi_required.index),
        df_oi["totalTradedVolume"].reindex(df_oi_required.index),
        df_oi["openInterest"].reindex(df_oi_required.index),
        df_oi["changeinOpenInterest"].reindex(df_oi_required.index),
        df_oi["underlyingValue"].reindex(df_oi_required.index),
        df_oi["strikePrice"].reindex(df_oi_required.index)], axis=1)
    print(df_oi_required)
    df_oi_required.to_csv(PROJECT_PATH + "OI_filtered.csv", index=False)
        

def run_by_ticker(ticker):
    """
    Make the OI.csv by TICKER.
    """
    xl = make_latest_option_xls_by_tiker(ticker)
    (df_CE, df_PE) = read_option_xls_make_dataframes(xl)
    #print(df_CE)
    #print(df_PE)
    df_CE = df_CE
    df_PE = df_PE
    df_CE_OI = get_large_open_interest(df_CE)
    df_PE_OI = get_large_open_interest(df_PE)
    #print(df_CE_OI)
    #print(df_PE_OI)
    df_OI = df_PE_OI.append(df_CE_OI)
    df_OI.index.name = "PutCall"
    append_to_OI_csv(df_OI)
    #print(df_OI)
    #df_OI.to_csv("OI.csv")
    #print(df_OI)
    
    

def append_to_OI_csv(df_oi):
    """
    This will append to the existing csv for OI data.
    """
    import pandas as pd
    df_existing = pd.read_csv(PROJECT_PATH + "OI.csv", index_col = None)
    df_all = df_existing.append(df_oi)
    #df_all = df_all.set_index("PutCall")
    df_all.to_csv(PROJECT_PATH + "OI.csv")

def get_large_open_interest(df):
    """
    This will filter large open interest by provided dataframe DF.
    Generally will filter values larger than LARGE_OI.
    """
    df_OI = filter_item_by_value(df, 'openInterest', LARGE_OI, True)
    return(df_OI)

def filter_item_by_value(df, item, value, is_greater): 
    """
    This will filter the DF by ITEM if VALUE is > or < based on IS_GREATER.
    """
    if(is_greater):
        df_filtered = df[df[item] > value]
    else:
        df_filtered = df[df[item] < value]
    return(df_filtered)

def read_option_xls_make_dataframes(xls_path):
    """
    This will make the dataframe from the XLS_PATH provided.
    """
    import pandas as pd
    df_CE = pd.read_excel(xls_path, skiprows = 20, nrows = 19, index_col = None)
    df_PE = pd.read_excel(xls_path, nrows = 19, index_col = None)
    df_CE = df_CE.set_index("Unnamed: 0").T
    #df_CE = df_CE.T
    #df_CE.rename_axis("PutCall")
    df_PE = df_PE.set_index("Unnamed: 0").T
    #df_PE = df_PE.T
    #df_PE.rename_axis("PutCall")
    #print(df_CE)
    #print(df_PE)
    df_CE.to_csv(XLS_PATH + "CE.csv")
    df_PE.to_csv(XLS_PATH + "PE.csv")
    return(df_CE, df_PE)
    
    
def make_latest_option_xls_by_tiker(TICKER):
    """
    make the option xls by the TICKER.
    """
    #from nsetools import Nse
    from nsepython import nse_optionchain_scrapper
    from pprint import pprint
    import openpyxl
    from openpyxl import Workbook
    import pandas as pd
    #nse = Nse()
    #all_stock_codes = nse.get_stock_codes()
    #pprint(all_stock_codes)
    #pprint(nse.get_quote('infy'))
    raw_options_data = nse_optionchain_scrapper(TICKER)
    #print(type(raw_options_data))
    df_raw_option_data = pd.DataFrame.from_dict(raw_options_data)
    #print(df_option_table_by_strike)
    #print("Columns are:")
    for col in df_raw_option_data.columns:
        print(col)
        #print(df_option_table_by_strike.loc[['data']])
        df_filter_useful_data = df_raw_option_data.loc[['data']]
        df_latest_useful_data = df_filter_useful_data['filtered'][0]
        sheet_name = 0
        xls_path = XLS_PATH + TICKER + "_Option_Data" + ".xls"
        writer = pd.ExcelWriter(xls_path, engine='openpyxl')
        #first = True
        counter = 0
        for data_by_strike_price in df_latest_useful_data:
            df_option_table_by_strike = pd.DataFrame.from_dict(data_by_strike_price)
            #print(df_option_table_by_strike)
            df_option_chain_per_strike = df_option_table_by_strike.T
            #print(df_option_chain_per_strike)
            #sheet_name += 1
            #df_option_chain_per_strike.to_excel(writer, sheet_name = str(sheet_name))
            title = df_option_table_by_strike.index
            try:
                ce_array = df_option_chain_per_strike.values[2]
            except IndexError:
                ce_array = [0]*19
            try:
                pe_array = df_option_chain_per_strike.values[3]
            except IndexError:
                pe_array = [0]*19
            #print("\nPrinting: \n")
            #print(title)
            #print(ce_array)
            #print(pe_array)
            #if first == True: 
            #    df_option_chain = pd.DataFrame(data = {'CE':ce_array,'PE':pe_array}, index = title)
            #    df_option_chain = df_option_chain.T
            #    first = False
            #else:
            #    df_option_chain_ce_per_strike = pd.DataFrame(data = {'CE':ce_array}, index = title)
            #    df_option_chain_ce_per_strike = df_option_chain_ce_per_strike.T
            #    df_option_chain_pe_per_strike = pd.DataFrame(data = {'PE':pe_array}, index = title)
            #    df_option_chain_pe_per_strike = df_option_chain_pe_per_strike.T
            #    print(df_option_chain_pe_per_strike)
            #    print(df_option_chain_ce_per_strike)
            #    df_option_chain.append(df_option_chain_ce_per_strike)
            #    df_option_chain.append(df_option_chain_pe_per_strike)             
            df_option_chain_ce_per_strike = pd.DataFrame(data = {'CE':ce_array}, index = title)
            #df_option_chain_ce_per_strike = df_option_chain_ce_per_strike.T
            df_option_chain_pe_per_strike = pd.DataFrame(data = {'PE':pe_array}, index = title)
            #df_option_chain_pe_per_strike = df_option_chain_pe_per_strike.T
            if counter == 0:
                df_option_chain_pe_per_strike.to_excel(writer, startcol = counter,startrow =0,index = True)
                df_option_chain_ce_per_strike.to_excel(writer, startcol = counter,startrow =20,index = True)
            else:
                df_option_chain_pe_per_strike.to_excel(writer, startcol = counter,startrow =0,index = False)
                df_option_chain_ce_per_strike.to_excel(writer, startcol = counter,startrow =20,index = False)
            counter += 1
            #print(counter)
            writer.save()
            #print(df_option_chain)
            #sheet_name += 1
            #df_option_chain.to_excel(writer, sheet_name = str(sheet_name))
            #writer.save()
        #print(df_option_chain)
        #df_option_chain.to_excel(writer)
    writer.close()
    return(xls_path)



if __name__ == '__main__':
    main()
