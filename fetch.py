import os
import requests
import pandas as pd
import streamlit as st
from fredapi import Fred
from datetime import datetime

#Initial Setup
current_year = datetime.now().year

#Data Caching
def get_fred_client():
    try:
        return Fred(api_key=st.secrets['FRED_API_KEY'])
    except:
        from dotenv import load_dotenv
        load_dotenv()
        return Fred(api_key=os.getenv('FRED_API_KEY'))

indicators_us ={
    'US 10Y Yield': 'DGS10',
    'CPI': 'CPIAUCSL',
    'Core PCE': 'PCEPILFE',
    'Michigan Consumer': 'UMCSENT', #delayed due to UMich constraints
    # 'ADP Employment': 'ADPWNUSNERSA', #delayed as API is restricted to ADP clients
    'SOFR': 'SOFR',
}

@st.cache_data(ttl=86400) #run function once, store the result, and reuse it until you restart the app
def load_fred_data():
    fred = get_fred_client()
    data = {}
    for name, series_id in indicators_us.items():
        data[name] = fred.get_series(series_id)
    return data

@st.cache_data(ttl=86400)
def load_bls_data():
    try:
        bls_key = st.secrets['BLS_API_KEY']
    except:
        from dotenv import load_dotenv
        load_dotenv()
        bls_key = os.getenv('BLS_API_KEY')
    
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-type': 'application/json'}
    chunks = []
    for start in range(1950, current_year + 1, 20): #must iterate per every 20 years due to BLS limitations
        end = min(start + 19, current_year)
        payload = {
            "seriesid": ['CES0000000001'], #id for Nonfarm Payrolls
            "startyear": str(start),
            "endyear": str(end),
            "registrationkey": bls_key
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        series = data['Results']['series'][0]['data']
        chunks.extend(series)
    
    df = pd.Series(
        {f"{d['year']}-{d['period'].replace('M', '')}-01": float(d['value']) for d in chunks}
    )
    df.index = pd.to_datetime(df.index)
    return df.sort_index()

#Standardizing Different Data
def zscore(series):
    return (series - series.mean()) / series.std()