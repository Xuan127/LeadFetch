"""
Gemini-Powered Influencer Marketing Agent

This agent uses Google's Gemini API to intelligently identify and contact 
potential influencer marketers to form business partnerships with a client company.
It demonstrates function calling with Gemini similar to the Google example.
"""

import json
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

# Import Google Generative AI library
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Mock functions for database and email operations
def mock_query_database(query: str) -> List[Dict[str, Any]]:
    """
    Mock function to query a PostgreSQL database.
    
    Args:
        query: SQL query string
        
    Returns:
        List of dictionaries representing database records
    """
    print(f"Executing database query: {query}")
    
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
    print(f"Checking emails with filter: {email_filter}")
    
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
    print(f"\nSending email to: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    
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
        print("\n--- Gemini Function Call ---")
        print(f"Prompt: {prompt}")
        print(f"Function: {function_name}")
        print(f"Arguments: {json.dumps(function_args, indent=2)}")
        
        # Create function calling config to force use of the specific function
        from google.generativeai.types import content_types
        tool_config = content_types.to_tool_config(
            {"function_calling_config": {"mode": "auto", "allowed_function_names": [function_name]}}
        )
        
        # Call the model with the prompt and tool config
        response = self.chat.send_message(prompt, tool_config=tool_config)
        
        # Extract the function call from the response
        if hasattr(response, 'parts') and len(response.parts) > 0:
            function_call = response.parts[0].function_call
            if function_call:
                # Call the appropriate function with the arguments
                if function_name == "find_influencers":
                    result = find_influencers(**function_call.args)
                elif function_name == "analyze_email_response":
                    result = analyze_email_response(**function_call.args)
                elif function_name == "draft_response_email":
                    result = draft_response_email(**function_call.args)
                elif function_name == "get_campaign_performance":
                    result = get_campaign_performance(**function_call.args)
                else:
                    result = json.dumps({"error": "Unknown function"})
                
                print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
                print(f"--- End Gemini Function Call ---\n")
                
                return json.loads(result)
        
        # If no function call was made, fall back to direct function call
        print("No function call detected, calling function directly")
        if function_name == "find_influencers":
            result = find_influencers(**function_args)
        elif function_name == "analyze_email_response":
            result = analyze_email_response(**function_args)
        elif function_name == "draft_response_email":
            result = draft_response_email(**function_args)
        elif function_name == "get_campaign_performance":
            result = get_campaign_performance(**function_args)
        else:
            result = json.dumps({"error": "Unknown function"})
            
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        print(f"--- End Gemini Function Call ---\n")
        
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
    
    def run_outreach_campaign(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a full outreach campaign using Gemini to make intelligent decisions.
        
        Args:
            campaign_brief: Dictionary with campaign requirements
            
        Returns:
            Dictionary with campaign results
        """
        print(f"\n=== Starting Outreach Campaign for {self.client_company['name']} ===")
        print(f"Campaign Brief: {json.dumps(brief, indent=2)}")
        
        # Step 1: Find matching influencers
        influencers = self.find_matching_influencers(brief)
        print(f"Found {len(influencers)} matching influencers")
        
        # Step 2: Send personalized outreach emails
        outreach_results = []
        for influencer in influencers:
            # Skip if already contacted
            if influencer["id"] in self.contacted_influencers:
                print(f"Skipping {influencer['name']} - already contacted")
                continue
                
            # Generate personalized email
            email_content = self.generate_outreach_email(influencer)
            
            # Send the email
            send_result = self.send_email(
                to=influencer["email"],
                subject=email_content["subject"],
                body=email_content["body"]
            )
            
            # Mark as contacted
            self.contacted_influencers.add(influencer["id"])
            
            # Record result
            outreach_results.append({
                "influencer_id": influencer["id"],
                "influencer_name": influencer["name"],
                "email_result": send_result
            })
            
            # Add a small delay between emails
            time.sleep(1)
        
        # Step 3: Check for and process responses
        responses = self.check_for_responses()
        processed_responses = []
        
        for email in responses:
            # Find the influencer who sent this email
            influencer = None
            for inf in influencers:
                if inf["email"] == email["from"]:
                    influencer = inf
                    break
            
            if not influencer:
                print(f"Could not identify influencer for email: {email['from']}")
                continue
                
            # Analyze the response
            analysis = self.analyze_influencer_response(email)
            
            # Generate a reply if sentiment is positive
            if analysis["sentiment"] == "positive":
                reply = self.generate_response_email(influencer, analysis)
                
                # Send the reply
                reply_result = self.send_email(
                    to=email["from"],
                    subject=reply["subject"],
                    body=reply["body"]
                )
                
                processed_responses.append({
                    "email_id": email["id"],
                    "influencer_id": influencer["id"],
                    "analysis": analysis,
                    "reply_sent": True,
                    "reply_result": reply_result
                })
            else:
                processed_responses.append({
                    "email_id": email["id"],
                    "influencer_id": influencer["id"],
                    "analysis": analysis,
                    "reply_sent": False,
                    "action": "flagged_for_review"
                })
        
        # Return campaign results
        return {
            "campaign_id": f"camp_{int(time.time())}",
            "campaign_brief": campaign_brief,
            "outreach_count": len(outreach_results),
            "response_count": len(processed_responses),
            "outreach_results": outreach_results,
            "processed_responses": processed_responses,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_outreach_email(self, influencer: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate a personalized outreach email for an influencer.
        
        Args:
            influencer: Dictionary with influencer data
            
        Returns:
            Dictionary with email subject and body
        """
        company_name = self.client_company["name"]
        industry = self.client_company["industry"]
        
        subject = f"Partnership Opportunity with {company_name}"
        
        # Personalize based on influencer niche
        body = f"""Hello {influencer['name']},

I hope this email finds you well. My name is AI Assistant, and I represent {company_name}, a leading brand in the {industry} industry.

We've been following your content and are impressed with your engagement rate of {influencer['engagement_rate']}% and your audience of {influencer['followers']} followers in the {influencer['niche']} niche.

We believe there could be a great opportunity for collaboration between our brand and your platform. Our {', '.join(self.client_company['product_types'])} would resonate well with your audience, particularly those in the {influencer['audience_demographics']['age']} age range.

Would you be interested in exploring a collaboration? We can offer competitive compensation and are open to various partnership models including sponsored content, product reviews, or brand ambassadorship.

Looking forward to your response.

Best regards,
AI Assistant
Partnerships Team
{company_name}
"""
        
        return {
            "subject": subject,
            "body": body
        }
    
    def check_for_responses(self) -> List[Dict[str, Any]]:
        """
        Check for email responses from influencers.
        
        Returns:
            List of unread email responses
        """
        email_filter = {
            "to": "partnerships@clientcompany.com",
            "read": False
        }
        
        return self.check_emails(email_filter)


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
    campaign_results = agent.run_outreach_campaign(test_brief)
    
    # Print summary
    print("\n=== Campaign Summary ===")
    print(f"Campaign ID: {campaign_results['campaign_id']}")
    print(f"Total influencers contacted: {campaign_results['outreach_count']}")
    print(f"Total responses processed: {campaign_results['response_count']}")
