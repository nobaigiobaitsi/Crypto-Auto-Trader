import ccxt
import time
import yfinance as yf


api_key = "An API Key"
api_secret = "A Secret API Key"

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'test': True
})

symbol = "SUI/USDT"

#The thresholds should be adjusted based on the risk factors willing to take.
buy_threshold = 0.99
sell_threshold = 1.01
funds = 100 #$ This is adjustable depending on the available funds.

def calculate_amount_to_buy(price, funds):
    """
    Calculate how much of the cryptocurrency you can buy with the available funds.
    """
    return funds / price

def get_crypto_price(symbol="SUI/USDT"):
    ticker = exchange.fetch_ticker(symbol)
    return ticker["last"]

def buy_order(symbol, amount):
    order_price = get_crypto_price(symbol)
    print(f"Buying {amount} {symbol} at {order_price}")
    return {'symbol': symbol, 'side': 'buy', 'amount': amount, 'price': order_price}

def sell_order(symbol, amount):
    order_price = get_crypto_price(symbol)
    print(f"Selling {amount} {symbol} at {order_price}.")
    return {'symbol': symbol, 'side': 'sell', 'amount': amount, 'price': order_price}

def auto_trade():
    global funds
    amount = 10 #This has to be adjusted based on amount available
    previous_price = get_crypto_price(symbol)
    while True:
        current_price = get_crypto_price(symbol)
        print(f"Current price of {symbol}: {current_price}")
        if current_price <= previous_price * buy_threshold:
            print("The price has dropped, placinc buy order")
            amount_to_buy = calculate_amount_to_buy(current_price, funds)
            buy_order(symbol, amount_to_buy)
            funds -= amount_to_buy * current_price
            previous_price = current_price
        elif current_price >= previous_price * sell_threshold:
            print("The price has increased, placing sell order")
            sell_order(symbol, amount_to_buy)
            funds += amount_to_buy * current_price
            previous_price = current_price
        #This should be adjusted based on the timer the exchanges should happen.
        #Currently set at 0.5 minute(30 seconds).
        time.sleep(30)



if __name__ == "__main__":
    auto_trade()
