# frontend/components/charts.py

import pandas as pd
import plotly.express as px
import streamlit as st

def plot_severity_distribution(counts: pd.DataFrame) -> None:
    """Plots a pie chart representing threat severity distributions."""
    fig = px.pie(
        counts,
        names="Severity",
        values="Count",
        color="Severity",
        color_discrete_map={"LOW": "#10b981", "MEDIUM": "#eab308", "HIGH": "#f97316", "CRITICAL": "#ef4444"},
        hole=0.4
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280
    )
    st.plotly_chart(fig, width='stretch')

def plot_channel_analysis(chan_data: pd.DataFrame) -> None:
    """Plots a bar chart representing suspicious channel volume distributions."""
    fig = px.bar(
        chan_data,
        x="Channel",
        y="Suspicious Volume (%)",
        color="Channel",
        color_discrete_sequence=["#ef4444", "#f97316", "#eab308", "#3b82f6"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=280
    )
    st.plotly_chart(fig, width='stretch')

def plot_vulnerability_ratios(vuln_data: pd.DataFrame) -> None:
    """Plots a horizontal bar chart of demographic vulnerabilities."""
    fig = px.bar(
        vuln_data,
        x="Recruitment Prevalence (%)",
        y="Occupation",
        orientation="h",
        color="Recruitment Prevalence (%)",
        color_continuous_scale=px.colors.sequential.OrRd
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=260
    )
    st.plotly_chart(fig, width='stretch')

def plot_threat_stream(threat_stream: pd.DataFrame) -> None:
    """Plots an area chart representing real-time webhook complaint velocities."""
    fig = px.area(
        threat_stream,
        x="Time",
        y="Alerts Ingested",
        color_discrete_sequence=["#ef4444"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=260
    )
    st.plotly_chart(fig, width='stretch')
