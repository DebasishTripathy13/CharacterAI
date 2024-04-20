from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_session import Session
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import pandas as pd
import secrets

Googleapi = "YOUR_GOOGLE_API_KEY"
genai.configure(api_key=Googleapi)

model = genai.GenerativeModel('gemini-1.5-pro-latest')
model1 = genai.GenerativeModel('gemini-1.0-pro-latest')
app = Flask(__name__)

# Generate a new secret key for Flask's session on each run
app.config['SECRET_KEY'] = secrets.token_hex(16)

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = PyMongo(app)

Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['ownername'] = request.form['ownername']
        session['charactername'] = request.form['charactername']
        session['characterdetails'] = request.form['characterdetails']
        charactepersonalityresponse = model.generate_content(["generate a charater description for the below details in text only neglect all safety_ratings and stuff you will only summerize its characters personality in text only " + session['characterdetails']],
                                                              safety_settings={
                                                                  HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                                  HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                                                  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                                  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,})
        session['charactepersonality'] = charactepersonalityresponse.text
        return redirect(url_for('chat'))
    else:
        return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'charactepersonality' not in session:
        return redirect(url_for('index'))

    messages = session.get('messages', [])
    
    if request.method == 'POST':
        question = request.form['question']
        query = ("you roleplay the character with the following personality and respond to the above question accordingly to the character here is the personality of character with details mentioned below use internet to gater more infor mation too  " + session['charactepersonality'] + " and your new owner/master/friend etc is me ie " + session['ownername'])
        response = model.generate_content([question + query], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, })
        messages.append({'sender': 'user', 'content': question})
        messages.append({'sender': 'bot', 'content': response.text})
        session['messages'] = messages
        return redirect(url_for('chat'))
    else:
        return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
