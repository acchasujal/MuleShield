# frontend/components/kpi_cards.py

import streamlit as st

def render_kpi_card(title: str, value: str, footer: str, border_color: str = "#3b82f6") -> None:
    """Renders a premium metric KPI card with beautiful styling."""
    st.markdown(f"""
    <div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid {border_color};box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
        <h5 style='color:#94a3b8;margin:0;font-size:11px;text-transform:uppercase;'>{title}</h5>
        <h2 style='color:#f8fafc;margin:5px 0;font-size:24px;'>{value}</h2>
        <span style='color:{border_color};font-size:11px;font-weight:bold;'>{footer}</span>
    </div>
    """, unsafe_allow_html=True)
