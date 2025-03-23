import psycopg2
from psycopg2 import Error
import json
from typing import List, Dict, Any, Optional, Tuple

class DatabaseManager:
    def __init__(self, host: str = "dpg-cvfgf7ggph6c73bcmh40-a.oregon-postgres.render.com",
                 port: str = "5432",
                 database: str = "influencers_c321",
                 user: str = "hackathon",
                 password: str = "P9IG7soIKN9RNGlRKyRWcWRev03VEihD"):
        """
        Initialize DatabaseManager with connection parameters
        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Database user
            password: Database password
        """
        self.db_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password
        }
        self.connection = None
        self.cursor = None

    def connect(self) -> Tuple[Optional[psycopg2.extensions.connection], 
                              Optional[psycopg2.extensions.cursor]]:
        """
        Create a connection to the database
        Returns:
            Tuple of (connection, cursor) objects
        """
        try:
            self.connection = psycopg2.connect(**self.db_params)
            self.cursor = self.connection.cursor()
            print("Successfully connected to PostgreSQL database!")
            return self.connection, self.cursor
        except (Exception, Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            return None, None

    def close(self) -> None:
        """Close the database connection and cursor"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
        self.cursor = None
        self.connection = None

    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[List[tuple]]:
        """
        Execute a SQL query and return the results
        Args:
            query: SQL query string
            params: Optional tuple of parameters for the SQL query
        Returns:
            List of tuples containing the query results
        """
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except (Exception, Error) as error:
            print(f"Error executing query: {error}")
            return None
        
    def execute_query_with_columns(self, query: str, params: Optional[tuple] = None) -> Tuple[Optional[List[tuple]], Optional[List[str]]]:
        """
        Execute a SQL query and return both results and column names
        Args:
            query: SQL query string
            params: Optional tuple of parameters for the SQL query
        Returns:
            Tuple of (results, column_names)
        """
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return results, columns
        except (Exception, Error) as error:
            print(f"Error executing query: {error}")
            return None, None

    def execute_query_to_json(self, query: str, params: Optional[tuple] = None) -> List[Dict[Any, Any]]:
        """
        Execute a SQL query and return results in JSON format
        Args:
            query: SQL query string
            params: Optional tuple of parameters for the SQL query
        Returns:
            List of dictionaries containing the query results
        """
        results = []
        rows, columns = self.execute_query_with_columns(query, params)
        
        if rows and columns:
            for row in rows:
                results.append(dict(zip(columns, row)))
        
        return results

    def save_results_to_json(self, results: List[Dict[Any, Any]], filename: str) -> None:
        """
        Save query results to a JSON file
        Args:
            results: List of dictionaries containing the query results
            filename: Name of the file to save the results to
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, default=str)
            print(f"Results successfully saved to {filename}")
        except Exception as error:
            print(f"Error saving results to file: {error}")

    def get_table_names(self) -> List[str]:
        """
        Get list of all tables in the database
        Returns:
            List of table names
        """
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        results = self.execute_query(query)
        return [table[0] for table in results] if results else []

    def get_table_schema(self, table_name: str) -> List[Dict[str, str]]:
        """
        Get schema information for a specific table
        Args:
            table_name: Name of the table
        Returns:
            List of dictionaries containing column information
        """
        query = """
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = %s
        """
        return self.execute_query_to_json(query, (table_name,))

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Example usage and backwards compatibility functions
def get_database_connection():
    """
    Backwards compatibility function for existing code
    Returns:
        Tuple of (connection, cursor)
    """
    db = DatabaseManager()
    return db.connect()

def close_connection(connection, cursor):
    """
    Backwards compatibility function for existing code
    Args:
        connection: PostgreSQL connection object
        cursor: PostgreSQL cursor object
    """
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("Database connection closed.")

def execute_query_to_json(query: str, params: Optional[tuple] = None) -> List[Dict[Any, Any]]:
    """
    Backwards compatibility function for existing code
    Args:
        query: SQL query string
        params: Optional tuple of parameters
    Returns:
        List of dictionaries containing query results
    """
    with DatabaseManager() as db:
        return db.execute_query_to_json(query, params)

# Example usage
if __name__ == "__main__":
    # Using the class directly
    db = DatabaseManager()
    
    # Example 1: Using context manager
    with DatabaseManager() as db:
        # Get all table names
        tables = db.get_table_names()
        print("Available tables:", tables)
        
        # Get schema for influencer_metrics table
        schema = db.get_table_schema("influencer_metrics")
        print("Table schema:", schema)
        
        # Execute a query
        query = "SELECT * FROM influencer_metrics LIMIT 5"
        results = db.execute_query_to_json(query)
        
        # Save results to file
        if results:
            db.save_results_to_json(results, "query_results.json")
    
    # Example 2: Using individual methods
    db = DatabaseManager()
    db.connect()
    
    # Execute a query
    query = """
    SELECT 
        profile_name,
        contract_shares,
        contract_plays,
        contract_comments
    FROM 
        influencer_metrics
    ORDER BY 
        profile_name
    LIMIT 5;
    """
    
    results = db.execute_query_to_json(query)
    print("Query results:", results)
    
    # Close the connection
    db.close() 