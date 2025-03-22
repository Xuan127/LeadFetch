"""
Utility functions for the LeadFetch application.
"""

import os
import logging
from typing import Any
from datetime import datetime
import json

def setup_logging() -> str:
    """
    Set up logging for the application.
    
    Returns:
        Path to the log file
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Set up log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = f"logs/influencer_agent_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    
    return log_file_path

def convert_to_serializable(obj: Any) -> Any:
    """
    Convert an object to a JSON-serializable format.
    
    Args:
        obj: The object to convert
        
    Returns:
        JSON-serializable version of the object
    """
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    
    if hasattr(obj, '__dict__'):
        return {k: convert_to_serializable(v) for k, v in obj.__dict__.items() 
                if not k.startswith('_')}
    
    if isinstance(obj, (list, tuple)):
        return [convert_to_serializable(x) for x in obj]
    
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    
    return obj