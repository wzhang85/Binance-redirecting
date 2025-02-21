from flask import Flask, request, jsonify
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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

@app.route('/get_chart/<currency>', methods=['GET'])
def get_chart(currency):
    """Fetch chart SVG from CoinMarketCap using Selenium"""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode for cloud environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1920x1080")

    # Set Chrome binary and driver path from Render environment variables
    chrome_bin = os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

    options.binary_location = chrome_bin
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url_map = {
        "xrp": "https://coinmarketcap.com/ja/currencies/xrp/",
        "trx": "https://coinmarketcap.com/ja/currencies/tron/"
    }

    if currency not in url_map:
        return jsonify({"error": "Invalid currency"}), 400

    try:
        url = url_map[currency]
        driver.get(url)

        # Wait for the SVG chart to load
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "highcharts-root"))
        )

        # Extract the SVG chart
        svg_element = driver.find_element(By.CLASS_NAME, "highcharts-root")
        svg_html = svg_element.get_attribute("outerHTML")

    except Exception as e:
        svg_html = f"<p>Error loading SVG: {str(e)}</p>"

    finally:
        driver.quit()

    return jsonify({"svg": svg_html})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
