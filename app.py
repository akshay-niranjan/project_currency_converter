from flask import Flask,request

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data=request.det_json()
    return data

if __name__ == "__main__":
    app.run(debug=True)
