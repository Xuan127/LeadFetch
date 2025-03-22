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
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Google Generative AI library
import google.generativeai as genai
from dotenv import load_dotenv

# Import utility functions
from influencerOutreach.utils import setup_logging, convert_to_serializable
# Import the email function
from influencerOutreach.email_function import send_simple_message

# Load environment variables from .env file
load_dotenv()

# Call setup_logging to initialize
log_file_path = setup_logging()

MODEL_NAME = "gemini-2.0-flash"

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

def send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Send an email using the email_function module.
    
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
    
    # Use the improved send_simple_message function with all parameters
    response = send_simple_message(
        message=body,
        recipient=to,
        subject=subject
    )
    
    # Return a standardized response format
    status_code = getattr(response, 'status_code', None)
    return {
        "status": "sent" if response and status_code == 200 else "failed",
        "message_id": f"msg_{int(time.time())}",
        "recipient": to,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "response_code": status_code
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
    model = genai.GenerativeModel(MODEL_NAME)
    
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
        email_send_function: Callable = send_email,  # Changed to use real email function
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
            MODEL_NAME,
            tools=[
                find_influencers,
                analyze_email_response,
                draft_response_email,
                self.send_email_tool  # Use the class method
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
        
        # Create a more flexible tool config that allows the model to choose any function
        from google.generativeai.types import content_types
        tool_config = content_types.to_tool_config({
            "function_calling_config": {
                "mode": "any"
            }
        })
        
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
    
    def _create_initial_outreach_email(self, influencer: Dict[str, Any], brief: Dict[str, Any]) -> Dict[str, str]:
        """
        Create an initial outreach email for an influencer.
        
        Args:
            influencer: Dictionary containing influencer data
            brief: Dictionary with campaign requirements
            
        Returns:
            Dictionary with email subject and body
        """
        # Get influencer name, handling both formats
        influencer_name = influencer.get("influencer_name", influencer.get("name", "Influencer"))
        # Get influencer niche if available
        influencer_niche = influencer.get("niche", "content")
        
        subject = f"Partnership Opportunity with {self.client_company['name']}"
        body = f"""Hello {influencer_name},

We're {self.client_company['name']}, a company in the {self.client_company['industry']} industry, and we're impressed with your content in the {influencer_niche} niche.

We'd like to discuss a potential partnership for our upcoming campaign focused on {brief.get('product_focus', self.client_company['product_types'][0])}.

Our target audience aligns well with your followers, and we believe a collaboration would be mutually beneficial.

Would you be interested in discussing this opportunity further?

Best regards,
The Partnership Team at {self.client_company['name']}
"""
        return {"subject": subject, "body": body}
    
    def _find_influencer_email(self, influencer_name: str, actions_taken: List[Dict[str, Any]]) -> Optional[str]:
        """
        Find an influencer's email address from previous actions.
        
        Args:
            influencer_name: Name of the influencer
            actions_taken: List of previous actions taken
            
        Returns:
            Email address if found, None otherwise
        """
        for action in actions_taken:
            if action["function"] == "find_influencers":
                for influencer in action["result_data"]:
                    if influencer["name"] == influencer_name:
                        return influencer["email"]
        return None
    
    def send_influencer_email(self, influencer_data: Dict[str, Any], email_type: str, brief: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send an email to an influencer and track the result.
        
        Args:
            influencer_data: Dictionary with influencer data and/or email details
            email_type: Type of email (initial_outreach or follow_up)
            brief: Dictionary with campaign requirements (for initial outreach)
            
        Returns:
            Dictionary with email send status and tracking info
        """
        # Handle different email types
        if email_type == "initial_outreach":
            # For initial outreach, generate the email content
            influencer_name = influencer_data["name"]
            email_content = self._create_initial_outreach_email(influencer_data, brief)
            to_email = influencer_data["email"]
            
            # Send the email
            email_result = self.send_email(
                to=to_email,
                subject=email_content["subject"],
                body=email_content["body"]
            )
            
            # Add influencer to contacted set
            self.contacted_influencers.add(influencer_name)
            
            # Prepare result for tracking
            email_tracking = {
                "influencer_id": influencer_data.get("id"),
                "influencer_name": influencer_name,
                "email": to_email,
                "subject": email_content["subject"],
                "type": email_type,
                "status": email_result.get("status", "unknown"),
                "timestamp": email_result.get("timestamp")
            }
            
            logging.info(f"📧 Sent outreach email to {influencer_name} ({to_email})")
            
        elif email_type == "follow_up":
            # For follow-up, the email content is provided in the influencer_data
            influencer_name = influencer_data.get("influencer_name", "")
            subject = influencer_data.get("subject", "")
            body = influencer_data.get("body", "")
            to_email = influencer_data.get("email", "")
            
            if to_email:
                # Send the email
                email_result = self.send_email(
                    to=to_email,
                    subject=subject,
                    body=body
                )
                
                # Prepare result for tracking
                email_tracking = {
                    "influencer_name": influencer_name,
                    "email": to_email,
                    "subject": subject,
                    "type": email_type,
                    "status": email_result.get("status", "unknown"),
                    "timestamp": email_result.get("timestamp")
                }
                
                logging.info(f"📧 Sent follow-up email to {influencer_name} ({to_email})")
            else:
                # If email not provided, attempt was unsuccessful
                logging.warning(f"⚠️ No email address for {influencer_name}, email not sent")
                email_result = {"status": "failed", "reason": "No email address found"}
                email_tracking = {
                    "influencer_name": influencer_name,
                    "type": email_type,
                    "status": "failed",
                    "reason": "No email address found"
                }
        else:
            # Unsupported email type
            email_result = {"status": "failed", "reason": f"Unsupported email type: {email_type}"}
            email_tracking = {
                "type": email_type,
                "status": "failed",
                "reason": f"Unsupported email type: {email_type}"
            }
        
        return {"result": email_result, "tracking": email_tracking}

    def send_email_tool(self, influencer_name: str, email: str, subject: str, body: str, email_type: str = "follow_up") -> str:
        """
        Send an email to an influencer and track the result.
        
        Args:
            influencer_name: Name of the influencer
            email: Email address of the influencer
            subject: Subject line for the email
            body: Content of the email
            email_type: Type of email (default: follow_up)
            
        Returns:
            JSON string with email send status
        """
        # Create a simplified data structure
        influencer_data = {
            "influencer_name": influencer_name,
            "email": email,
            "subject": subject,
            "body": body
        }
        
        result = self.send_influencer_email(
            influencer_data=influencer_data,
            email_type=email_type
        )
        
        return json.dumps(result)

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
        
        What would you like to do first?
        """
        
        logging.info("\n🔧 Setting up tool configuration for agent decision-making")
        # Create a more flexible tool config that allows the model to choose any function
        from google.generativeai.types import content_types
        tool_config = content_types.to_tool_config({
            "function_calling_config": {
                "mode": "any"
            }
        })
        
        # Start a conversation and let the model decide the flow
        results = {
            "campaign_id": f"camp_{int(time.time())}",
            "campaign_brief": brief,
            "actions_taken": [],
            "influencers_contacted": [],
            "responses_processed": [],
            "emails_sent": []  # Field to track emails sent
        }
        
        logging.info("\n🤖 Starting agent conversation loop")
        # Let the agent drive the conversation and take actions for a few turns
        chat = self.model.start_chat(history=[])
        for turn in range(15):  # Limit to 10 turns to avoid infinite loops
            logging.info(f"\n▶️ Turn {turn+1}: Sending prompt to agent")
            current_prompt = prompt if turn == 0 else "What should we do next?"
            logging.info(f"Prompt: {current_prompt}")
            
            response = chat.send_message(current_prompt, tool_config=tool_config)
            logging.info(f"✅ Received response from agent")
            logging.info(f"Response: {response}")
            
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
                    
                    logging.info(f"With arguments: {function_call.args}")
                    
                    # Process the function call and get results
                    logging.info(f"⚙️ Processing function call...")
                    
                    # Implement the actual function call
                    if function_name == "find_influencers":
                        raw_result = find_influencers(**function_call.args)
                        result_data = json.loads(raw_result)
                        result_summary = f"Found {len(result_data)} matching influencers"
                        
                        # Automatically send initial outreach emails to found influencers
                        if len(result_data) > 0 and turn < 2:  # Only do this in early turns
                            logging.info(f"✉️ Automatically sending outreach emails to {len(result_data)} influencers")
                            for influencer in result_data:
                                # Skip if already contacted
                                if influencer['name'] in self.contacted_influencers:
                                    continue
                                    
                                # Send the email and track results
                                email_operation = self.send_influencer_email(
                                    influencer_data=influencer,
                                    email_type="initial_outreach",
                                    brief=brief
                                )
                                
                                # Add to results tracking
                                results["emails_sent"].append(email_operation["tracking"])
                                
                    elif function_name == "analyze_email_response":
                        raw_result = analyze_email_response(**function_call.args)
                        result_data = json.loads(raw_result)
                        result_summary = f"Analysis: {result_data['sentiment']} sentiment with {len(result_data['key_points'])} key points"
                    elif function_name == "draft_response_email":
                        raw_result = draft_response_email(**function_call.args)
                        result_data = json.loads(raw_result)
                        result_summary = f"Drafted email with subject: {result_data['subject']}"
                        
                        # Actually send the drafted email if it's a valid response
                        if 'subject' in result_data and 'body' in result_data:
                            # Get influencer name from arguments
                            recipient_name = args_dict.get("influencer_name", "")
                            
                            # Find the influencer's email
                            recipient_email = self._find_influencer_email(recipient_name, results["actions_taken"])
                            
                            if recipient_email:
                                # Prepare data for sending email
                                email_data = {
                                    "influencer_name": recipient_name,
                                    "email": recipient_email,
                                    "subject": result_data['subject'],
                                    "body": result_data['body']
                                }
                                
                                # Send the email and track results
                                email_operation = self.send_influencer_email(
                                    influencer_data=email_data,
                                    email_type="follow_up"
                                )
                                
                                # Add to results tracking
                                results["emails_sent"].append(email_operation["tracking"])
                                
                                result_summary += f" and sent to {recipient_email}"
                            else:
                                logging.warning(f"⚠️ Could not find email address for {recipient_name}, email not sent")
                    
                    elif function_name == "send_email_tool":
                        # Handle the simplified email tool
                        raw_result = self.send_email_tool(**function_call.args)
                        result_data = json.loads(raw_result)
                        influencer_name = args_dict.get("influencer_name", "unknown")
                        result_summary = f"Sent email to {influencer_name} with subject: {args_dict.get('subject', 'No subject')}"
                        
                        # Add to email tracking if not already added by the function
                        if "tracking" in result_data:
                            results["emails_sent"].append(result_data["tracking"])
                                
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
        logging.info(f"Total emails sent: {len(results['emails_sent'])}")
        return results


# Example usage
if __name__ == "__main__":
    # Initialize the agent for client company with ID 1
    agent = GeminiInfluencerAgent(client_company_id=1)
    
    # Define a test campaign brief
    test_brief = {
        "goals": ["brand awareness", "product sales"],
        "preferred_niche": "TTS engine for developers to develop voice assistants",
        "min_followers": 100000,
        "min_engagement_rate": 3.0,
        "product_focus": "ElevenLabs TTS engine",
        "target_audience": "developers",
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
