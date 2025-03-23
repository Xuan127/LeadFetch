import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import time
from datetime import datetime
import os
from database import execute_query_to_json
from gemini_helper import GeminiHelper

class PerformanceAnalysisAgent:
    def __init__(self):
        """Initialize the Performance Analysis Agent"""
        self.data = pd.DataFrame()
        self.last_update = None
        # Initialize Gemini helper
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        self.gemini = GeminiHelper(api_key)
        
    def fetch_metrics(self):
        """Fetch metrics from the database"""
        query = """
        SELECT 
            profile_name,
            contract_shares,
            contract_plays,
            contract_comments
        FROM 
            influencer_metrics
        ORDER BY 
            profile_name;
        """
        
        results = execute_query_to_json(query)
        return results

    def process_metrics_with_llm(self, raw_data):
        """
        Process metrics using Gemini LLM to get structured insights
        """
        # Create a prompt for the LLM to analyze the data
        prompt = f"""
        Analyze the following influencer metrics and provide insights in a structured format:
        {raw_data}
        
        Focus on:
        1. Top performing profiles
        2. Engagement patterns
        3. Areas for improvement
        4. Notable trends
        """
        
        # Define the expected structure for the analysis
        analysis_structure = {
            "top_performers": "list",
            "engagement_patterns": {
                "high_engagement_times": "list",
                "popular_content_types": "list"
            },
            "improvement_areas": "list",
            "trends": {
                "growing_profiles": "list",
                "declining_profiles": "list"
            }
        }
        
        # Get structured analysis from Gemini
        analysis = self.gemini.structured_analysis(prompt, analysis_structure)
        return analysis

    def create_dashboard(self):
        """Create and run the dashboard"""
        app = dash.Dash(__name__)
        
        app.layout = html.Div([
            html.H1("Influencer Performance Dashboard", style={'textAlign': 'center'}),
            html.Div(id='last-update', style={'textAlign': 'center'}),
            html.Div([
                dcc.Graph(id='metrics-graph'),
                html.Div(id='ai-insights', style={'margin': '20px', 'padding': '20px', 'border': '1px solid #ddd'})
            ]),
            dcc.Interval(
                id='interval-component',
                interval=30*1000,  # Update every 30 seconds
                n_intervals=0
            )
        ])
        
        @app.callback(
            [Output('metrics-graph', 'figure'),
             Output('last-update', 'children'),
             Output('ai-insights', 'children')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_dashboard(n):
            # Fetch new data
            raw_data = self.fetch_metrics()
            
            if not raw_data:
                return {}, "No data available", "No insights available"
            
            # Convert to DataFrame for plotting
            self.data = pd.DataFrame(raw_data)
            self.last_update = datetime.now()
            
            # Get AI insights
            insights = self.process_metrics_with_llm(raw_data)
            
            # Create subplots for metrics
            fig = make_subplots(rows=3, cols=1,
                              subplot_titles=('Shares', 'Plays', 'Comments'),
                              vertical_spacing=0.1)
            
            # Add traces for each metric
            fig.add_trace(
                go.Bar(x=self.data['profile_name'], y=self.data['contract_shares'], name='Shares'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=self.data['profile_name'], y=self.data['contract_plays'], name='Plays'),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Bar(x=self.data['profile_name'], y=self.data['contract_comments'], name='Comments'),
                row=3, col=1
            )
            
            # Update layout
            fig.update_layout(
                height=900,
                showlegend=False,
                title_text="Influencer Performance Metrics"
            )
            
            last_update_text = f"Last Updated: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Format insights for display
            insights_html = [
                html.H3("AI-Generated Insights"),
                html.H4("Top Performers"),
                html.Ul([html.Li(performer) for performer in insights.get('top_performers', [])]),
                
                html.H4("Engagement Patterns"),
                html.H5("High Engagement Times"),
                html.Ul([html.Li(time) for time in insights.get('engagement_patterns', {}).get('high_engagement_times', [])]),
                html.H5("Popular Content Types"),
                html.Ul([html.Li(content) for content in insights.get('engagement_patterns', {}).get('popular_content_types', [])]),
                
                html.H4("Areas for Improvement"),
                html.Ul([html.Li(area) for area in insights.get('improvement_areas', [])]),
                
                html.H4("Trends"),
                html.H5("Growing Profiles"),
                html.Ul([html.Li(profile) for profile in insights.get('trends', {}).get('growing_profiles', [])]),
                html.H5("Declining Profiles"),
                html.Ul([html.Li(profile) for profile in insights.get('trends', {}).get('declining_profiles', [])])
            ]
            
            return fig, last_update_text, insights_html
        
        return app

def run_agent():
    """Run the Performance Analysis Agent"""
    try:
        agent = PerformanceAnalysisAgent()
        app = agent.create_dashboard()
        app.run_server(debug=True, port=8050)
    except Exception as e:
        print(f"Error starting the agent: {str(e)}")

if __name__ == "__main__":
    run_agent() 