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

def query_tiktok(query):
    # Prepare the Actor input
    run_input = {
        "excludePinnedPosts": False,
        "resultsPerPage": 20,
        "searchQueries": [
            query
        ],
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
    return items

def get_top_authors(data, top_k):
    # Sort the list by 'playCount' in descending order
    sorted_data = sorted(data, key=lambda item: item['authorMeta']["fans"], reverse=True)
    # Extract the 'authorMeta.name' from the top x items
    return [item for item in sorted_data[:top_k]]

def extract_influencer_info(data):
    influencer_data = []
    for profile in data:
        profile_name = profile["authorMeta"]['name']
        fans = profile["authorMeta"]['fans']
        hearts = profile["authorMeta"]['heart']
        videos = profile["authorMeta"]['video']
        
        # Prepare influencer record for dataframe display
        influencer_record = {
            'profile_name': profile_name,
            'fans': fans,
            'hearts': hearts,
            'videos': videos,
            'platform': 'tiktok',
            'email': profile_name + '@gmail.com',
            'lead_stage': 'prospect'
        }
        influencer_data.append(influencer_record)
        
        # Also save to database
        result = urlparse(os.getenv("DATABASE_URL"))
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname

        conn = None  # Initialize connection to None

        try:
            conn = psycopg2.connect(
            user=username,
            password=password,
            host=hostname,
            port="5432",
            database=database
            )

            insert_data(conn, 'leads', influencer_record)
        except Exception as e:
            print(f"Database connection error: {e}")
        finally:
            if conn:
                conn.close()
                
    # Return data for display
    return influencer_data


if __name__ == "__main__":
    query = "AI tools"
    data = query_tiktok(query)
    top_authors = get_top_authors(data, 10)
    print(top_authors)
