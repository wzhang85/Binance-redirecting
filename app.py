from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BINANCE_BASE_URL = "https://api.binance.com"

@app.route('/')
def home():
    return "Binance API Redirect Service is Running!"

@app.route('/binance/<path:endpoint>', methods=['GET', 'POST'])
def binance_api(endpoint):
    """ Forwards requests to Binance API, ensuring signed parameters are preserved. """

    binance_url = f"{BINANCE_BASE_URL}/{endpoint}"
    
    # Preserve query parameters (including signature)
    params = request.args.to_dict()
    headers = {
        "X-MBX-APIKEY": request.headers.get("X-MBX-APIKEY")
    }

    try:
        # Send the request to Binance
        response = requests.get(binance_url, params=params, headers=headers)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
