from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data=request.get_json()
    if not data:
            return {"fulfillmentText": "Invalid request. No JSON received."}, 400
    source_currency=data['queryResult']['parameters']['unit-currency']['currency']
    amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_currency=data['queryResult']['parameters']['currency-name']

    # print(source_currency)
    # print(amount)
    # print(target_currency)
    cf = fetch_conversion_factor(source_currency,target_currency)  # using conversion api
    # print("cf",cf)
    final_amount=amount*cf
    resp={
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    print(final_amount)
    return jsonify(response)

def fetch_conversion_factor(source,target):
    url="https://currencyconversionapi.com/api/v1/live?access_key=46ddee37c04ebb446376e21613d3bfff"
    response=requests.get(url)
    data=response.json()
    quotes=data.get("quotes",{})
    conversion_key=f"{source}{target}"
    rate=quotes[conversion_key]
    return rate
if __name__ == "__main__":
    app.run(debug=True)
