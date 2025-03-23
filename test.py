from scrap_tiktok import query_tiktok, get_top_authors, extract_influencer_info
from product_to_query import product_description_to_query
from render_db import fetch_data
from influencerOutreach.email_function import send_simple_message
import streamlit as st
import psycopg2
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize session state for email sending
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False
    st.session_state.email_success = False
    st.session_state.email_recipient = ""
    st.session_state.email_error = ""

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

# Function to send email without refreshing the page
def send_email_callback():
    recipient = st.session_state.selected_email
    subject = st.session_state.email_subject
    message = st.session_state.email_message
    
    response = send_simple_message(
        message=message,
        recipient=recipient,
        subject=subject
    )
    
    st.session_state.email_sent = True
    st.session_state.email_recipient = recipient
    
    if response and response.status_code == 200:
        st.session_state.email_success = True
    else:
        st.session_state.email_success = False
        st.session_state.email_error = "Failed to send email. Check your Mailgun API key and configuration."

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
    
    # Display email sent notification if exists
    if st.session_state.email_sent:
        if st.session_state.email_success:
            st.success(f"✅ Email sent successfully to {st.session_state.email_recipient}!")
        else:
            st.error(st.session_state.email_error)
        
        # Add button to dismiss notification
        if st.button("Clear notification"):
            st.session_state.email_sent = False
    
    # Initialize session state for dataframe if it doesn't exist
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.has_data = False
    
    # Display dataframe if it exists
    if st.session_state.has_data and st.session_state.df is not None:
        st.dataframe(st.session_state.df, use_container_width=True)
    
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
                        
                        # Store the dataframe in session state for later use
                        st.session_state.df = df
                        st.session_state.has_data = True
                        
                        # Display the data as a table - no need for rerun as we'll display below
                        st.success(f"Successfully fetched {len(results)} records from the database!")
                        # Immediately display the dataframe
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No records found in the database.")
                        st.session_state.has_data = False
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
                    st.session_state.has_data = False
                finally:
                    conn.close()
            else:
                st.error("Failed to connect to the database. Check your DATABASE_URL environment variable.")
    
    # Only show email options if we have data
    if st.session_state.has_data and st.session_state.df is not None:
        df = st.session_state.df
        
        # Create a dropdown for selecting influencers
        st.subheader("Send Email to Influencer")
        
        # Extract names and emails for dropdown
        influencer_options = []
        for i, row in df.iterrows():
            if 'profile_name' in df.columns and 'email' in df.columns:
                if pd.notna(row['email']):
                    # Format: "Name (email@example.com)"
                    option = f"{row['profile_name']} ({row['email']})"
                    influencer_options.append((option, i, row['email'], row['profile_name']))
        
        if influencer_options:
            # Extract the display strings for the selectbox
            display_options = [opt[0] for opt in influencer_options]
            
            # Create the dropdown
            selected_option_idx = st.selectbox(
                "Select an influencer to email:",
                range(len(display_options)),
                format_func=lambda i: display_options[i]
            )
            
            # Get the selected influencer's info
            _, row_idx, email, name = influencer_options[selected_option_idx]
            selected_row = df.iloc[row_idx]
            
            # Store the email in session state
            st.session_state.selected_email = email
            
            # Email fields with keys for session state
            st.text_input(
                "Email Subject:", 
                value=f"Partnership Opportunity with {name}",
                key="email_subject"
            )
            
            st.text_area(
                "Email Message:", 
                value=f"Hi {name},\n\nWe'd like to discuss a potential partnership opportunity with you.\n\nBest regards,\nLeadFetch Team", 
                height=200,
                key="email_message"
            )
            
            # Send button with callback
            st.button("📧 Send Email", on_click=send_email_callback, type="primary")
            
        else:
            st.warning("No influencers with email addresses found in the database.")
