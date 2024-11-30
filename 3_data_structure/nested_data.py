hedge_fund_portfolio = {
    "fund_name": "Alpha Investments",
    "portfolio_value": 5_00_00_000,
    "investments": [

        {
            "type": "Equity",
            "holdings": [
                {"ticker": "AAPL", "quantity": 10000, "average_buy_price": 120},
                {"ticker": "TSLA", "quantity": 5000, "average_buy_price": 600}
            ]
        },

        {
            "type": "Fixed Income",
            "holdings": [
                {"bond_issue": "US Treasuries", "amount": 10000000, "yield": 1.5}
            ]
        },

        {
            "type": "Derivatives",
            "holdings": [
                {"instrument": "Options", "details": {"underlying": "GOOGL", "type": "Call", "strike_price": 1500}}
            ]
        }

    ],
    "performance_metrics": {
        "year_to_date_return": 5.2,
        "five_year_annualized_return": 7.1
    }
}


#read write update del
apple_value=hedge_fund_portfolio.get('investments')[0].get('holdings')[0].get('average_buy_price')
print(apple_value)

yield_value=hedge_fund_portfolio.get('investments')[1].get('holdings')[0].get('yield')
print(yield_value)

a={"quantity": 6000}
hedge_fund_portfolio.get('investments')[0].get('holdings')[1].update(a)
print(hedge_fund_portfolio.get('investments')[0].get('holdings')[1])

hedge_fund_portfolio.get('investments')[2].get('holdings')[0].get('details').update({'strike_price':1700})
print(hedge_fund_portfolio.get('investments')[2].get('holdings')[0].get('details').get('strike_price'))