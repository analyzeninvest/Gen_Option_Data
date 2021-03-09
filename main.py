#!/usr/bin/env python

def main():
    ticker = "ITC"
    xl = make_latest_option_xls_by_tiker(ticker)
    read_option_xls_make_dataframes(xl)
    

def read_option_xls_make_dataframes(xls_path):
    """
    This will make the dataframe from the XLS_PATH provided.
    """
    import pandas as pd
    df_CE = pd.read_excel(xls_path, skip_rows = 20, nrows = 20)
    df_PE = pd.read_excel(xls_path, nrows = 20)
    print(df_CE)
    print(df_PE)
    df_CE.to_csv("CE.csv")
    df_PE.to_csv("PE.csv")
    
    
def make_latest_option_xls_by_tiker(ticker):
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
    raw_options_data = nse_optionchain_scrapper(ticker)
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
        xls_path = ticker + "_Option_Data" + ".xls"
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
            ce_array = df_option_chain_per_strike.values[2]
            pe_array = df_option_chain_per_strike.values[3]
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
