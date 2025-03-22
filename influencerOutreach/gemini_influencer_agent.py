"""
Gemini-Powered Influencer Marketing Agent

This agent uses Google's Gemini API to intelligently identify and contact 
potential influencer marketers to form business partnerships with a client company.
It demonstrates function calling with Gemini similar to the Google example.
"""

import json
import time
import logging
import os
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

# Import Google Generative AI library
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
def setup_logging(log_file='agent_logs.log'):
    """
    Set up logging to both console and file
    
    Args:
        log_file: Path to the log file
    """
    # Create logs directory if it doesn't exist
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_path = os.path.join(logs_dir, log_file)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    logging.info(f"Logging initialized. Logs will be saved to: {log_path}")
    return log_path

# Call setup_logging to initialize
log_file_path = setup_logging()

# Add this utility function after imports, before the mock functions
def convert_to_serializable(obj):
    """
    Convert Google Generative AI response objects to JSON-serializable Python types.
    Handles MapComposite, RepeatedComposite, and other non-serializable types.
    
    Args:
        obj: Any object, potentially containing non-serializable types
        
    Returns:
        JSON-serializable version of the object
    """
    # Handle dictionaries and dict-like objects
    if hasattr(obj, "items"):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    
    # Handle lists, tuples and other iterables (except strings)
    elif isinstance(obj, (list, tuple)) or (hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, dict))):
        return [convert_to_serializable(item) for item in obj]
    
    # Return primitive types as is
    return obj

# Mock functions for database and email operations
def mock_query_database(query: str) -> List[Dict[str, Any]]:
    """
    Mock function to query a PostgreSQL database.
    
    Args:
        query: SQL query string
        
    Returns:
        List of dictionaries representing database records
    """
    logging.info(f"Executing database query: {query}")
    
    # Mock data for influencers
    if "influencers" in query.lower():
        return [
            {
                "id": 1,
                "name": "Alex Johnson",
                "email": "alex@influencer.com",
                "followers": 150000,
                "niche": "fitness",
                "engagement_rate": 3.5,
                "previous_partnerships": 12,
                "location": "Los Angeles, CA",
                "content_quality": "high",
                "audience_demographics": {"age": "25-34", "gender": "mixed"}
            },
            {
                "id": 2,
                "name": "Taylor Smith",
                "email": "taylor@contentcreator.com",
                "followers": 250000,
                "niche": "beauty",
                "engagement_rate": 4.2,
                "previous_partnerships": 8,
                "location": "New York, NY",
                "content_quality": "premium",
                "audience_demographics": {"age": "18-29", "gender": "female"}
            },
            {
                "id": 3,
                "name": "Jordan Lee",
                "email": "jordan@socialmedia.com",
                "followers": 500000,
                "niche": "tech",
                "engagement_rate": 2.8,
                "previous_partnerships": 20,
                "location": "San Francisco, CA",
                "content_quality": "high",
                "audience_demographics": {"age": "25-40", "gender": "male"}
            },
            {
                "id": 4,
                "name": "Morgan Chen",
                "email": "morgan@lifestyleblog.com",
                "followers": 320000,
                "niche": "lifestyle",
                "engagement_rate": 3.9,
                "previous_partnerships": 15,
                "location": "Chicago, IL",
                "content_quality": "high",
                "audience_demographics": {"age": "30-45", "gender": "mixed"}
            }
        ]
    
    # Mock data for client companies
    elif "companies" in query.lower():
        return [
            {
                "id": 1,
                "name": "FitLife Products",
                "industry": "fitness",
                "product_types": ["supplements", "workout gear"],
                "target_audience": "health enthusiasts",
                "budget": 50000,
                "brand_values": ["quality", "authenticity", "results"],
                "campaign_goals": ["brand awareness", "product sales"]
            }
        ]
    
    # Mock data for campaign performance
    elif "campaign_performance" in query.lower():
        return [
            {
                "campaign_id": 101,
                "influencer_id": 1,
                "engagement": 4500,
                "clicks": 1200,
                "conversions": 85,
                "roi": 3.2
            },
            {
                "campaign_id": 102,
                "influencer_id": 3,
                "engagement": 7800,
                "clicks": 2100,
                "conversions": 130,
                "roi": 2.8
            }
        ]
    
    # Default empty response
    return []

