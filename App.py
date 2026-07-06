import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sentiment vs Trader Behavior", layout="wide")


@st.cache_data
def load_data():
    # Cell 2: load + inspect
    sentiment_df = pd.read_csv('fear_greed_index (1).csv')
    trades_df = pd.read_csv('historical_data.csv')

    # Cell 3: timestamp alignment — the landmine you already know about
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    trades_df['date'] = pd.to_datetime(
        trades_df['Timestamp IST'], format='%d-%m-%Y %H:%M'
    ).dt.normalize()

    # Cell 4: left join — keep every trade even if sentiment is missing
    merged = trades_df.merge(
        sentiment_df[['date', 'classification']], on='date', how='left'
    )

    # Cell 5: derive features, build the daily rollup
    def is_long(direction):
        return direction in ['Buy', 'Open Long', 'Close Short', 'Short > Long']

    def is_short(direction):
        return direction in ['Sell', 'Open Short', 'Close Long', 'Long > Short']

    merged['is_long'] = merged['Direction'].apply(is_long)
    merged['is_short'] = merged['Direction'].apply(is_short)
    merged['win'] = merged['Closed PnL'] > 0

    daily = merged.groupby(['Account', 'date']).agg(
        daily_pnl=('Closed PnL', 'sum'),
        n_trades=('Closed PnL', 'size'),
        win_rate=('win', 'mean'),
        avg_trade_size=('Size USD', 'mean'),
        long_trades=('is_long', 'sum'),
        short_trades=('is_short', 'sum'),
        classification=('classification', 'first'),
    ).reset_index()

    daily['long_short_ratio'] = (
        daily['long_trades'] / daily['short_trades'].replace(0, np.nan)
    )

    def bucket(c):
        if pd.isna(c): return np.nan
        if 'Fear' in c: return 'Fear'
        if 'Greed' in c: return 'Greed'
        return 'Neutral'

    daily['sentiment_bucket'] = daily['classification'].apply(bucket)

    return daily

daily = load_data()

st.title("Trader Performance vs Market Sentiment")
st.caption("Primetrade.ai take-home — Hyperliquid trader behavior across Fear/Greed regimes")

# ─────────────────────────────────────────────────────────
# 2. SIDEBAR FILTER
# ─────────────────────────────────────────────────────────
st.sidebar.header("Filters")
all_buckets = sorted(daily['sentiment_bucket'].dropna().unique().tolist())
selected = st.sidebar.multiselect(
    "Sentiment regime",
    options=all_buckets,
    default=all_buckets
)
filtered = daily[daily['sentiment_bucket'].isin(selected)]

if filtered.empty:
    st.warning("No data for this filter selection.")
    st.stop()

# ─────────────────────────────────────────────────────────
# 3. KPI ROW
# ─────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Win Rate", f"{filtered['win_rate'].mean():.1%}")
with col2:
    st.metric("Avg Daily PnL", f"${filtered['daily_pnl'].mean():,.2f}")
with col3:
    st.metric("Avg Long/Short Ratio", f"{filtered['long_short_ratio'].mean():.2f}")

# ─────────────────────────────────────────────────────────
# 4. CHARTS
# ─────────────────────────────────────────────────────────
st.subheader("PnL & Win Rate by Sentiment")
chart_data = filtered.groupby('sentiment_bucket')[['daily_pnl', 'win_rate']].mean()
st.bar_chart(chart_data)

st.subheader("Size vs Frequency Segments")
med_size = filtered['avg_trade_size'].median()
filtered = filtered.copy()
filtered['size_segment'] = np.where(filtered['avg_trade_size'] > med_size, 'High size', 'Low size')
med_freq = filtered['n_trades'].median()
filtered['freq_segment'] = np.where(filtered['n_trades'] > med_freq, 'Frequent', 'Infrequent')

seg_col1, seg_col2 = st.columns(2)
with seg_col1:
    st.write("**Win rate by size segment**")
    st.bar_chart(filtered.groupby('size_segment')['win_rate'].mean())
with seg_col2:
    st.write("**Win rate & PnL by frequency segment**")
    st.bar_chart(filtered.groupby('freq_segment')[['win_rate', 'daily_pnl']].mean())

# ─────────────────────────────────────────────────────────
# 5. RAW DATA TABLE
# ─────────────────────────────────────────────────────────
if st.checkbox("Show raw data"):
    st.dataframe(filtered)
