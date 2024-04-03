from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Function to execute PostgreSQL stored procedure
def call_stored_procedure(json_data):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname='your_database_name',
        user='your_database_user',
        password='your_database_password',
        host='your_database_host'
    )
    cursor = conn.cursor()

    # Execute the stored procedure
    cursor.callproc('your_stored_procedure_name', [json_data])

    # Fetch the result
    result = cursor.fetchone()[0]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return result

# Define API route to accept JSON requests
@app.route('/call_stored_procedure', methods=['POST'])
def handle_request():
    try:
        # Get JSON data from request
        json_data = request.json

        # Call stored procedure with JSON data
        response = call_stored_procedure(json_data)

        # Return JSON response
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
