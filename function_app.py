import azure.functions as func
import logging
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import requests

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

# def get_db_connection():
#     logging.info('Python HTTP trigger function processed a request.')
#     try:
#         conn = psycopg2.connect(
#             dbname=os.getenv("DB_NAME"),
#             user=os.getenv("DB_USER"),  
#             password=os.getenv("DB_PASSWORD"),
#             host=os.getenv("DB_HOST"),
#             port=os.getenv("DB_PORT"),
#         )
#         return conn
#     except Exception as e:
#         logging.error("Failed to connect to the database: %s", e)
#         return None
        

# @app.route(route="register", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
# def register(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')
    
#     path = req.route_params.get('action')
    
#     try:
#         req_body = req.get_json()
#     except ValueError:
#         return func.HttpResponse("Invalid JSON", status_code=400)
    
#     email = req_body.get('email')
#     password = req_body.get('password')  # Not hashing for simplicity as per instructions
    
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
    
#     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#     if cursor.fetchone():
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")

#     # Insert new user with plaintext password (not recommended)
#     cursor.execute(
#         "INSERT INTO users (email, password) VALUES (%s, %s)",  # Assuming the column is named 'password'
#         (email, password)
#     )
#     conn.commit()

#     cursor.close()
#     conn.close()
#     return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")

@app.route(route="login", auth_level=func.AuthLevel.ANONYMOUS)
def login(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing login request.')
    
    # path = req.route_params.get('action')
    email = req.params.get('email')
    password = req.params.get('password')
    
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)


    # email = req.params.get('email')
    # if not email:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         email = req_body.get('email')
            
    # if email:
    #     return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")
    # else:
    #      return func.HttpResponse("Not Found", status_code=404)
            
    # password = req.params.get('password')
    # if not password:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         password = req_body.get('password')
    
    # conn = get_db_connection()
    # cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # if email:
    #     return 
    
    # # email = req_body.get('email')
    # # password = req_body.get('password')
    
    # if not email or not password:
    #     return func.HttpResponse("Missing email or password", status_code=400)
    
    conn = get_db_connection()
    if conn is None:
        return func.HttpResponse("Database connection failed", status_code=500)

    else:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM reviews WHERE email = %s", (email,))
        user_data= cursor.fetchone()
        cursor.close()
        conn.close()
    try:
        # Example: check if user exists and verify password (pseudo-code)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Assuming you have a users table with email and password columns
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        
        if email == user_data['email'] and password == user_data['password']:
            return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
        
        cursor.close()
        conn.close()
        

        # if user_record and user_record['password'] == password:
        #     return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
        # else:
        #     return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")
    
    except Exception as e:
        logging.error("Database operation failed: %s", e)
        return func.HttpResponse("An error occurred", status_code=500)
    
    
    # conn = get_db_connection()
    # cursor = conn.cursor(cursor_factory=RealDictCursor)

    # cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    # user_data = cursor.fetchone()

    # if not user_data:
    #     cursor.close()
    #     conn.close()
    #     return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

    # if password == user_data['password']: 
    #     cursor.close()
    #     conn.close()
    #     return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
    # else:
    #     cursor.close()
    #     conn.close()
    #     return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")


# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),  
#         password=os.getenv("DB_PASSWORD"),
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#     )
#     return conn


# def simple_hash(password):
#     """A simple hashing function for demonstration. In production, use more secure methods."""
#     return sha256(password.encode('utf-8')).hexdigest()

# @app.route(route="register", auth_level=func.AuthLevel.ANONYMOUS)
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
    
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
    
#     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#     if cursor.fetchone():
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")

#     # Hash the password for storage
#     password_hash = simple_hash(password)

#     # Insert new user
#     cursor.execute(
#         "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
#         (email, password_hash)
#     )
#     conn.commit()

#     cursor.close()
#     conn.close()
#     return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")


# @app.route(route="login", auth_level=func.AuthLevel.ANONYMOUS)
# def login(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Processing login request.')
    
#     path = req.route_params.get('action')

#     try:
#         req_body = req.get_json()
#     except ValueError:
#         return func.HttpResponse("Invalid JSON", status_code=400)

#     email = req_body.get('email')
#     password = req_body.get('password')

#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)

#     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#     user_data = cursor.fetchone()

#     if not user_data:
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

#     # stored_password_hash = user_data['password_hash']
#     # if simple_hash(password) == stored_password_hash:
#     stored_password_hash = user_data['password']
#     if password == stored_password_hash:
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
#     else:
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")
