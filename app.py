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

@app.route('/get_chart/<currency>', methods=['GET'])
def get_chart(currency):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1920x1080")

    # Get Chrome binary and driver paths from environment
    chrome_bin = os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

    options.binary_location = chrome_bin
    service = Service(chromedriver_path)
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)

        # Example URL (CoinMarketCap)
        url_map = {
            "xrp": "https://coinmarketcap.com/ja/currencies/xrp/",
            "trx": "https://coinmarketcap.com/ja/currencies/tron/"
        }

        if currency not in url_map:
            return jsonify({"error": "Invalid currency"}), 400

        driver.get(url_map[currency])

        # Wait for SVG chart
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "highcharts-root"))
        )

        svg_element = driver.find_element(By.CLASS_NAME, "highcharts-root")
        svg_html = svg_element.get_attribute("outerHTML")

    except Exception as e:
        svg_html = f"<p>Error loading SVG: {str(e)}</p>"

    finally:
        if driver:
            driver.quit()

    return jsonify({"svg": svg_html})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
