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


foreign_exchange = {
    "base_currency": "USD",
    "exchange_rates": {
        "EUR": {
            "current_rate": 0.85,
            "historical_rates": [
                {"date": "2024-01-10", "rate": 0.84},
                {"date": "2024-01-09", "rate": 0.85}
            ]
        },
        "JPY": {
            "current_rate": 110.00,
            "historical_rates": [
                {"date": "2024-01-10", "rate": 109.50},
                {"date": "2024-01-09", "rate": 110.20}
            ]
        }
    }
}
r=foreign_exchange.get('exchange_rates').get('JPY').get('historical_rates')[1].get('rate')
print(r)


credit_risk_profiles = {
    "individuals": [
        {
            "name": "John Doe",
            "credit_score": 750,
            "outstanding_loans": {
                "auto_loan": {"amount": 20000, "interest_rate": 3.5},
                "home_loan": {"amount": 150000, "interest_rate": 2.8}
            },
            "payment_history": [("2024-01-10", "On Time"), ("2024-01-01", "Late")]
        },
        {
            "name": "Jane Smith",
            "credit_score": 680,
            "outstanding_loans": {
                "credit_card": {"amount": 5000, "interest_rate": 12.0}
            },
            "payment_history": [("2024-01-10", "On Time")]
        }
    ]
}
i=credit_risk_profiles.get('individuals')[0].get('outstanding_loans').get('home_loan').get('interest_rate')
print(i)


investment_portfolio = {
    "investor_name": "Jane Doe",
    "portfolio_id": "JD1234",
    "assets": {
        "stocks": [
            {
                "ticker": "AAPL",
                "quantity": 50,
                "purchase_price": 120.00,
                "current_price": 130.00
            },
            {
                "ticker": "MSFT",
                "quantity": 30,
                "purchase_price": 200.00,
                "current_price": 210.00
            }
        ],
        "bonds": [
            {
                "identifier": "US123456",
                "quantity": 100,
                "purchase_price": 1000.00,
                "current_price": 1020.00,
                "maturity_date": "2030-01-01"
            }
        ],
        "mutual_funds": [
            {
                "name": "XYZ Growth Fund",
                "quantity": 200,
                "purchase_price": 15.00,
                "current_price": 15.50
            }
        ]
    },
    "cash_holdings": 10000.00,
    "investment_goals": {"retirement": 2035, "education": 2025}
}

cp=investment_portfolio.get('assets').get('stocks')[1].get('purchase_price')
print(cp)

investment_portfolio.get('assets').get('stocks')[1].pop('current_price')
print(investment_portfolio.get('assets').get('stocks')[1])