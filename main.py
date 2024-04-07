import csv
import json
import requests

from candles import SingleCandleStick, DoubleCandleStick, TripleCandleStick

#--------------------------------------------------------------------------------------------------------
stk_name = input("Enter the STOCK NAME=")
read_option = int(input("Enter 1 to get market data 2 for read from json file:"))
json_enable = int(input("Enter 1 to create and 0 for not to create json file: "))
csv_enable = int(input("Enter 1 to create and 0 for not to create csv file: "))
#--------------------------------------------------------------------------------------------------------

#-------------------Function to get data from API-------------------------------------------
def getstockdata(stk_name: str) -> dict:
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stk_name+'.BSE&outputsize=full&apikey=4PUVR5YN5CP30RNV'
    r = requests.get(url, timeout=5)

    if r.status_code == 200:
        return r.json()
    elif r.status_code == 404:
        r.raise_for_status()
        return {}
    else:
        return {}


#---------------------Function to create csv file-------------------------------------------
def createjsonfile(response, stk_name: str) -> None:
    with open(f'{stk_name}.json', 'w') as json_file:
        json.dump(response, json_file)
    print(f'json file in the name of {stk_name}.json is created')


#---------------------Function to create json file------------------------------------------
def createcsvfile(response, stk_name: str) -> None:
    json_data = response
    headers = ['Data', 'Open', 'High', 'Low', 'close', 'Volumes']
    with open(f'{stk_name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(headers)

        for date, values in json_data['Time Series (Daily)'].items():
            open_price = values['1. open']
            high_price = values['2. high']
            low_price = values['3. low']
            close_price = values['4. close']
            volume = values['5. volume']
            date_list = [date, open_price, high_price, low_price, close_price, volume]
            csv_write.writerow(date_list)

    print(f'CSV file in the name of {stk_name}.csv is created')


#----------------------Function to create the csv,json file based on enable-----------------
def create_files(stk_data, stk_name, csv_enable, json_enable):
    if csv_enable == 1:
        createcsvfile(stk_data, stk_name)
    if json_enable == 1:
        createjsonfile(stk_data, stk_name)

if __name__ == "__main__":

    #-------------------Reading data from API or json---------------------------------------
    if read_option == 1:
        stk_data = getstockdata("stk_name")
        print(stk_data)
    elif read_option == 2:
        with open(f'{stk_name}.json', 'r') as json_data,open(f'{stk_name}.txt','w') as text_file:
            stk_data = json.load(json_data)
    else:
        print("Invalid Entry")
    
    #------------------Calling function to create json,csv file-----------------------------
    create_files(stk_data, stk_name, csv_enable, json_enable)

    # Setting day to '0' in start of the program
    day: int = 0

    #------------------Looping through data from detecting candle pattern-------------------
    for date, ohlcv in stk_data["Time Series (Daily)"].items():
        patten1 = SingleCandleStick(ohlcv)
         
        if day > 0:
             patten2 = DoubleCandleStick(ohlcv2, ohlcv)
        
        if day > 1:
            patten3 = TripleCandleStick(ohlcv3, ohlcv2, ohlcv)
        
        ohlcv2 = ohlcv
        ohlcv3 = ohlcv2

        #-------------Writeing the detected patten in the text file-------------------------
        if day == 0:
            format_row = f"{(date,)+patten1.ohlvc_value+(0,0)+(0,0)},\n"
        if day == 1:
            format_row = f"{(date,)+patten1.ohlvc_value+patten2.get_value()+(0,0)},\n"
        if day >1:
            format = (date,patten1.ohlvc_value,patten2.get_value(),patten3.get_patten())
            date,tupl1,tuple2,tuple3 = format
            format_row = f"{(date,)+tupl1+tuple2+tuple3},\n"
        
        text_file.write(format_row)

        day = day + 1
else:
    print("This is not a main file")
