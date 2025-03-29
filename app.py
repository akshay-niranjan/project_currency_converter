from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    try:
        data=request.get_json()
        if not data:
            return {"fulfillmentText": "Invalid request. No JSON received."}, 400
        source_currency = data['queryResult']['parameters'].get('unit-currency', {}).get('currency')
        amount = data['queryResult']['parameters'].get('unit-currency', {}).get('amount')
        target_currency = data['queryResult']['parameters'].get('currency-name')

        if not source_currency or not target_currency or amount is None:
            return {"fulfillmentText": "Missing required parameters."}, 400


        # print(source_currency)
        # print(amount)
        # print(target_currency)
        cf = fetch_conversion_factor(source_currency,target_currency)  # using conversion api
        if cf is None:
            return jsonify({"fulfillmentText": f"Conversion rate for {source_currency} to {target_currency} not found."}), 400

        # print("cf",cf)
        final_amount=amount*cf
        resp={
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
        }
        print(final_amount)
        return jsonify(resp)
        
    except Exception as e:
        print("Error:", str(e))  # Log the error
        return {"fulfillmentText": f"Internal Server Error: {str(e)}"}, 500
def fetch_conversion_factor(source,target):
    try:
        url="https://currencyconversionapi.com/api/v1/live?access_key=46ddee37c04ebb446376e21613d3bfff"
        response=requests.get(url)
        if response.status_code != 200:
            return None  # Return None if API fails
        data=response.json()
        quotes=data.get("quotes",{})
        conversion_key=f"{source}{target}"
        rate=quotes.get(conversion_key,None)
        return rate
        
    except Exception as e:
        print("Error fetching conversion rate:", str(e))
        return None  # Return None in case of failure
if __name__ == "__main__":
    app.run(debug=True)
