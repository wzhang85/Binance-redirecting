from flask import Flask, request, jsonify
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import chromedriver_autoinstaller

app = Flask(__name__)

BINANCE_BASE_URL = "https://api.binance.com"

@app.route('/')
def home():
    return "Binance API Redirect Service is Running!"

@app.route('/get_chart/<currency>', methods=['GET'])
def get_chart(currency):
    """Fetch chart SVG from CoinMarketCap using Selenium"""

    # Automatically install compatible chromedriver
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1920x1080")

    # Explicitly set Google Chrome binary location
    options.binary_location = "/usr/bin/google-chrome"

    driver = None
    try:
        driver = webdriver.Chrome(options=options)

        url_map = {
            "xrp": "https://coinmarketcap.com/ja/currencies/xrp/",
            "trx": "https://coinmarketcap.com/ja/currencies/tron/"
        }

        if currency not in url_map:
            return jsonify({"error": "Invalid currency"}), 400

        driver.get(url_map[currency])

        # Wait for the SVG chart to load
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
