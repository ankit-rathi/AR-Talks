import psycopg2
from psycopg2 import sql

def insert_json_to_postgres(json_data, table_name, conn_params):
    """
    Inserts records from a JSON object into a PostgreSQL table.
    
    Parameters:
        json_data (list): A list of dictionaries where keys are column names and values are the data to insert.
        table_name (str): The name of the table to insert data into.
        conn_params (dict): A dictionary containing connection parameters like dbname, user, password, host, port.
    """
    # Establish a connection to the database
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    
    # Get the column names from the first record
    columns = json_data[0].keys()
    
    # Create an SQL query for insertion
    insert_query = sql.SQL('INSERT INTO {table} ({fields}) VALUES ({values})').format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    
    # Prepare the data for insertion
    values = [tuple(record[column] for column in columns) for record in json_data]
    
    try:
        # Execute the insertion for each record
        cursor.executemany(insert_query.as_string(conn), values)
        conn.commit()
        print(f"Inserted {cursor.rowcount} records into {table_name}")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    json_data = [
        {"column1": "value1", "column2": 123, "column3": "2024-06-22"},
        {"column1": "value2", "column2": 456, "column3": "2024-06-23"}
    ]
    
    conn_params = {
        "dbname": "your_dbname",
        "user": "your_user",
        "password": "your_password",
        "host": "your_host",
        "port": "your_port"
    }
    
    insert_json_to_postgres(json_data, "your_table", conn_params)
