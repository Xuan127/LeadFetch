from scrap_tiktok import query_tiktok, get_top_authors, extract_influencer_info
from product_to_query import product_description_to_query
from render_db import fetch_data
import streamlit as st
import psycopg2
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Function to establish database connection
def get_db_connection():
    try:
        result = urlparse(os.getenv("DATABASE_URL"))
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        
        conn = psycopg2.connect(
            user=username,
            password=password,
            host=hostname,
            port="5432",
            database=database
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Set page title
st.title("TikTok Influencer Finder")

# Create tabs
tab1, tab2 = st.tabs(["Find Influencers", "Database Records"])

with tab1:
    # Text area for product brief input
    product_brief = st.text_area("Enter Product Brief", value="iphone 15", height=150, 
                                help="Describe your product in detail to find relevant influencers")

    # Add a button to trigger the process
    if st.button("Find Influencers"):
        with st.spinner("Processing your request..."):
            # Convert product brief to query
            st.subheader("Generated Query")
            query = product_description_to_query(product_brief)
            st.write(query.text)
            
            # Query TikTok
            st.subheader("Querying TikTok")
            data = query_tiktok(query.text)
            
            # Get top authors
            st.subheader("Top Authors")
            top_authors = get_top_authors(data, 10)
            st.write(f"Found {len(top_authors)} top authors")
            
            # Extract influencer info
            st.subheader("Influencer Information")
            influencer_info = extract_influencer_info(top_authors)
            
            # Display results in a more structured way
            if influencer_info:
                st.success("Successfully retrieved influencer information!")
                try:
                    # Try to display as a dataframe if possible
                    st.dataframe(influencer_info)
                except:
                    # Fallback to displaying the raw data
                    st.json(influencer_info)

with tab2:
    st.subheader("Database Records")
    
    # Button to refresh data
    if st.button("Fetch Records"):
        with st.spinner("Fetching data from database..."):
            # Connect to database
            conn = get_db_connection()
            
            if conn:
                # Fetch data from the leads table
                try:
                    results = fetch_data(conn, 'leads')
                    
                    if results:
                        # Get column names for the leads table
                        cursor = conn.cursor()
                        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'leads' ORDER BY ordinal_position")
                        columns = [col[0] for col in cursor.fetchall()]
                        
                        # Create a pandas DataFrame with the results
                        df = pd.DataFrame(results, columns=columns)
                        
                        # Display the data as a table
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Successfully fetched {len(results)} records from the database!")
                    else:
                        st.info("No records found in the database.")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
                finally:
                    conn.close()
            else:
                st.error("Failed to connect to the database. Check your DATABASE_URL environment variable.")
