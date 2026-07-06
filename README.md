# Trader Performance vs Market Sentiment

**Primetrade.ai Take-Home Assignment**
Analyzing Hyperliquid trader behavior across Fear/Greed market sentiment regimes.

🔗 **Live Dashboard:** https://trader-sentiment-analysis-87osqeqyfxxhig8rtbdavi.streamlit.app

---

## Overview

This project merges two datasets — Hyperliquid historical trade data and the
Bitcoin Fear & Greed Index — to answer a core question: **does trader
behavior and performance shift measurably with market sentiment, and if so,
how?**

The analysis moves from raw data validation → sentiment-segmented
performance comparison → behavioral segmentation (size, frequency) → a
data-backed strategy write-up → an exploratory account-level clustering
bonus.

## Repo Contents

| File | Purpose |
|---|---|
| `trades_sentiment.ipynb` | Full analysis notebook (Cells 1–10) |
| `App.py` | Streamlit dashboard (interactive version of Cells 6–8) |
| `requirements.txt` | Python dependencies for deployment |
| `historical_data.csv` | Hyperliquid trade-level data |
| `fear_greed_index (1).csv` | Daily sentiment classification |

## Methodology

1. **Load & inspect** — checked shape, dtypes, nulls, and duplicates on both
   raw files before any transformation.
2. **Timestamp alignment** — trade timestamps (`Timestamp IST`, custom
   `%d-%m-%Y %H:%M` format) were parsed and normalized to a bare date to
   match the sentiment index's daily granularity. This step is the most
   common silent-failure point in this kind of merge, so it was validated
   before joining.
3. **Left join** — trades were joined to sentiment on `date` using a left
   join, preserving every trade even where sentiment data was unavailable,
   rather than silently dropping rows via an inner join.
4. **Daily rollup** — trades were aggregated to Account × Date grain,
   computing daily PnL, win rate, average trade size, trade count, and
   long/short ratio.
5. **Segmentation** — accounts/days were split by sentiment bucket
   (Fear / Greed / Neutral), and independently by **median** trade size and
   trade frequency, to isolate behavioral patterns from sentiment-driven
   ones.

## Key Findings

- **Fear-day performance exceeds Greed-day performance** on both PnL and
  win rate in this sample — traders active during Fear outperformed those
  active during Greed.
- **Directional bias flips with sentiment**: long/short ratio moves from
  roughly 1.7 (net long) during Fear to roughly 0.46 (net short) during
  Greed — the opposite of the naive "panic-sell in Fear" assumption.
- **Frequent traders outperform infrequent traders** on both dimensions:
  28.8% vs 23.5% win rate, and $15,990 vs $3,287 average PnL — a larger,
  more consistent gap than the sentiment-based split.

### Rules of Thumb
1. Don't reduce activity during Fear regimes — in this sample, Fear-day
   activity correlates with *better* outcomes, not worse.
2. Favor a high-frequency trading profile — trade count correlates with
   both higher win rate and higher PnL, suggesting consistency/skill rather
   than a lucky small sample.

## Bonus: Account-Level Clustering

Accounts were clustered (KMeans, k=3, standardized features) on win rate,
average trade size, trade count, long/short ratio, and active days.

**Important caveat, stated explicitly rather than glossed over:** this
dataset contains only **4 unique accounts**. Clustering 4 points into 3
groups is illustrative, not statistically robust — there isn't enough data
for the result to generalize, and it shouldn't be read as a validated
segmentation model. It's included to demonstrate the technique and because
even at n=4, one pattern held up: **larger trade size did not correlate
with better outcomes** — the best- and worst-performing clusters both
traded large size; win rate, not size, was the differentiator. This lines
up with the frequency-over-size finding above.

## Dashboard

The Streamlit app reproduces the sentiment and segmentation analysis
interactively:
- Sidebar filter by sentiment regime (Fear / Greed / Neutral)
- KPI cards for win rate, daily PnL, and long/short ratio
- Sentiment-segmented and size/frequency-segmented bar charts
- Raw data table (toggleable)

### Run locally
```bash
pip install -r requirements.txt
streamlit run App.py
```

## Tech Stack
- Python, pandas, numpy
- scikit-learn (StandardScaler, KMeans)
- Streamlit (dashboard + Community Cloud deployment)

## Limitations
- Small account count (n=4) limits statistical power for clustering.
- Findings are descriptive (group means, medians) rather than
  significance-tested — directional patterns, not proven causal effects.
- Sentiment classification is daily-level; intraday sentiment shifts are
  not captured.

---
**Author:** Angel Suri ([@Auraangel07](https://github.com/Auraangel07))
