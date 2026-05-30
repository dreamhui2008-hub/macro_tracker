import os
import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go

from dotenv import load_dotenv
from fredapi import Fred
from datetime import datetime
from plotly.subplots import make_subplots

#Initial Setup
load_dotenv()
current_year = datetime.now().year

st.set_page_config(
    page_title="Macro Tracker",
    layout="wide"
)

#Fred Setup
fred = Fred(api_key = st.secrets('FRED_API_KEY'))

indicators ={
    'US 10Y Yield': 'DGS10',
    'CPI': 'CPIAUCSL',
    'Core PCE': 'PCEPILFE',
    'Michigan Consumer': 'UMCSENT', #delayed due to UMich constraints
    # 'ADP Employment': 'ADPWNUSNERSA', #delayed as API is restricted to ADP clients
    'SOFR': 'SOFR',
}

#Data Caching
@st.cache_data #run function once, store the result, and reuse it until you restart the app
def load_fred_data():
    data = {}
    for name, series_id in indicators.items():
        data[name] = fred.get_series(series_id)
    return data

@st.cache_data
def load_bls_data():
    url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-type': 'application/json'}

    chunks = []
    for start in range(1950, current_year + 1, 20): #must iterate per every 20 years due to BLS limitations
        end = min(start + 19, current_year)
        payload = {
            "seriesid": ['CES0000000001'], #id for Nonfarm Payrolls
            "startyear": str(start),
            "endyear": str(end),
            "registrationkey": st.secrets('BLS_API_KEY')
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

normalize = st.checkbox('Normalize (Z-score)', value=False)

#Streamlit Setup
st.title('Macro Tracker')

st.sidebar.header('Controls')

selected = st.sidebar.multiselect(
    'Select indicators',
    options = list(indicators.keys()) + ['Nonfarm Payrolls'],
    default = list(indicators.keys()) + ['Nonfarm Payrolls']
    )

years = st.sidebar.selectbox(
    'Time window',
    options=[1, 5, 10, 20, 50, 100],
    index = 2
)

with st.spinner('Loading data...'): #context manager that shows a spinning animation in the browser while the code inside it is running
    series_data = load_fred_data()
    series_data['Nonfarm Payrolls'] = load_bls_data()

st.success('Data loaded.')

filter_data = {k: v for k, v in series_data.items() if k in selected}

fig = make_subplots(
    rows = max(1, -(-len(filter_data) // 2)), cols= 2,
    subplot_titles=list(filter_data.keys())
)

cutoff = pd.Timestamp.now() - pd.DateOffset(years=years)

for i, (name, series) in enumerate(filter_data.items()):
    row = i // 2 + 1
    col = i % 2 + 1
    filtered = series[series.index >= cutoff]
    fig.add_trace(
        go.Scatter(x=filtered.index, y=filtered.values, name=name),
        row=row, col=col
    )

fig.update_layout(height=900, title_text='Macro Tracker', showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader('Indicator Overlay')

max_select = None if normalize else 2

overlay_selected = st.multiselect(
    'Select indicators to overlay',
    options = list(filter_data.keys()),
    default = list(filter_data.keys())[:2],
    max_selections=max_select
)

fig2 = go.Figure()

for i, name in enumerate(overlay_selected):
    series = filter_data[name]
    filtered = series[series.index >= cutoff]
    if normalize:
        filtered = zscore(filtered)
    fig2.add_trace(
        go.Scatter(
            x=filtered.index,
            y=filtered.values,
            name=name,
            yaxis='y' if (normalize or i == 0) else 'y2'
            )
    )

st.divider()
fig2.update_layout(
    height=500,
    yaxis=dict(title='Z-score' if normalize else ''),
    yaxis2=dict(
        title=overlay_selected[1] if len(overlay_selected) > 1 and not normalize else '',
        overlaying='y',
        side='right'
    ) if not normalize else {},
    xaxis=dict(rangeslider=dict(visible=True)),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    )
)

st.plotly_chart(fig2, use_container_width=True)

if not normalize and len(overlay_selected) > 2:
    st.warning("Raw mode works best with 2 indicators. Enable Z-score for 3 or more.")