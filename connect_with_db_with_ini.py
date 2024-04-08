[postgresql]
host = your_host
database = your_database
user = your_username
password = your_password




import psycopg2
from configparser import ConfigParser

def read_config(filename='config.ini', section='postgresql'):
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to postgresql
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db_config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Read connection parameters
        params = read_config()

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Execute a test query
        cur.execute('SELECT version()')

        # Display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(f'PostgreSQL database version: {db_version}')

        # Close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()
