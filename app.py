from flask import Flask,request
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data=request.det_json()
    source_currency=data['queryResult']['parameters']['unit-currency']['currency']
    amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_currency=data['queryResult']['parameters']['currency-name']

    print(source_money)
    print(amount)
    print(target_money)
    cf = fetch_conversion_factor(source_currency,target_currency)  # using conversion api
    print("cf",cf)
    return "Hello ! This is a currency_conversion_bot backend page"

def fetch_conversion_factor(source,target):
    url="https://currencyconversionapi.com/api/v1/live?access_key=46ddee37c04ebb446376e21613d3bfff"
    response=requests.get(url)
    data=response.json()
    quotes=data.get("quotes",{})
    conversion_key=f"{FROM_CURRENCY}{TO_CURRENCY}"
    rate=quotes[conversion_key]
    return rate
if __name__ == "__main__":
    app.run(debug=True)
