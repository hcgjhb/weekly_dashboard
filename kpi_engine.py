import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

df=pd.read_csv("parsed_data.csv")

global date_range
date_range=False

global start_date
start_date = None
global end_date
end_date = None

df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# KPI 1: Total Outages
def total_outages(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df.shape[0]

# print("Total Outages:", total_outages(df))

# KPI 2: Average MTTR
def average_mttr(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df['MTTR in \nMints'].mean()

# print("Average MTTR:", average_mttr(df))

df['Customers'] = df['Customers'].apply(ast.literal_eval)


# KPI 3: Customers Impacted
def customers_impacted(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    customers=set()
    for i, row in df.iterrows():
        impacted=row['Customers']

        for customer in impacted:
            customers.add(customer)
    return len(customers)

# print("Customers Impacted:", customers_impacted(df))

# KPI 4: Total Downtime
def total_downtime(df):
    if date_range:
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df['MTTR in \nMints'].sum()

# print("Total Downtime:", total_downtime(df))

# Downtime trend
def plot_downtime_trend(df, week=None):
    df = df.copy()

    # ── Prepare columns ────────────────────────────────────────────────────────
    df['date']      = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['Down Time'] = pd.to_numeric(df['MTTR in \nMints'], errors='coerce').fillna(0)
    df['week']      = df['date'].dt.to_period('W').apply(lambda r: r.start_time)

    # ── Default to last week WITH data ─────────────────────────────────────────
    if week is None:
        latest_date = df['date'].max()
        week = df['week'][df['date'] == latest_date].values[0]

    df_week = df[df['week'] == week].sort_values('date')

    if df_week.empty:
        print(f"No data found for week starting {week}")
        return

    # ── Aggregate per day ──────────────────────────────────────────────────────
    daily = (
        df_week.groupby('date')
        .agg(downtime=('Down Time', 'sum'), outages=('Sr. No.', 'count'))
        .reset_index()
        .sort_values('date')
    )

    labels   = daily['date'].dt.strftime('%d %b').tolist()
    downtime = daily['downtime'].tolist()
    outages  = daily['outages'].tolist()
    x        = np.arange(len(labels))

    # ── Plot ───────────────────────────────────────────────────────────────────
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor('white')
    ax1.set_facecolor('white')

    # Bars → Downtime (Mins)
    ax1.bar(x, downtime, color='#6C63FF', width=0.55, zorder=2)
    ax1.set_ylabel('Downtime (Mins)', color='#444', fontsize=10)
    ax1.set_ylim(0, max(downtime) * 1.3 if downtime else 1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9)
    ax1.tick_params(axis='y', labelcolor='#444')
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(5, integer=True))
    ax1.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
    ax1.spines[['top', 'right']].set_visible(False)

    # Line → Outages
    ax2 = ax1.twinx()
    ax2.plot(x, outages, color='#00BFFF', marker='o',
             markerfacecolor='white', markeredgecolor='#00BFFF',
             markeredgewidth=2, markersize=7, linewidth=2, zorder=3)
    ax2.set_ylabel('Outages', color='#444', fontsize=10)
    ax2.set_ylim(0, max(outages) * 1.3 if outages else 1)
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(5, integer=True))
    ax2.tick_params(axis='y', labelcolor='#444')
    ax2.spines[['top', 'left']].set_visible(False)

    # Legend
    legend_elements = [
        Patch(facecolor='#6C63FF', label='Downtime (Mins)'),
        Line2D([0], [0], color='#00BFFF', marker='o', markerfacecolor='white',
               markeredgecolor='#00BFFF', markeredgewidth=2, label='Outages'),
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=9,
               frameon=False, ncol=2)

    # Title with week range
    week_start = pd.Timestamp(week)
    week_end   = week_start + pd.Timedelta(days=6)
    week_label = f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}"
    ax1.set_title(f'DOWNTIME TREND (MINUTES)  |  {week_label}',
                  fontweight='bold', fontsize=11, loc='left', pad=12)

    plt.tight_layout()
    plt.savefig('downtime_trend.png', dpi=150, bbox_inches='tight')
    plt.show()


# # Default — last week with data
plot_downtime_trend(df)

# Or pass a specific week
# plot_downtime_trend(df, week='2026-01-05')