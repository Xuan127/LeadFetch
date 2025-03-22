from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse
from render_db import fetch_data, insert_data, update_data
from scrap_tiktok import query_tiktok, get_top_authors

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create a connection to the PostgreSQL database."""
    result = urlparse(os.getenv("DATABASE_URL"))
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    
    return psycopg2.connect(
        user=username,
        password=password,
        host=hostname,
        port="5432",
        database=database
    )

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({"status": "healthy", "message": "Flask API is running"}), 200

@app.route('/api/influencers', methods=['GET'])
def get_influencers():
    """Get all influencers from the database."""
    try:
        conn = get_db_connection()
        results = fetch_data(conn, 'leads')
        
        influencers = []
        for result in results:
            # Map database columns to JSON response
            # Adjust column indices based on your actual schema
            influencer = {
                'id': result[0],
                'name': result[1],  # profile_name
                'followers': result[2],  # fans
                'hearts': result[3],
                'videos': result[4],
                'platform': result[5],
                'email': result[6],
                'leadStage': result[7],
                'contractVideo': result[8],
                'createdAt': result[9].isoformat() if result[9] else None,
                'contractShares': result[10],
                'contractPlays': result[11],
                'contractComments': result[12]
            }
            influencers.append(influencer)
        
        conn.close()
        return jsonify(influencers)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/influencers/search', methods=['POST'])
def search_influencers():
    """Search for influencers using TikTok API."""
    data = request.json
    query = data.get('query', '')
    top_k = data.get('limit', 10)
    
    try:
        # Use the existing scraping functionality
        tiktok_data = query_tiktok(query)
        top_influencers = get_top_authors(tiktok_data, top_k)
        
        # Store the results in the database
        conn = get_db_connection()
        for profile in top_influencers:
            profile_name = profile["authorMeta"]['name']
            fans = profile["authorMeta"]['fans']
            hearts = profile["authorMeta"]['hearts']
            videos = profile["authorMeta"]['videos']
            
            insert_data(conn, 'leads', {
                'profile_name': profile_name,
                'fans': fans,
                'hearts': hearts,
                'videos': videos,
                'platform': 'tiktok',
                'email': profile_name + '@gmail.com',
                'lead_stage': 'prospect'
            })
        
        conn.close()
        return jsonify(top_influencers)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/briefs', methods=['POST'])
def create_brief():
    """Create a new client brief."""
    data = request.json
    response = {
        "id": data.get('id', None) or int(round(time.time() * 1000)),
        "name": data.get('clientName', 'Unnamed Brief'),
        "type": data.get('type', 'generated'),
        "clientName": data.get('clientName', ''),
        "productService": data.get('productService', ''),
        "targetAudience": data.get('targetAudience', ''),
        "campaignGoal": data.get('campaignGoal', ''),
        "influencerType": data.get('influencerType', ''),
        "date": data.get('date', '')
    }
    
    return jsonify(response)

@app.route('/api/contact', methods=['POST'])
def contact_influencer():
    """Send contact request to an influencer."""
    data = request.json
    influencer_id = data.get('influencerId')
    message = data.get('message')
    
    # In a real app, this would send an email or notification
    # For now, we'll just update the lead stage in the database
    
    try:
        conn = get_db_connection()
        update_data(
            conn, 
            'leads', 
            {'lead_stage': 'contacted'}, 
            f"id = {influencer_id}"
        )
        conn.close()
        
        return jsonify({
            "success": True,
            "message": f"Contact request sent to influencer {influencer_id}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
