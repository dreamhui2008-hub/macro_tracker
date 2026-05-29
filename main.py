import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd
import requests

#BLS Setup
def get_bls_latest(series_id):
    url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/{series_id}"
    response = requests.get(url)
    data = response.json()
    latest = data['Results']['series'][0]['data'][0]
    return float(latest['value']), f"{latest['year']}-{latest['period'].replace('M', '')}-01" #adding "-01" since Nonfarm only as date per month, but we want to align with other data

#Fred Setup
load_dotenv()

fred = Fred(api_key = os.getenv('FRED_API_KEY'))

indicators ={
    'US 10Y Yield': 'DGS10',
    'CPI': 'CPIAUCSL',
    'Core PCE': 'PCEPILFE',
    'Michigan Consumer': 'UMCSENT', #delayed due to UMich constraints
    # 'ADP Employment': 'ADPWNUSNERSA', #delayed as API is restricted to ADP clients
    'SOFR': 'SOFR',
}

results = {}

#Terminal Preview
for name, series_id in indicators.items():
    data = fred.get_series(series_id)
    results[name] = {
        'Latest Value': round(float(data.iloc[-1]), 2),
        'As of': data.index[-1].strftime('%Y-%m-%d')
    }

bls_value, bls_date = get_bls_latest('CES0000000001')
results['Nonfarm Payrolls'] = {
    'Latest Value': bls_value,
    'As of': bls_date
}

df = pd.DataFrame.from_dict(results, orient='index')

print(df)