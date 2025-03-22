from apify_client import ApifyClient
import os
from dotenv import load_dotenv
from render_db import insert_data
from urllib.parse import urlparse
import psycopg2

load_dotenv()

# Initialize the ApifyClient with your Apify API token
# Replace '<YOUR_API_TOKEN>' with your token.
client = ApifyClient(os.getenv("APIFY_API_KEY"))

def scrap_performance(vid_url):
    # Prepare the Actor input
    run_input = {
        "excludePinnedPosts": False,
        "postURLs": [
            vid_url
        ],
        "resultsPerPage": 100,
        "searchSection": "/video",
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": False
    }

    # Run the Actor and wait for it to finish
    run = client.actor("clockworks/free-tiktok-scraper").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
    items = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        items.append(item)
    
    vid = items[0]

    created_time = vid["createTimeISO"]
    shares = vid["shareCount"]
    plays = vid["playCount"]
    comments = vid["commentCount"]