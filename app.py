from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_session import Session
from flask_bcrypt import Bcrypt
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import pandas as pd
import secrets
import time


app = Flask(__name__)
bcrypt = Bcrypt(app)

Googleapi = "own gemini key"
genai.configure(api_key=Googleapi)

model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat1 = model.start_chat(history=[])

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = PyMongo(app)
Session(app)

mongo = PyMongo(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})
        if user and user['password'] == password:
            session['user_id'] = str(user['_id'])
            session['email'] = user['email']
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            flash('User already exists, please login', 'error')
            return redirect(url_for('login'))
        else:
            new_user = {'email': email, 'password': password}
            mongo.db.users.insert_one(new_user)
            flash('Registration successful, please login', 'success')
            return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['ownername'] = request.form['ownername']
        session['charactername'] = request.form['charactername']
        session['characterdetails'] = request.form['characterdetails']
        charactepersonalityresponse = chat1.send_message([
            "generate a charater description for the below details in text only neglect all safety_ratings and stuff you will only summerize its characters personality in text only " + session['characterdetails']],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, })

        session['charactepersonality'] = charactepersonalityresponse.text
        return redirect(url_for('chat'))
    else:
        return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'charactepersonality' not in session:
        return redirect(url_for('index'))

    messages = session.get('messages', [])
    
    if request.method == 'POST':
        question = request.form['question']
        query = ("use the previos history to continue the the conversation  if any available and you roleplay the character with the following personality and respond to the above question accordingly to the character here is the personality of character with details mentioned below use internet to gater more infor mation too  " + session['charactepersonality'] + " and your new owner/master/friend etc is me ie " + session['ownername'])
        response = chat1.send_message([question + query], safety_settings={
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
