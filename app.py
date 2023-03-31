import pandas as pd
import json
from requests import Request, Session
import pandas as pd

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("\n Dataframe empty. Finishing execution")
        return False
    if df.symbol.empty:
        raise Exception("\n Symbol is Null or the value is empty")
    if df.price.empty:
        raise Exception("\n Price is Null or the value is empty")
    if df.date_added.empty:
        raise Exception("\n Date is Null or the value is empty")
    return True


def load_data(table_name,coins_df,session_db, engine_db):
    if check_if_valid_data(coins_df):
        print("\nData valid, proceed to Load stage")
    
    #Load data on database
    try:
        coins_df.to_sql(table_name,engine_db,index=False,If_exists="append")
        print("\nData Loaded on Database")
    except Exception as err:
        print("\nFail to load data on database: {err}")
    
    session_db.commit()
    session_db.close()
    print("\nClose database succesfully")
    return session_db

def get_data(session_db, engine_db, start, limit, convert, key, url):
    parameters = {
        'start' : start,
        'limit' : limit,
        'convert' : convert
    }
    headers ={
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key
    }

    session = Session()
    session.headers.update(headers)

    name = []
    symbol = []
    date_added = []
    last_updated = []
    price = []
    volume_24h = []
    circulating_supply = []
    total_supply = []
    max_supply = []
    volume_24h = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        print('\n')
        for coin in data['data']:
            name.append(coin['name'])
            symbol.append(coin['symbol'])
            date_added.append(coin['date_added'])
            last_updated.append(coin['last_updated'])
            circulating_supply.append(coin['circulating_supply'])
            total_supply.append(coin['total_supply'])
            max_supply.append(coin['max_supply'])
            price.append(coin['quote']['USD']['price'])
            volume_24h.append(coin['quote']['USD']['volume_24h'])
            percent_change_1h.append(coin['quote']['USD']['percent_change_1h'])
            percent_change_24h.append(coin['quote']['USD']['percent_change_24h'])
            percent_change_7d.append(coin['quote']['USD']['percent_change_7d'])

        coin_dict = {
            "name" : name,
            "symbol": symbol,
            "date_added" : date_added,
            "last_updated" : last_updated,
            "price": price,
            "volume_24h": volume_24h,
            "circulating_supply" : circulating_supply,
            "total_supply": total_supply,
            "max_supply": max_supply, 
            "percent_change_1h": percent_change_1h,
            "percent_change_24h": percent_change_24h,
            "percent_change_7d": percent_change_7d
    }   


    except Exception as e:
        print (f'Error to get data from APi: {e}')
        exit(1)   

    coins_df = pd.DataFrame(coin_dict, columns=["name", "symbol", "date_added", "last_updated","price","volume_24h","circulating_supply",
                                                 "total_supply","max_supply","percent_change_1h","percent_change_24h","percent_change_7d"])    
    
    print("Data on pandas Dataframe: \n")
    print(coins_df.head(10))

    load_data('tb_coins',coins_df,session_db,engine_db)






