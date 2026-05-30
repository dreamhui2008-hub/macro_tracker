import pandas as pd
import streamlit as st

from fetch import load_fred_data, load_bls_data, indicators_us, zscore
from visualize import build_subplot_grid, build_overlay_chart

#Initial Setup
st.set_page_config(
    page_title="Macro Tracker",
    layout="wide"
)

normalize = st.sidebar.checkbox('Normalize (Z-score)', value=False)

#Streamlit Setup
st.title('Macro Tracker')

st.sidebar.header('Controls')

selected = st.sidebar.multiselect(
    'Select indicators',
    options = list(indicators_us.keys()) + ['Nonfarm Payrolls'],
    default = list(indicators_us.keys()) + ['Nonfarm Payrolls']
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
cutoff = pd.Timestamp.now() - pd.DateOffset(years=years)

fig = build_subplot_grid(filter_data, cutoff)
st.plotly_chart(fig, use_container_width=True)

st.subheader('Indicator Overlay')

max_select = None if normalize else 2

overlay_selected = st.multiselect(
    'Select indicators to overlay',
    options = list(filter_data.keys()),
    default = list(filter_data.keys())[:2],
    max_selections=max_select
)

fig2 = build_overlay_chart(overlay_selected, filter_data, cutoff, normalize, zscore)

st.plotly_chart(fig2, use_container_width=True)

if not normalize and len(overlay_selected) > 2:
    st.warning("Raw mode works best with 2 indicators. Enable Z-score for 3 or more.")