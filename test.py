from flask import Flask, request, jsonify, Response, render_template, session
import requests
import uuid
import os
from dotenv import load_dotenv

app = Flask('__name__')
app.secret_key = os.urandom(24)

# Load environment variables from .env file
load_dotenv()

# Replace with your ngrok URL for the model
KAGGLE_MODEL_API_URL = "https://ed5a-34-132-97-98.ngrok-free.app"  # Update this if the URL changes

@app.route('/')
def render_home():
    return render_template('home.html')

@app.route('/chat')
def render_neutralized_chat():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    session['chat_type'] = 'neutralized'
    session['session_id'] = session_id
    session['once'] = False
    return render_template('chat.html')

@app.route('/chat/ask', methods=['POST'])
def ask_query():
    data = request.json
    prompt = data.get('prompt')
    chat_type = session.get('chat_type')  # Retrieve chat type from the session
    session_id = session.get('session_id')  # Retrieve session ID from the session

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Make a POST request to the Kaggle model API
        response = requests.post(KAGGLE_MODEL_API_URL, json={"input": prompt})
        response.raise_for_status()

       # Extract the relevant part from the response
        response_text = response.json().get('text')
        response_part = response_text.split('### Response:')[1].strip() if '### Response:' in response_text else response_text
        return jsonify({"response": response_part})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
