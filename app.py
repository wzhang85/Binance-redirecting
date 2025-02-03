from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BINANCE_BASE_URL = "https://api.binance.com"

@app.route('/')
def home():
    return "Binance API Redirect Service is Running!"

@app.route('/binance/<path:endpoint>', methods=['GET', 'POST'])
def binance_api(endpoint):
    """
    Calls the Binance API and returns the response.
    """
    # Build the Binance API URL
    binance_url = f"{BINANCE_BASE_URL}/{endpoint}"

    # Get request parameters
    params = request.args
    headers = {"Content-Type": "application/json"}

    try:
        # Determine request method (GET or POST)
        if request.method == 'GET':
            response = requests.get(binance_url, params=params, headers=headers)
        elif request.method == 'POST':
            response = requests.post(binance_url, json=request.json, headers=headers)

        # Return Binance API response
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
