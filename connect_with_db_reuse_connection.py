import psycopg2
from psycopg2 import Error

# Global variable to store the database connection
connection = None

def connect_to_db():
    global connection
    try:
        # Connect to the PostgreSQL database if connection is not already open
        if connection is None:
            connection = psycopg2.connect(
                user="your_username",
                password="your_password",
                host="your_host",
                port="your_port",
                database="your_database"
            )
            print("Connected to PostgreSQL successfully")
        else:
            print("Already connected to PostgreSQL")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)

def close_connection():
    global connection
    if connection is not None:
        connection.close()
        print("PostgreSQL connection is closed")
        connection = None

def execute_query(query):
    try:
        global connection
        # Ensure there's an open connection
        if connection is None:
            print("Not connected to PostgreSQL. Establishing connection...")
            connect_to_db()
        
        # Create a cursor object using the cursor() method
        cursor = connection.cursor()

        # Execute a SQL query
        cursor.execute(query)

        # If the query is a SELECT statement, fetch the data
        if query.strip().lower().startswith('select'):
            result = cursor.fetchall()
            return result
        else:
            # Commit the changes in the database
            connection.commit()
            print("Query executed successfully")
    except (Exception, Error) as error:
        print("Error while executing query:", error)

# Example usage:
# connect_to_db()

# Example select query
# select_query = "SELECT * FROM your_table"
# result = execute_query(select_query)
# print("Result of SELECT query:", result)

# Example insert query
# insert_query = "INSERT INTO your_table (column1, column2) VALUES ('value1', 'value2')"
# execute_query(insert_query)

# Close the connection
# close_connection()
