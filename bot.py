import ccxt
import time
from config import API_KEY, API_SECRET, EXCHANGE_ID

symbol = 'BTC/USDT'
amount = 0.001  # Position size
entry_price = 26500.0  # custom entry
take_profit_pct = 0.02  # 2%
stop_loss_pct = 0.01  # 1%

exchange = getattr(ccxt, EXCHANGE_ID)({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
})

def get_price(symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

def place_order(entry_price, tp_price, sl_price):
    print(f"Placing market order at {entry_price}, TP: {tp_price}, SL: {sl_price}")
    # Place entry
    order = exchange.create_market_buy_order(symbol, amount)

    # Place TP
    tp_order = exchange.create_limit_sell_order(symbol, amount, tp_price)

    # Place SL (simulate using polling — or use OCO/stop-limit if supported)
    return order, tp_order

print("Trading bot started...")

position_opened = False

while True:
    try:
        current_price = get_price(symbol)
        print(f"Current price: {current_price}")

        if not position_opened and current_price <= entry_price:
            take_profit_price = round(entry_price * (1 + take_profit_pct), 2)
            stop_loss_price = round(entry_price * (1 - stop_loss_pct), 2)

            place_order(entry_price, take_profit_price, stop_loss_price)
            position_opened = True
            entry_time = time.time()

        # Simulate stop-loss check
        if position_opened:
            if current_price <= stop_loss_price:
                print("Stop loss hit. Selling position...")
                exchange.create_market_sell_order(symbol, amount)
                position_opened = False

            elif current_price >= take_profit_price:
                print("Take profit hit. Position should close via limit order.")
                position_opened = False

        time.sleep(10)  # interval

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
