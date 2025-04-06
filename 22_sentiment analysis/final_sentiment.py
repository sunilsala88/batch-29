import pandas as pd
import numpy as np
import warnings
# For plotting graphs
import matplotlib.pyplot as plt
# plt.style.use('seaborn-darkgrid')

# Import the function performance_analysis from the nsts_quantra file
import sys
warnings.filterwarnings('ignore')

# Read the data which contains the event dates for Apple Products
event_dates_data = pd.read_csv('/Users/algotrading2024/batch 29/22_sentiment analysis/apple_events_new.csv')
print(event_dates_data)
event_dates_data['Date'] = pd.to_datetime(event_dates_data['Date'],format='%d-%m-%Y')
print(event_dates_data)


# Fetch the price data of Apple from January 2001 to June 2023
stock_prices_data = pd.read_csv('/Users/algotrading2024/batch 29/22_sentiment analysis/AAPL_history.csv', index_col=0)
stock_prices_data.index = pd.to_datetime(stock_prices_data.index)
print(stock_prices_data)


# Fetch the sentiment data of Apple from January 2016 to Sep 2023
daily_sentiment_scores = pd.read_csv('/Users/algotrading2024/batch 29/22_sentiment analysis/daily_sentiment_scores_2016_jan_2023_sep.csv', index_col=0)
daily_sentiment_scores.index = pd.to_datetime(daily_sentiment_scores.index)
daily_sentiment_scores['date'] = daily_sentiment_scores.index
print(daily_sentiment_scores)



daily_sentiment_scores['rolling_20_mean'] = daily_sentiment_scores.sentiment_score.rolling(
    20).mean()
print(daily_sentiment_scores)

stock_prices_data = stock_prices_data.merge(daily_sentiment_scores[[
                                            'rolling_20_mean']], left_on='Date', right_index=True, how='left')


print(stock_prices_data)



def get_dates_before_event(event_dates_data, num_days):
    """
    Retrieve a list of intermediate dates between each date in the 'event_dates_data' DataFrame
    and the date 'num_days' days before it.

    Parameters:
    - event_dates_data: DataFrame containing a column 'Date' with event dates.
    - num_days: Number of days before each event date to calculate intermediate dates.

    Returns:
    - intermediate_dates_list: List of intermediate dates between 'date_prior_to_event' and 'Date'.
    """

    # Calculate the date 'num_days' days prior to the event date and store it in a new column
    event_dates_data['date_prior_to_event'] = event_dates_data['Date'] - pd.DateOffset(days=num_days)

    # Create a list to store intermediate dates
    intermediate_dates_list = []

    # Iterate through the rows and generate intermediate dates
    for index, row in event_dates_data.iterrows():
        event_date = row['Date']
        prior_date = row['date_prior_to_event']
        intermediate_dates = pd.date_range(start=prior_date, end=event_date)
        intermediate_dates_list.extend(intermediate_dates)

    return intermediate_dates_list



# Call the function get_dates_before_event from the util file
# to fetch a list of dates occurring 9 days before a significant event.
dates_list = get_dates_before_event(event_dates_data, 9)

# Create a column is_9_days_prior_to_event to mark if the day is within 9 days of a significant event
stock_prices_data['is_9_days_prior_to_event'] = stock_prices_data.index.isin(dates_list).astype(int)

print(stock_prices_data)



# Create a new column 'signal' in the 'stock_prices_data' dataframe
stock_prices_data['signal'] = np.where(
    # Check if the 'rolling_20_mean' column is greater than 0
    (stock_prices_data['rolling_20_mean'] > 0) &

    # Check if the 'is_9_days_prior_to_event' column is greater than 0
    (stock_prices_data['is_9_days_prior_to_event'] > 0),

    # If both conditions are met, assign the value 1
    1,

    # If not, assign the value 0
    0
)





# Calculate daily stock returns
stock_prices_data['daily_returns'] = stock_prices_data['Close'].pct_change()

# Calculate daily returns of the portfolio
stock_prices_data['strategy_returns'] = stock_prices_data['signal'].shift(1) * stock_prices_data['daily_returns']
print(stock_prices_data)

# print(stock_prices_data[stock_prices_data['is_9_days_prior_to_event']==1].tail(30))



def performance_analysis(stock_prices_data):
    # Calculate cumulative strategy returns
    stock_prices_data['cumulative_returns'] = (
        stock_prices_data['strategy_returns'] + 1.0).cumprod()
    
    # Print the cumulative returns
    print("The cumulative returns are {:.2f} times the initial returns".format(
        round(stock_prices_data['cumulative_returns'].iloc[-1], 2)))

    # Plot cumulative returns
    stock_prices_data['cumulative_returns'].plot(figsize=(15, 7), color='black')
    plt.title('Equity Curve', fontsize=14)
    plt.ylabel('Returns (in times)', fontsize=12)
    plt.xlabel('Year', fontsize=12)
    plt.show()

    # Total number of trading candles over time
    trading_candles = len(stock_prices_data['strategy_returns'])

    # Calculate compound annual growth rate
    cagr_value = (stock_prices_data['cumulative_returns'].iloc[-1] ** (252 / trading_candles) - 1) * 100

    # Print the CAGR in the desired format
    print("The CAGR is {:.2f}%".format(cagr_value))
    
    # Set a risk-free rate
    risk_free_rate = 0

    # Calculate Sharpe ratio
    sharpe_ratio = round(np.sqrt(252) * (np.mean(stock_prices_data['strategy_returns']) - risk_free_rate) / np.std(stock_prices_data['strategy_returns']), 2)
    print("The Sharpe Ratio is {:.2f}".format(sharpe_ratio))

    # Compute the cumulative maximum
    returns = pd.DataFrame()
    returns['Peak'] = (stock_prices_data['strategy_returns'] + 1).cumprod().cummax()

    # Compute the Drawdown
    returns['Drawdown'] = (((stock_prices_data['strategy_returns'] + 1).cumprod() - returns['Peak']) / returns['Peak']) * 100

    # Compute the maximum drawdown
    max_drawdown = "{0:.2f}%".format(returns['Drawdown'].min())
    print("The Maximum Drawdown is " + max_drawdown)

    # Plot maximum drawdown
    returns['Drawdown'].plot(figsize=(15, 7), color='red')

    # Set the title and axis labels
    plt.title('Drawdowns', fontsize=14)
    plt.ylabel('Drawdown(%)', fontsize=12)
    plt.xlabel('Year', fontsize=12)
    plt.fill_between(returns['Drawdown'].index, returns['Drawdown'].values, color='red')
    plt.show()
   

# Call the performance_analysis function to generate performance measures
performance_analysis(stock_prices_data)