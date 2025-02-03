from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return "Binance API Redirect Service is Running!"

@app.route('/binance/<path:url>')
def binance_redirect(url):
    binance_url = f"https://api.binance.com/{url}"
    return redirect(binance_url, code=302)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
