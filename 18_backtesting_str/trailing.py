from backtesting import Backtest, Strategy
import yfinance as yf
import pandas_ta as ta

def get_sma(closing_price,len):
    return ta.sma(closing_price,len)

class TrailingStopLossStrategy(Strategy):
    # Define the parameters for the strategy
    n1 = 10  # Period for the short moving average
    n2 = 20  # Period for the long moving average
    trailing_stop_pct = 0.05  # 2% trailing stop-loss

    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(get_sma, self.data.Close.s, self.n1)
        self.sma2 = self.I(get_sma, self.data.Close.s, self.n2)

    def next(self):
        # Check if we have a position open
        if self.position.is_long:
            # Update the trailing stop-loss price
            current_price = self.data.Close[-1]
            trailing_stop_price = current_price * (1 - self.trailing_stop_pct)
            
            # Update the stop-loss price if the current price is higher than the previous stop-loss price
            if trailing_stop_price > self.trades[0].sl:
                self.trades[0].sl = trailing_stop_price

        # If we don't have a position, check for a crossover to enter a long position
        if (self.sma1[-1]>self.sma2[-1]) and (self.sma1[-2]<self.sma2[-2]) :
            if self.position.is_short:
                self.position.close()
            current_price = self.data.Close[-1]
            trailing_stop_price = current_price * (1 - self.trailing_stop_pct)

            self.buy(sl=trailing_stop_price)
        elif (self.sma1[-1]<self.sma2[-1]) and (self.sma1[-2]>self.sma2[-2]) :
            if (self.position.is_long):
                self.position.close()
            # self.sell()

data=yf.download('TSLA',period='5y')
data.columns=[i[0] for i in data.columns]
print(data)

print(get_sma(data.Close,10))
# Initialize and run the backtest
bt = Backtest(data, TrailingStopLossStrategy, cash=10000, commission=.002)
stats = bt.run()

# Print the performance metrics
print(stats)

# Plot the backtest results
bt.plot()