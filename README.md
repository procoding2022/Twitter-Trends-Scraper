# Twitter Trends Scraper

This project is a Twitter trends scraper built using Selenium and Flask. It retrieves trending topics from Twitter and displays them in a web interface. The scraper also uses ProxyMesh for rotating IP addresses for each scraping request.

## Features

- Scrapes the latest trending topics on Twitter.
- Uses ProxyMesh to rotate IP addresses for each request.
- Displays the top 5 trending topics along with the current date and time.
- Stores the scraped data in MongoDB for persistence.
- A simple Flask-based web interface for interacting with the scraper.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/procoding2022/twitter-trends-scraper.git
   cd twitter-trends-scraper
2. Create a virtual environment
   ```bash
   python -m venv venv
3. Install required dependencies
   ````bash
   pip install -r requirements.txt
4. Ensure MongoDB is running on your local machine, or update the connection string.
5. Set up your ProxyMesh credentials:
   Replace `username` and `password` in the get_proxy function with your actual ProxyMesh credentials.
6. Set up your twitter account credentials:
   Replace `username` and `password` in the scrape_twitter function with your actual Twitter credentials.
7. Run the app
   ```bash
   python app.py
8. Open your browser and navigate to http://127.0.0.1:5000 to interact with the scraper.

## Usage

Click the "Click here to run the script" button on the web interface to start scraping Twitter trends. The results will be displayed, and you can also view the raw JSON data retrieved from MongoDB.
