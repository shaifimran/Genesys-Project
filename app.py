import os
import google.generativeai as genai
from flask import Flask,request,jsonify,render_template,Response, session
import uuid
from dotenv import load_dotenv
import re

# Set your API key directly or fetch it from an environment variable.
# It's a good practice to store sensitive information like API keys in environment variables.
# GOOGLE_API_KEY = 'AIzaSyCYD0BvwLra2MKBHyizyavRNsOu75fujjQ'

app = Flask('__name__')
app.secret_key = os.urandom(24)

# Load environment variables from .env file
load_dotenv()


GOOGLE_API_KEY =  os.getenv('GOOGLE_API_KEY') 

# Ensure the API key is correctly retrieved
if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Make sure to set the GOOGLE_API_KEY environment variable.")

# Configure the genai library with the API key
genai.configure(api_key=GOOGLE_API_KEY)


safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
# Initialize the chat model
model = genai.GenerativeModel('gemini-pro',safety_settings=safe)
chat_sessions = {}

@app.route('/')
def render_home():
    return render_template('home.html')
@app.route('/about')
def render_about():
    return render_template('about.html')

@app.route('/chat')
def render_neutralized_chat():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    session['session_id'] = session_id
    session['once'] = False
    chat = model.start_chat(history=[])
    chat_sessions[session_id] = chat
    return render_template('chat.html')


@app.route('/chat/ask',methods=['POST'])   
def ask_query():
    data = request.json
    prompt = data.get('prompt')
    session_id = session.get('session_id')  # Retrieve session ID from the session

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    chat = chat_sessions.get(session_id)  # Retrieve the chat instance using session ID

    if not session.get('once'):
        prompt = "You are an AI assistant that is an expert in medical health called MedBot. You know about symptoms and signs of various types of illnesses. You can provide expert advice on self-diagnosis options in cases where an illness can be treated using a home remedy. If a query requires serious medical attention, recommend booking an appointment with doctors. If you are asked a question that is not related to medical health, respond with 'I'm sorry but your question is beyond my functionalities.'. Give properly formatted responses. If someone asks what can you do for me, tell him I am here to help you with any sickness or medical related queries." + prompt
        session['once'] = True

    response_text = ""
    response = chat.send_message(prompt, stream=True)

    def yield_text():
        for chunk in response:
            if chunk and chunk.text:
                chunk = re.sub(r'\*', '', chunk.text)
                chunk = re.sub(r':', ':\n', chunk)
                yield chunk

    return Response(yield_text(),mimetype='text/plain')      
            
if __name__ == '__main__':
    app.run() 
