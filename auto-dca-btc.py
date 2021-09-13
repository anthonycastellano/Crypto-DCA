import requests, os, csv
from dotenv import load_dotenv
from CoinbaseExchangeAuth import CoinbaseExchangeAuth

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
API_PASS = os.getenv('API_PASS')

BTC_ACCOUNT_ID = os.getenv('BTC_ACCOUNT_ID')
USD_ACCOUNT_ID = os.getenv('USD_ACCOUNT_ID')
BTC_PURC_AMT = os.getenv('BTC_PURC_AMT')

api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

# get BTC balance
r = requests.get(api_url + 'accounts/' + BTC_ACCOUNT_ID, auth=auth)
res_json = r.json()
btc_balance = res_json['balance']
print('BTC balance: ' + btc_balance)

# get USD balance
r = requests.get(api_url + 'accounts/' + USD_ACCOUNT_ID, auth=auth)
res_json = r.json()
usd_balance = res_json['balance']
print('USD balance: ' + usd_balance)

# get BTC/USD price
r = requests.get(api_url + 'products/BTC-USD/ticker')
res_json = r.json()
btc_price = res_json['price']
print('BTC Price (USD): $' + btc_price)

# purchase amount
amount_to_purchase = round(float(BTC_PURC_AMT) / float(btc_price), 8)
print('Trading $' + BTC_PURC_AMT + ' of USD for ' + str(amount_to_purchase) + ' BTC')

# post order
payload = {
    'type': 'market',
    'side': 'buy',
    'product_id': 'BTC-USD',
    'size': amount_to_purchase
}
r = requests.post(api_url + 'orders', params=payload)
res_json = r.json()
orderDetails = {
    'id': res_json['id'],
    'price': res_json['price'],
    'size': res_json['size'],
    'status': res_json['status'],
    'fill_fees': res_json['fill_fees'],
    'created_at': res_json['created_at']
}
print('Order submitted:\n\tid:\t' + orderDetails['id']
        + '\n\tprice:\t' + orderDetails['price']
        + '\n\tsize:\t' + orderDetails['size']
        + '\n\tstatus:\t' + orderDetails['status']
        + '\n\tfees:\t' + orderDetails['fill_fees']
        + '\n\tcreated at:\t' + orderDetails['created_at'])

# write to csv file
row = [orderDetails['created_at'], 'BTC', orderDetails['price'], orderDetails['size'], orderDetails['fill_fees']]
with open('orders.csv', 'a') as file:
    writer = csv.writer(file)
    writer.writerow(row)