def mock_check_emails(email_filter: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Mock function to check emails.
    
    Args:
        email_filter: Dictionary with filter criteria
        
    Returns:
        List of dictionaries representing emails
    """
    logging.info(f"Checking emails with filter: {email_filter}")
    
    # Mock data for emails
    return [
        {
            "id": "email123",
            "from": "jordan@socialmedia.com",
            "to": "partnerships@clientcompany.com",
            "subject": "Interested in partnership opportunity",
            "body": "Hello, I saw your products and I'm interested in a potential collaboration. I believe my tech-focused audience would be a great fit for your fitness products, especially those with smart features. Could we discuss partnership terms? I'm looking for a 3-month contract with at least $5000 per sponsored post. Let me know if this aligns with your budget.",
            "date": "2025-03-20T09:15:00Z",
            "read": False
        },
        {
            "id": "email124",
            "from": "taylor@contentcreator.com",
            "to": "partnerships@clientcompany.com",
            "subject": "Re: Partnership Opportunity with FitLife Products",
            "body": "Thank you for reaching out! I'm definitely interested in working with FitLife Products. I've been looking for more fitness-related partnerships to complement my beauty content. My audience has been asking for more holistic wellness recommendations. Can we set up a call next week to discuss details?",
            "date": "2025-03-21T14:22:00Z",
            "read": False
        }
    ]

def mock_send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Mock function to send an email.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        
    Returns:
        Dictionary with email send status
    """
    logging.info(f"\nSending email to: {to}")
    logging.info(f"Subject: {subject}")
    logging.info(f"Body: {body}")
    
    return {
        "status": "sent",
        "message_id": f"msg_{int(time.time())}",
        "recipient": to,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

# Define the tools (functions) that will be available to the Gemini model
def find_influencers(niche: str, min_followers: int, min_engagement_rate: float) -> str:
    """
    Find influencers matching specific criteria.
    
    Args:
        niche: Content niche (e.g., fitness, beauty, tech)
        min_followers: Minimum number of followers required
        min_engagement_rate: Minimum engagement rate percentage
        
    Returns:
        JSON string with matching influencers
    """
    query = f"SELECT * FROM influencers WHERE niche = '{niche}' AND followers >= {min_followers} AND engagement_rate >= {min_engagement_rate}"
    results = mock_query_database(query)
    return json.dumps(results)

def analyze_email_response(email_body: str) -> str:
    """
    Analyze an email response from an influencer to determine sentiment and key points.
    
    Args:
        email_body: The body text of the email
        
    Returns:
        JSON string with analysis results
    """
    # Use Gemini to analyze the email
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""Analyze the following email response from an influencer. Extract the following information:
    1. Overall sentiment (positive, neutral, or negative)
    2. Key points mentioned
    3. Any requested compensation amounts
    4. Any timeline mentioned
    5. Any questions asked
    
    Format your response as a JSON object with these keys: sentiment, key_points (array), 
    requested_compensation (string or null), timeline_mentioned (string or null), 
    questions_asked (array).
    
    Email body:
    {email_body}
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Try to parse the response as JSON
        analysis = json.loads(response.text)
    except json.JSONDecodeError:
        # If parsing fails, create a basic structure and extract what we can
        analysis = {
            "sentiment": "positive" if "interested" in email_body.lower() else "neutral",
            "key_points": [],
            "requested_compensation": None,
            "timeline_mentioned": None,
            "questions_asked": []
        }
        
        # Extract some basic information
        if "budget" in email_body.lower() or "$" in email_body:
            analysis["key_points"].append("Discussed compensation")
        if "call" in email_body.lower() or "meet" in email_body.lower():
            analysis["key_points"].append("Requested meeting")
        if "next week" in email_body.lower():
            analysis["key_points"].append("Proposed timeline")
            analysis["timeline_mentioned"] = "next week"
        if "?" in email_body:
            analysis["key_points"].append("Asked questions")
    return json.dumps(analysis)

def draft_response_email(influencer_name: str, influencer_niche: str, sentiment: str, key_points: List[str]) -> str:
    """
    Draft a response email to an influencer based on their previous communication.
    
    Args:
        influencer_name: Name of the influencer
        influencer_niche: Content niche of the influencer
        sentiment: Sentiment of their previous email
        key_points: Key points from their previous email
        
    Returns:
        JSON string with draft email subject and body
    """
    # Use Gemini to generate the email
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    Draft a professional response email to an influencer with the following details:
    - Influencer name: {name}
    - Influencer niche: {niche}
    - Sentiment of their previous email: {sentiment}
    - Key points they mentioned: {key_points}
    
    The email should be from the partnerships team at FitLife Products, a fitness company.
    It should address each of the key points mentioned by the influencer.
    
    Format your response as a JSON object with these keys: subject, body.
    The subject should be professional and reference the partnership discussion.
    The body should be well-formatted with appropriate paragraphs, greeting, and closing.
    """.format(
        name=influencer_name,
        niche=influencer_niche,
        sentiment=sentiment,
        key_points=', '.join(key_points)
    )
    
    response = model.generate_content(prompt)
    
    try:
        # Try to parse the response as JSON
        email_content = json.loads(response.text)
    except json.JSONDecodeError:
        # If parsing fails, create a basic template response
        subject = "RE: Partnership Discussion - FitLife Products"
        
        # Start with greeting
        body = f"Hello {influencer_name},\n\nThank you for your response regarding a potential partnership with FitLife Products.\n\n"
        
        # Add personalized content based on sentiment and key points
        if sentiment == "positive":
            body += "We're thrilled to hear about your interest in working with us! "
        else:
            body += "We appreciate your consideration of our partnership opportunity. "
        
        body += f"Your expertise in the {influencer_niche} space aligns well with our brand values.\n\n"
        
        # Address key points
        if "Discussed compensation" in key_points:
            body += "Regarding compensation, we typically work with a flexible budget based on campaign specifics and performance metrics. We'd be happy to discuss the details of our compensation structure during our call.\n\n"
        
        if "Requested meeting" in key_points:
            body += "We would love to set up a call to discuss this partnership further. How does next Tuesday or Wednesday at 2:00 PM EST work for your schedule?\n\n"
        
        # Closing
        body += "Looking forward to potentially working together and creating some amazing content for your audience.\n\nBest regards,\nAI Assistant\nPartnerships Team\nFitLife Products"
        
        email_content = {"subject": subject, "body": body}
    
    return json.dumps(email_content)

def get_campaign_performance(influencer_id: int) -> str:
    """
    Get performance metrics for previous campaigns with an influencer.
    
    Args:
        influencer_id: ID of the influencer
        
    Returns:
        JSON string with campaign performance data
    """
    # For now, we'll still use the mock database function since we don't have a real database
    query = f"SELECT * FROM campaign_performance WHERE influencer_id = {influencer_id}"
    results = mock_query_database(query)
    return json.dumps(results)

class GeminiInfluencerAgent:
    """
    Agent that uses Google's Gemini API to intelligently identify and contact
    potential influencer marketers to form business partnerships.
    """
    
    def __init__(
        self, 
        client_company_id: int,
        database_query_function: Callable = mock_query_database,
        email_check_function: Callable = mock_check_emails,
        email_send_function: Callable = mock_send_email,
        api_key: Optional[str] = None
    ):
        """
        Initialize the agent with the client company ID and necessary functions.
        
        Args:
            client_company_id: ID of the client company
            api_key: Google API key for Gemini (optional in mock version)
            database_query_function: Function to query the database
            email_check_function: Function to check emails
            email_send_function: Function to send emails
        """
        self.client_company_id = client_company_id
        self.db_query = database_query_function
        self.check_emails = email_check_function
        self.send_email = email_send_function
        
        # Load client company data
        self.client_company = self._get_client_company()
        
        # Store processed influencers to avoid duplicate outreach
        self.contacted_influencers = set()
        
        # Initialize Gemini API
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Use API key from environment variable
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("No Gemini API key provided. Set GEMINI_API_KEY in .env file or pass as parameter.")
            genai.configure(api_key=api_key)
            
        # Initialize the model with tools
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            tools=[
                find_influencers,
                analyze_email_response,
                draft_response_email,
                get_campaign_performance
            ]
        )
        self.chat = self.model.start_chat()
        
        print("Initialized GeminiInfluencerAgent for", self.client_company["name"])
        
    def _get_client_company(self) -> Dict[str, Any]:
        """
        Get client company information from the database.
        
        Returns:
            Dictionary with client company data
        """
        query = f"SELECT * FROM companies WHERE id = {self.client_company_id}"
        results = self.db_query(query)
        
        if not results:
            raise ValueError(f"No company found with ID {self.client_company_id}")
            
        return results[0]
    
    def _call_gemini_function(self, prompt: str, function_name: str, function_args: Dict[str, Any]) -> Any:
        """
        Call a Gemini function with the appropriate tool.
        
        Args:
            prompt: The prompt to send to Gemini
            function_name: Name of the function to call
            function_args: Arguments to pass to the function
            
        Returns:
            Result of the function call
        """
        logging.info("\n--- Gemini Function Call ---")
        logging.info(f"Prompt: {prompt}")
        logging.info(f"Function: {function_name}")
        logging.info(f"Arguments: {json.dumps(function_args, indent=2)}")
        
        # Create function calling config to force use of the specific function
        from google.generativeai.types import content_types
        tool_config = content_types.to_tool_config(
            {"function_calling_config": {"mode": "any", "allowed_function_names": [function_name]}}
        )
        
        # Call the model with the prompt and tool config
        response = self.chat.send_message(prompt, tool_config=tool_config)
        
        # Extract the function call from the response
        if hasattr(response, 'parts') and len(response.parts) > 0:
            function_call = response.parts[0].function_call
            if function_call:
                # Call the appropriate function with the arguments
                args_dict = convert_to_serializable(function_call.args)
                
                if function_name == "find_influencers":
                    result = find_influencers(**args_dict)
                elif function_name == "analyze_email_response":
                    result = analyze_email_response(**args_dict)
                elif function_name == "draft_response_email":
                    result = draft_response_email(**args_dict)
                elif function_name == "get_campaign_performance":
                    result = get_campaign_performance(**args_dict)
                else:
                    result = json.dumps({"error": "Unknown function"})
                
                logging.info(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
                logging.info(f"--- End Gemini Function Call ---\n")
                
                return json.loads(result)
        
        # If no function call was made, fall back to direct function call
        logging.info("No function call detected, calling function directly")
        args_dict = convert_to_serializable(function_args)
        
        if function_name == "find_influencers":
            result = find_influencers(**args_dict)
        elif function_name == "analyze_email_response":
            result = analyze_email_response(**args_dict)
        elif function_name == "draft_response_email":
            result = draft_response_email(**args_dict)
        elif function_name == "get_campaign_performance":
            result = get_campaign_performance(**args_dict)
        else:
            result = json.dumps({"error": "Unknown function"})
            
        logging.info(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        logging.info(f"--- End Gemini Function Call ---\n")
        
        return json.loads(result)
    
    def find_matching_influencers(self, brief: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Use Gemini to find influencers that match a campaign brief.
        
        Args:
            brief: Dictionary with campaign requirements
            
        Returns:
            List of matching influencers
        """
        # TODO: We only need to check for the progress_stage to make sure that's at the "pending_outreach" stage. All other checks are done by previous steps in the pipeline
        # Use Gemini's function calling to determine the best parameters for the search
        prompt = f"""
        Find influencers for a {self.client_company['name']} campaign with these requirements:
        - Campaign goals: {', '.join(brief.get('goals', ['brand awareness']))}
        - Target audience: {brief.get('target_audience', self.client_company['target_audience'])}
        - Budget: ${brief.get('budget', self.client_company['budget'])}
        - Product focus: {brief.get('product_focus', self.client_company['product_types'][0])}
        
        Based on these requirements, find influencers in the appropriate niche with sufficient followers and engagement rate.
        """
        
        # Prepare default function arguments in case direct call is needed
        function_args = {
            "niche": brief.get("preferred_niche", self.client_company["industry"]),
            "min_followers": brief.get("min_followers", 100000),
            "min_engagement_rate": brief.get("min_engagement_rate", 2.5)
        }
        
        # Call the function and parse results
        result = self._call_gemini_function(prompt, "find_influencers", function_args)
        
        return result
    
    def analyze_influencer_response(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Gemini to analyze an email response from an influencer.
        
        Args:
            email_data: Dictionary with email data
            
        Returns:
            Dictionary with analysis results
        """
        prompt = f"""
        Analyze this email response from an influencer:
        
        From: {email_data['from']}
        Subject: {email_data['subject']}
        Body: {email_data['body']}
        
        Extract key information like sentiment, requested compensation, timeline, and questions.
        """
        
        # Prepare function arguments
        function_args = {
            "email_body": email_data['body']
        }
        
        # Call the function and parse results
        return self._call_gemini_function(prompt, "analyze_email_response", function_args)
    
    def generate_response_email(self, influencer: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Use Gemini to generate a response email to an influencer.
        
        Args:
            influencer: Dictionary with influencer data
            analysis: Dictionary with email analysis results
            
        Returns:
            Dictionary with email subject and body
        """
        prompt = f"""
        Draft a response email to {influencer['name']}, an influencer in the {influencer['niche']} niche.
        
        Their email had a {analysis['sentiment']} sentiment and mentioned these key points:
        {', '.join(analysis['key_points'])}
        
        Our company, {self.client_company['name']}, is in the {self.client_company['industry']} industry.
        Our brand values are: {', '.join(self.client_company['brand_values'])}
        
        Make the email professional, friendly, and personalized.
        """
        
        # Prepare function arguments
        function_args = {
            "influencer_name": influencer['name'],
            "influencer_niche": influencer['niche'],
            "sentiment": analysis['sentiment'],
            "key_points": analysis['key_points']
        }
        
        # Call the function and parse results
        result = self._call_gemini_function(prompt, "draft_response_email", function_args)
        
        return result
    
    def get_influencer_performance_history(self, influencer_id: int) -> List[Dict[str, Any]]:
        """
        Use Gemini to get and interpret an influencer's past campaign performance.
        
        Args:
            influencer_id: ID of the influencer
            
        Returns:
            List of campaign performance data with insights
        """
        prompt = f"""
        Get performance data for previous campaigns with influencer ID {influencer_id}.
        Analyze the ROI and engagement metrics.
        """
        
        # Prepare function arguments
        function_args = {
            "influencer_id": influencer_id
        }
        
        # Call the function and parse results
        result = self._call_gemini_function(prompt, "get_campaign_performance", function_args)
        
        return result
    
    def manage_influencer_campaign(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Let the agent decide the overall strategy and necessary actions for the campaign.
        
        Args:
            brief: Dictionary with campaign requirements
            
        Returns:
            Dictionary with campaign results
        """
        logging.info(f"\n=== Starting Influencer Campaign for {self.client_company['name']} ===")
        logging.info(f"Campaign Brief: {json.dumps(brief, indent=2)}")
        
        # Initialize conversation with the LLM
        prompt = f"""
        You are a marketing assistant helping to run an influencer marketing campaign for {self.client_company['name']}, 
        a company in the {self.client_company['industry']} industry.
        
        Campaign brief:
        - Goals: {', '.join(brief.get('goals', ['brand awareness']))}
        - Target audience: {brief.get('target_audience', self.client_company['target_audience'])}
        - Budget: ${brief.get('budget', self.client_company['budget'])}
        - Product focus: {brief.get('product_focus', self.client_company['product_types'][0])}
        
        Based on this information, determine what actions to take. You can:
        - Find influencers that match our requirements
        - Check for email responses from influencers
        - Analyze influencer responses
        - Draft email responses
        - Get campaign performance data
        
        What would you like to do first?
        """
        
        logging.info("\n🔧 Setting up tool configuration for agent decision-making")
        # Create a more flexible tool config that allows the model to choose any function
        from google.generativeai.types import content_types
        tool_config = content_types.to_tool_config(
            {"function_calling_config": {"mode": "any"}}
        )
        
        # Start a conversation and let the model decide the flow
        results = {
            "campaign_id": f"camp_{int(time.time())}",
            "campaign_brief": brief,
            "actions_taken": [],
            "influencers_contacted": [],
            "responses_processed": []
        }
        
        logging.info("\n🤖 Starting agent conversation loop")
        # Let the agent drive the conversation and take actions for a few turns
        chat = self.model.start_chat(history=[])
        for turn in range(10):  # Limit to 10 turns to avoid infinite loops
            logging.info(f"\n▶️ Turn {turn+1}: Sending prompt to agent")
            current_prompt = prompt if turn == 0 else "What should we do next?"
            logging.info(f"Prompt: {current_prompt}")
            
            response = chat.send_message(current_prompt, tool_config=tool_config)
            logging.info(f"✅ Received response from agent")
            
            # Extract function calls from the response
            if hasattr(response, 'parts') and len(response.parts) > 0:
                function_call = response.parts[0].function_call
                if function_call:
                    function_name = function_call.name
                    function_args = function_call.args
                    
                    logging.info(f"\n🔍 Agent decided to call function: {function_name}")
                    # Convert complex objects to JSON-serializable Python types
                    args_dict = convert_to_serializable(function_args)
                    
                    # Use json.dumps with a fallback to string representation
                    try:
                        args_str = json.dumps(args_dict, indent=2)
                    except TypeError:
                        args_str = str(args_dict)
                    
                    logging.info(f"With arguments: {args_str}")
                    
                    # Process the function call and get results
                    logging.info(f"⚙️ Processing function call...")
                    
                    # Implement the actual function call
                    if function_name == "find_influencers":
                        raw_result = find_influencers(**args_dict)
                        result_data = json.loads(raw_result)
                        result_summary = f"Found {len(result_data)} matching influencers"
                    elif function_name == "analyze_email_response":
                        raw_result = analyze_email_response(**args_dict)
                        result_data = json.loads(raw_result)
                        result_summary = f"Analysis: {result_data['sentiment']} sentiment with {len(result_data['key_points'])} key points"
                    elif function_name == "draft_response_email":
                        raw_result = draft_response_email(**args_dict)
                        result_data = json.loads(raw_result)
                        result_summary = f"Drafted email with subject: {result_data['subject']}"
                    elif function_name == "get_campaign_performance":
                        raw_result = get_campaign_performance(**args_dict)
                        result_data = json.loads(raw_result)
                        result_summary = f"Retrieved performance data for {len(result_data)} campaigns"
                    else:
                        result_summary = f"Unknown function: {function_name}"
                        result_data = {"error": "Unknown function"}
                    
                    logging.info(f"📊 Result summary: {result_summary}")
                    
                    # Record the action in results
                    results["actions_taken"].append({
                        "function": function_name,
                        "args": args_dict,
                        "result_summary": result_summary,
                        "result_data": result_data
                    })
                    logging.info(f"📝 Recorded action #{len(results['actions_taken'])} in results")
                    
                    # Update relevant campaign stats based on the function
                    if function_name == "find_influencers":
                        logging.info(f"📊 Updating potential influencers list")
                        # We would normally add logic to track which influencers we found
                        
                    elif function_name == "draft_response_email":
                        # If we're drafting a response, assume we're contacting an influencer
                        if "influencer_name" in args_dict:
                            results["influencers_contacted"].append(args_dict["influencer_name"])
                            logging.info(f"✉️ Added {args_dict['influencer_name']} to contacted influencers")
                            
                    elif function_name == "analyze_email_response":
                        # If we're analyzing a response, track it
                        results["responses_processed"].append({
                            "email_body": args_dict.get("email_body", "")[:50] + "...",
                            "analysis": result_data
                        })
                        logging.info(f"📨 Added response analysis to processed responses")
                    
                    # Send the function result back to the agent
                    logging.info(f"🔄 Sending result back to agent")
                    chat.send_message(f"Function {function_name} executed. Results: {results['actions_taken'][-1]['result_summary']}")
                else:
                    # Agent is done or needs more information
                    logging.info(f"\n⚠️ No function call detected in response - agent may be done or needs more information")
                    logging.info(f"Agent response: {response.text[:100]}..." if len(response.text) > 100 else f"Agent response: {response.text}")
                    break
            else:
                logging.info(f"\n❌ No function call parts found in response")
                break
        
        logging.info(f"\n🏁 Agent conversation completed after {len(results['actions_taken'])} actions")
        return results


# Example usage
if __name__ == "__main__":
    # Initialize the agent for client company with ID 1
    agent = GeminiInfluencerAgent(client_company_id=1)
    
    # Define a test campaign brief
    test_brief = {
        "goals": ["brand awareness", "product sales"],
        "preferred_niche": "fitness",
        "min_followers": 100000,
        "min_engagement_rate": 3.0,
        "product_focus": "supplements",
        "target_audience": "health enthusiasts aged 25-40",
        "budget": 25000
    }
    
    # Run the campaign
    campaign_results = agent.manage_influencer_campaign(test_brief)
    
    # Print summary
    logging.info("\n=== Campaign Summary ===")
    logging.info(f"Campaign ID: {campaign_results['campaign_id']}")
    logging.info(f"Total actions taken: {len(campaign_results['actions_taken'])}")
    logging.info(f"Total influencers contacted: {len(campaign_results['influencers_contacted'])}")
    logging.info(f"Total responses processed: {len(campaign_results['responses_processed'])}")
    
    # Print detailed actions
    logging.info("\n=== Detailed Actions ===")
    for i, action in enumerate(campaign_results['actions_taken']):
        logging.info(f"\nAction #{i+1}: {action['function']}")
        # Ensure arguments are JSON serializable
        serializable_args = convert_to_serializable(action['args'])
        try:
            args_str = json.dumps(serializable_args, indent=2)
        except TypeError:
            args_str = str(serializable_args)
        logging.info(f"Arguments: {args_str}")
        logging.info(f"Result: {action['result_summary']}")
    
    # Print contacted influencers
    if campaign_results['influencers_contacted']:
        logging.info("\n=== Contacted Influencers ===")
        for i, name in enumerate(campaign_results['influencers_contacted']):
            logging.info(f"{i+1}. {name}")
    
    # Print processed responses
    if campaign_results['responses_processed']:
        logging.info("\n=== Processed Responses ===")
        for i, response in enumerate(campaign_results['responses_processed']):
            logging.info(f"\nResponse #{i+1}:")
            logging.info(f"Email excerpt: {response['email_body']}")
            logging.info(f"Sentiment: {response['analysis']['sentiment']}")
            logging.info(f"Key points: {', '.join(response['analysis']['key_points'])}")
    
    # Print log file location
    print(f"\n✅ Campaign completed! Full logs available at: {log_file_path}")
    print(f"View logs with: cat {log_file_path}")
