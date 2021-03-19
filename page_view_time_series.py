import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import sys

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

df.set_index('date', drop=True, inplace=True)
df.index = [pd.Timestamp(dt) for dt in df.index]

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))]



def draw_line_plot():
    # Draw line plot
    fig, axis = plt.subplots(1, 1)

    fig.set_figwidth(15)
    fig.set_figheight(5)

    plt.plot(df.index, df['value'], color='r', linewidth=1)

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    plt.xlabel('Date')
    plt.ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar['Date'] = df_bar.index
    df_bar['Year'] = df_bar['Date'].map(lambda x: x.strftime('%Y'))
    df_bar['Month'] = df_bar['Date'].map(lambda x: x.strftime('%B'))
    df_bar = pd.DataFrame({
        'Average Page Views':
        df_bar.groupby(['Year', 'Month'])['value'].mean()
    }).reset_index().sort_values(['Year', 'Month'], ascending=[1, 1])

    # Draw bar plot
    month_label = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]

    fig, ax = plt.subplots(figsize=(20, 15))

    bar_plot = sns.barplot(
        x='Year',
        y='Average Page Views',
        palette="deep",
        hue='Month',
        hue_order=month_label,
        data=df_bar)

    ax.set_ylabel("Average Page Views", fontsize='24')
    ax.set_xlabel("Years", fontsize='24')
    ax.legend(loc=2, fontsize='24')

    ax.tick_params(axis='both', which='major', labelsize=24)
    plt.xticks(rotation=90, horizontalalignment="center")
    sns.set(style="whitegrid", font_scale=5)

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['date'] = df_box.index
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    df_box['smonth'] = [d.strftime('%m') for d in df_box.date]

    df_box = df_box.sort_values(by='smonth')

    fig, axes = plt.subplots(1, 2)
    fig.set_figwidth(18)
    fig.set_figheight(6)

    axes[0].set_title("Year-wise Box Plot (Trend)", fontsize='16')
    axes[1].set_title("Month-wise Box Plot (Seasonality)", fontsize='16')

    axes[0] = sns.boxplot(x=df_box.year, y=df_box.value, ax=axes[0])
    axes[0].set_xlabel('Year', fontsize='10')
    axes[0].set_ylabel('Page Views', fontsize='10')

    axes[1] = sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_xlabel('Month', fontsize='10')
    axes[1].set_ylabel('Page Views', fontsize='10')

    axes[0].tick_params(axis='both', which='major', labelsize=14)
    axes[1].tick_params(axis='both', which='major', labelsize=14)

    fig.savefig('box_plot.png')
    return fig