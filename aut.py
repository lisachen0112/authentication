import azure.functions as func
import logging
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from hashlib import sha256

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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
#     return sha256(password.encode('utf-8')).hexdigest()

# @app.route(route="/auth/{action}", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
# def auth(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Processing login request.')
#     action = req.route_params.get('action')
    
#     try:
#         req_body = req.get_json()
#     except ValueError:
#         return func.HttpResponse("Invalid JSON", status_code=400)
    
#     email = req_body.get('email')
#     password = req_body.get('password')
    
#     if not email or not password:
#         return func.HttpResponse(json.dumps({"error": "Missing email or password"}), status_code=400, mimetype="application/json")

#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#     try:
#         if action == 'register':
#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             if cursor.fetchone():
#                 return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")
            
#             password_hash = simple_hash(password)
#             cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
#             conn.commit()
#             return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")
        
#         elif action == 'login':
#             cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
#             user = cursor.fetchone()
#             if user and simple_hash(password) == user['password_hash']:
#                 return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
#             else:
#                 return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")
        
#         else:
#             return func.HttpResponse("Not Found", status_code=404)
    
#     finally:  
#         cursor.close()
#         conn.close()
        
# ### 2 codes below have more clarityimport azure.functions as func
# import logging
# import json
# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from hashlib import sha256

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# # Function to establish a database connection
# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#     )
#     return conn

# # Function to hash the password
# def simple_hash(password):
#     return sha256(password.encode('utf-8')).hexdigest()

# # Route handler for authentication actions (register/login)
# @app.route(route="/auth/{action}", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
# def auth(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Processing authentication request.')

#     # Extract action from route parameter
#     action = req.route_params.get('action')
    
#     # Attempt to parse JSON body from the request
#     try:
#         req_body = req.get_json()
#     except ValueError:
#         return func.HttpResponse("Invalid JSON", status_code=400)
    
#     # Extract email and password from the request body
#     email = req_body.get('email')
#     password = req_body.get('password')
    
#     # Validate email and password presence
#     if not email or not password:
#         return func.HttpResponse(json.dumps({"error": "Missing email or password"}), status_code=400, mimetype="application/json")

#     # Establish database connection
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#     try:
#         if action == 'register':
#             # Check if the user already exists
#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             if cursor.fetchone():
#                 return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")
            
#             # Hash password and insert new user into the database
#             password_hash = simple_hash(password)
#             cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
#             conn.commit()
#             return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")
        
#         elif action == 'login':
#             # Retrieve the user's password hash from the database
#             cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
#             user = cursor.fetchone()
#             if user and simple_hash(password) == user['password_hash']:
#                 # Login successful
#                 return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
#             else:
#                 # Invalid credentials
#                 return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")
        
#         else:
#             # Action not found
#             return func.HttpResponse("Not Found", status_code=404)
    
#     finally:  
#         # Close cursor and connection to free resources
#         cursor.close()
#         conn.close()

# import azure.functions as func
# import logging
# import json
# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from hashlib import sha256

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# # Database connection helper function
# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),  
#         password=os.getenv("DB_PASSWORD"),
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#     )
#     return conn

# # Simple hash function for password hashing
# def simple_hash(password):
#     return sha256(password.encode('utf-8')).hexdigest()

# # Route for handling authentication actions (register/login)
# @app.route(route="/auth/{action}", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
# def auth(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Processing authentication request.')
#     action = req.route_params.get('action')  # Determine the action from URL parameter
    
#     # Attempt to parse JSON request body
#     try:
#         req_body = req.get_json()
#     except ValueError:
#         # JSON parsing failed
#         return func.HttpResponse("Invalid JSON", status_code=400)
    
#     email = req_body.get('email')
#     password = req_body.get('password')
    
#     # Check for missing required fields
#     if not email or not password:
#         return func.HttpResponse(json.dumps({"error": "Missing email or password"}), status_code=400, mimetype="application/json")

#     # Establish database connection
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#     try:
#         if action == 'register':
#             # Check if user already exists
#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             if cursor.fetchone():
#                 # User already exists
#                 return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")
            
#             # Register new user
#             password_hash = simple_hash(password)
#             cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
#             conn.commit()  # Commit changes to database
#             # Registration successful
#             return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")
        
#         elif action == 'login':
#             # Attempt to find user by email
#             cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
#             user = cursor.fetchone()
#             if user and simple_hash(password) == user['password_hash']:
#                 # Login successful
#                 return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
#             else:
#                 # Invalid credentials
#                 return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")
        
#         else:
#             # Action not found (neither register nor login)
#             return func.HttpResponse("Not Found", status_code=404)
    
#     finally:  
#         # Ensure database connections are closed properly
#         cursor.close()
#         conn.close()


###


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

#     stored_password_hash = user_data['password_hash']
#     if simple_hash(password) == stored_password_hash:
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
#     else:
#         cursor.close()
#         conn.close()
#         return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")