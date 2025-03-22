import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def insert_data(connection, table_name, data):
    """
    Inserts data into the specified PostgreSQL table.

    Parameters:
    - connection: psycopg2 connection object to the database.
    - table_name (str): Name of the table to insert data into.
    - data (dict): A dictionary where keys are column names and values are the data to insert.

    Example:
    insert_data(conn, 'employees', {'name': 'John Doe', 'age': 30, 'department': 'HR'})
    """
    columns = data.keys()
    values = [data[column] for column in columns]

    insert_query = sql.SQL(
        "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
    ).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, values)
            connection.commit()
            print(f"Data inserted successfully into {table_name} table.")
    except Exception as error:
        print(f"Error inserting data into {table_name}: {error}")
        connection.rollback()

def fetch_data(connection, table_name, columns='*', condition=None):
    """
    Fetches data from the specified PostgreSQL table.

    Parameters:
    - connection: psycopg2 connection object to the database.
    - table_name (str): Name of the table to fetch data from.
    - columns (str or list): Columns to retrieve; default is '*' (all columns).
    - condition (str): SQL condition for filtering data; default is None.

    Returns:
    - List of tuples containing the fetched data.

    Example:
    fetch_data(conn, 'employees', ['name', 'age'], "department = 'HR'")
    """
    if isinstance(columns, list):
        columns = ', '.join(columns)

    fetch_query = sql.SQL("SELECT {fields} FROM {table}").format(
        fields=sql.SQL(columns),
        table=sql.Identifier(table_name)
    )

    if condition:
        fetch_query += sql.SQL(" WHERE {condition}").format(
            condition=sql.SQL(condition)
        )

    try:
        with connection.cursor() as cursor:
            cursor.execute(fetch_query)
            results = cursor.fetchall()
            return results
    except Exception as error:
        print(f"Error fetching data from {table_name}: {error}")
        return []

def create_table(connection, table_name, columns_definition):
    """
    Creates a new table in the PostgreSQL database.

    Parameters:
    - connection: psycopg2 connection object to the database.
    - table_name (str): Name of the table to create.
    - columns_definition (dict): A dictionary where keys are column names and values are column definitions.
                                Each definition includes the data type and any constraints.

    Example:
    create_table(conn, 'employees', {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(100) NOT NULL',
        'age': 'INTEGER',
        'department': 'VARCHAR(50)'
    })
    """
    column_parts = []
    for column_name, definition in columns_definition.items():
        column_parts.append(sql.SQL("{} {}").format(
            sql.Identifier(column_name),
            sql.SQL(definition)
        ))

    create_query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS {table} ({columns})"
    ).format(
        table=sql.Identifier(table_name),
        columns=sql.SQL(', ').join(column_parts)
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(create_query)
            connection.commit()
            print(f"Table {table_name} created successfully.")
    except Exception as error:
        print(f"Error creating table {table_name}: {error}")
        connection.rollback()

def delete_table(connection, table_name, confirm=False):
    """
    Deletes a table from the PostgreSQL database.

    Parameters:
    - connection: psycopg2 connection object to the database.
    - table_name (str): Name of the table to delete.
    - confirm (bool): Safety parameter that must be set to True to confirm deletion.

    Example:
    delete_table(conn, 'employees', confirm=True)
    """
    if not confirm:
        print(f"Table deletion not confirmed. Set confirm=True to delete {table_name}.")
        return

    delete_query = sql.SQL("DROP TABLE IF EXISTS {table}").format(
        table=sql.Identifier(table_name)
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(delete_query)
            connection.commit()
            print(f"Table {table_name} deleted successfully.")
    except Exception as error:
        print(f"Error deleting table {table_name}: {error}")
        connection.rollback()

# Example usage:
if __name__ == "__main__":
    result = urlparse(os.getenv("DATABASE_URL"))
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname

    connection = None  # Initialize connection to None

    try:
        conn = psycopg2.connect(
        user=username,
        password=password,
        host=hostname,
        port="5432",
        database=database
        )

        # create_table(conn, 'leads', {
        #     'id': 'SERIAL PRIMARY KEY',
        #     'profile_name': 'VARCHAR(255) NOT NULL',
        #     'fans': 'INTEGER',
        #     'hearts': 'INTEGER',
        #     'lead_stage': 'VARCHAR(50)'
        # })

        insert_data(conn, 'leads', {
            'profile_name': 'test_user',
            'fans': 1000,
            'hearts': 500,
            'lead_stage': 'prospect'
        })

    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
