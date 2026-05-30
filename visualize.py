import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def build_subplot_grid(filter_data, cutoff):
    fig = make_subplots(
        rows=max(1, -(-len(filter_data) // 2)), cols=2,
        subplot_titles=list(filter_data.keys())
    )
    for i, (name, series) in enumerate(filter_data.items()):
        row = i // 2 + 1
        col = i % 2 + 1
        filtered = series[series.index >= cutoff]
        fig.add_trace(
            go.Scatter(x=filtered.index, y=filtered.values, name=name),
            row=row, col=col
        )
    fig.update_layout(height=900, title_text='Macro Tracker', showlegend=False, template='plotly_dark')
    return fig

def build_overlay_chart(overlay_selected, filter_data, cutoff, normalize, zscore):
    fig = go.Figure()
    for i, name in enumerate(overlay_selected):
        series = filter_data[name]
        filtered = series[series.index >= cutoff]
        if normalize:
            filtered = zscore(filtered)
        fig.add_trace(
            go.Scatter(
                x=filtered.index,
                y=filtered.values,
                name=name,
                yaxis='y' if (normalize or i == 0) else 'y2'
            )
        )
    
    fig.update_layout(
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
        ),
        template='plotly_dark'
    )
    return fig