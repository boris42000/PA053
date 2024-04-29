from flask import Flask, request, jsonify, make_response
import requests
import sympy
import json

app = Flask(__name__)

API_KEY = 'b6f45c5a99msh9c8e584ecba5a6fp15609ajsnb0e6d595e3f4'

@app.route('/', methods=['GET'])
def service():
    headers = {
                'x-rapidapi-key': API_KEY,
                'Accept': 'application/json'
               }
    
    if 'queryAirportTemp' in request.args:
        code = request.args['queryAirportTemp']
        url = f"https://api.weatherapi.com/v1/current.json?q=iata:{code}"
        response = requests.get(url,  headers=headers)
        data = response.json()
        json = {"temperature": data['current']['temp_c']}
    
    elif 'queryStockPrice' in request.args:
        symbol = request.args['queryStockPrice']
        url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?symbols={symbol}"
        response = requests.get(url, headers=headers)
        data = response.json()
        json = {"stock_price": data['price']['regularMarketPrice']['raw']} 

    elif 'queryEval' in request.args:
        expression = request.args['queryEval']
        try:
            expr = sympy.sympify(expression)
            result = float(expr.evalf())
        except Exception as e:
            result = str(e)
        json = {"result": result}
    else:
        return make_response("Invalid request", 400)
    return make_response(jsonify(json), 200, {'Content-Type': 'application/json'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
