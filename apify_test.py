from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the ApifyClient with your Apify API token
# Replace '<YOUR_API_TOKEN>' with your token.
client = ApifyClient(os.getenv("APIFY_API_KEY"))

# Prepare the Actor input
run_input = {
    "searchTerms": ["apify"],
    "sort": "Latest",
    "maxItems": 1000,
}

# Run the Actor and wait for it to finish
run = client.actor("apidojo/twitter-scraper-lite").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)

# 📚 Want to learn more 📖? Go to → https://docs.apify.com/api/client/python/docs/quick-start