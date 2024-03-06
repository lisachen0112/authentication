import azure.functions as func
import logging
import json
import requests
from hashlib import sha256


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def simple_hash(password):
    """A simple hashing function for demonstration. In production, use more secure methods."""
    return sha256(password.encode('utf-8')).hexdigest()


def Authentication(req: func.HttpRequest) -> func.HttpResponse:
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
    
    if 'login' in path:
        # Handle login
        user_data = {}
        # logic for login
        if not user_data:
            return func.HttpResponse(json.dumps({"error": "User not found"}), status_code=404, mimetype="application/json")

        stored_password_hash = user_data.get('password_hash')
        if simple_hash(password) == stored_password_hash:
            # Passwords match, login successful
            return func.HttpResponse(json.dumps({"message": "Login successful"}), status_code=200, mimetype="application/json")
        else:
            # Passwords do not match
            return func.HttpResponse(json.dumps({"error": "Invalid credentials"}), status_code=401, mimetype="application/json")

    elif 'register' in path:
        # Here, integrate logic to check if the user already exists in your database
        user_exists = False  # Replace with actual user existence check logic

        if user_exists:
            return func.HttpResponse(json.dumps({"error": "User already exists"}), status_code=409, mimetype="application/json")

        # Hash the password for storage
        password_hash = simple_hash(password)
        
        # Here, integrate logic to create a new user in your database with the email and hashed password
        # Assuming user creation was successful:
        return func.HttpResponse(json.dumps({"message": "User registered successfully"}), status_code=201, mimetype="application/json")

    else:
        return func.HttpResponse("Not Found", status_code=404)

