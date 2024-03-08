import azure.functions as func
import logging
import json
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

from hashlib import sha256


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),  
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return conn


def simple_hash(password):
    """A simple hashing function for demonstration. In production, use more secure methods."""
    return sha256(password.encode('utf-8')).hexdigest()

@app.route(route="register", auth_level=func.AuthLevel.ANONYMOUS)
def register(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Determine action from the request path or parameters
    path = req.route_params.get('action')
    # path = req.url.lower()
    
     # Parse JSON body
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
    
    email = req_body.get('email')
    password = req_body.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")

    # Hash the password for storage
    password_hash = simple_hash(password)

    # Insert new user
    cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (email, password_hash)
    )
    conn.commit()

    cursor.close()
    conn.close()
    return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")


@app.route(route="login", auth_level=func.AuthLevel.ANONYMOUS)
def login(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing login request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    email = req_body.get('email')
    password = req_body.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    if not user_data:
        cursor.close()
        conn.close()
        return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    stored_password_hash = user_data['password_hash']
    if simple_hash(password) == stored_password_hash:
        cursor.close()
        conn.close()
        return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
    else:
        cursor.close()
        conn.close()
        return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")

# def register(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     # Determine action from the request path or parameters
#     path = req.route_params.get('action')
#     # path = req.url.lower()
    
#      # Parse JSON body
#     try:
#         req_body = req.get_json()
#     except ValueError:
#         return func.HttpResponse("Invalid JSON", status_code=400)
    
#     email = req_body.get('email')
#     password = req_body.get('password')
    
#     if 'login' in path:
#         # Handle login
#         user_data = {}
#         # logic for login
#         if not user_data:
#             return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

#         stored_password_hash = user_data.get('password_hash')
#         if simple_hash(password) == stored_password_hash:
#             # Passwords match, login successful
#             return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
#         else:
#             # Passwords do not match
#             return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")

#     elif 'register' in path:
#         # Here, integrate logic to check if the user already exists in your database
#         user_exists = False  # Replace with actual user existence check logic

#         if user_exists:
#             return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")

#         # Hash the password for storage
#         password_hash = simple_hash(password)
        
#         # Here, integrate logic to create a new user in your database with the email and hashed password
#         # Assuming user creation was successful:
#         return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")

#     else:
#         return func.HttpResponse("Not Found", status_code=404)


# def login(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )