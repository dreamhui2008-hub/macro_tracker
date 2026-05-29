from dotenv import load_dotenv
from fredapi import Fred
from datetime import datetime
from plotly.subplots import make_subplots

import os
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

#Initial Setup
load_dotenv()
current_year = datetime.now().year

#BLS Setup
def get_bls_latest(series_id):
    url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-type': 'application/json'}

    chunks = []
    for start in range(1950, current_year + 1, 20):
        end = min(start + 19, current_year)
        payload = {
            "seriesid": [series_id],
            "startyear": str(start),
            "endyear": str(end),
            "registrationkey": os.getenv('BLS_API_KEY')
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

#Fred Setup
fred = Fred(api_key = os.getenv('FRED_API_KEY'))

indicators ={
    'US 10Y Yield': 'DGS10',
    'CPI': 'CPIAUCSL',
    'Core PCE': 'PCEPILFE',
    'Michigan Consumer': 'UMCSENT', #delayed due to UMich constraints
    # 'ADP Employment': 'ADPWNUSNERSA', #delayed as API is restricted to ADP clients
    'SOFR': 'SOFR',
}

#Series Data Aggregation
series_data = {}

for name, series_id in indicators.items():
    series_data[name] = fred.get_series(series_id)

series_data['Nonfarm Payrolls'] = get_bls_latest('CES0000000001')

#Plotly Setup

def filter_series(series, years):
    cutoff = series.index.max() - pd.DateOffset(years=years)
    return series[series.index >= cutoff]

selected = [x for x in indicators]

fig2 = go.Figure()

for name in selected:
    fig2.add_trace(
        go.Scatter(x=series_data[name].index, y=series_data[name].values, name=name)
    )
fig2.update_layout(title='Indicator Overlay', height=500)
fig2.show()

# fig = make_subplots(
#     rows = 3, cols= 2,
#     subplot_titles=list(series_data.keys())
# )

# for i, (name, series) in enumerate(series_data.items()):
#     row = i // 2 + 1
#     col = i % 2 + 1
#     fig.add_trace(
#         go.Scatter(x=series.index, y=series.values, name=name),
#         row=row, col=col
#     )

# fig.update_layout(height=900, title_text='Macro Tracker', showlegend=False)
# fig.show()