from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import uuid
import random

app = Flask(__name__)

# MongoDB Configuration
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client['twitter_trends']
    collection = db['trends']
    print("MongoDB connection successful!")
except ServerSelectionTimeoutError as e:
    print(f"Could not connect to MongoDB. Is it running? Error: {e}")
    raise
except PyMongoError as e:
    print(f"An error occurred with MongoDB: {e}")
    raise

import requests
from random import choice

def get_proxy():
    # proxy_url = 'https://proxymesh.com/api/proxies'
    # username = 'username'  # ProxyMesh username
    # password = 'password'  # ProxyMesh password
    # response = requests.get(proxy_url, auth=(username, password))
    
    # if response.status_code == 200:
    #     proxies = response.json()['proxies']  
    #     return choice(proxies) 
    # else:
    #     print(f"Failed to get proxy from ProxyMesh. Status code: {response.status_code}")
    #     return None
    return None 
# Due to twitter's internal security policies it is getting difficult to login with proxymesh IP address but without proxmesh program works.


def scrape_twitter():
    chrome_options = Options()
    proxy = get_proxy()
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # Twitter credentials
    TWITTER_USERNAME = "username" #username
    TWITTER_PASSWORD = "password" #password
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Login to Twitter
        driver.get("https://x.com/login")
        wait = WebDriverWait(driver, 60) 
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username_input.send_keys(TWITTER_USERNAME)
        
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button.click()
        
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.send_keys(TWITTER_PASSWORD)
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
        login_button.click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'What’s happening')]")))
        trend_spans = driver.find_elements(
            By.XPATH,
            "//div[@aria-label='Timeline: Trending now']//span[contains(@class, 'css-') and not(contains(text(), 'LIVE')) and not(contains(text(), 'Trending')) and not(contains(text(), 'posts'))]"
        )
        valid_trends = []
        for span in trend_spans:
            text = span.text.strip()
            if text and not any(kw in text for kw in ["What’s happening", "Trending", "posts", "LIVE"]):  # Filter out 'LIVE'
                valid_trends.append(text)
        print("Filtered trends:", valid_trends)
        record = {
            "_id": str(uuid.uuid4()),
            "nameoftrend1": valid_trends[0] if len(valid_trends) > 0 else "",
            "nameoftrend2": valid_trends[1] if len(valid_trends) > 1 else "",
            "nameoftrend3": valid_trends[2] if len(valid_trends) > 2 else "",
            "nameoftrend4": valid_trends[3] if len(valid_trends) > 3 else "",
            "nameoftrend5": valid_trends[4] if len(valid_trends) > 4 else "",
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": proxy if proxy else "localhost"
        }
        try:
            collection.insert_one(record)
            print(f"Successfully stored trends with ID: {record['_id']}")
        except PyMongoError as e:
            print(f"Failed to store in MongoDB. Error: {e}")
            raise
        
        return record

    except Exception as e:
        driver.save_screenshot("error_screenshot.png")
        print(f"Error occurred during scraping: {e}")
        raise
    
    finally:
        driver.quit()






@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    try:
        result = scrape_twitter()
        return jsonify(result)
    except Exception as e:
        print(f"Error occurred during scraping: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)