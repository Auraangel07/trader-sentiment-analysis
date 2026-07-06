import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sentiment vs Trader Behavior", layout="wide")

# ─────────────────────────────────────────────────────────
# 1. LOAD DATA
# Reuse your Cells 2-5 logic from the notebook: load both CSVs,
# convert timestamps, merge, build the `daily` dataframe.
# TODO: paste/adapt that pipeline into a function called load_data()
# that returns the finished `daily` dataframe.
# ─────────────────────────────────────────────────────────

@st.cache_data  # <- this decorator means Streamlit only re-runs this
                # function when the underlying files change, not on
                # every single click. Without it, your app reloads
                # and reprocesses 15k rows every time someone touches a widget.
def load_data():
    # TODO: your pipeline here
    daily = None
    return daily

daily = load_data()

st.title("Trader Performance vs Market Sentiment")
st.caption("Primetrade.ai take-home — Hyperliquid trader behavior across Fear/Greed regimes")

# ─────────────────────────────────────────────────────────
# 2. SIDEBAR FILTER
# TODO: add a st.sidebar.multiselect() letting the user pick which
# sentiment buckets to include (Fear / Greed / Neutral).
# Hint: get the unique values from daily['sentiment_bucket'] to
# populate the options, and use .isin() to filter the dataframe
# based on what's selected.
# ─────────────────────────────────────────────────────────

# selected = st.sidebar.multiselect(...)
# filtered = daily[daily['sentiment_bucket'].isin(selected)]

# ─────────────────────────────────────────────────────────
# 3. KPI ROW
# TODO: use st.columns(3) to lay out 3 side-by-side st.metric() cards:
#   - average win rate (filtered)
#   - average daily PnL (filtered)
#   - average long/short ratio (filtered)
# Hint: st.columns(3) returns 3 column objects, use them like:
#   col1, col2, col3 = st.columns(3)
#   with col1: st.metric("Win Rate", f"{value:.1%}")
# ─────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────
# 4. CHARTS
# TODO: at minimum, recreate your Cell 6 comparison as a bar chart.
# Hint: st.bar_chart() takes a dataframe directly — group your
# filtered data by sentiment_bucket, take the mean of daily_pnl
# and win_rate, and pass that grouped result straight in.
# ─────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────
# 5. RAW DATA TABLE (nice to have, easy win)
# TODO: st.dataframe(filtered) with maybe a st.checkbox() to
# toggle whether it's shown at all.
# ─────────────────────────────────────────────────────────