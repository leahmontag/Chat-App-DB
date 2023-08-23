from curses import flash
from flask import Flask, render_template, request, redirect, session, flash, jsonify
import csv
import os
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Retrieve the room files path from environment variable
#room_files_path = os.getenv('ROOM_FILES_PATH')
room_files_path = "rooms/"

# Helper functions for user authentication
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def check_user_credentials(username, password):
    with open('users.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == username:
                if decode_password(row[1]) != password:
                     return "user with that name already exist"
                else:
                     return "you already registered, please login"
    return False

def add_user_to_csv(username, encoded_password):
    # Save user details to the CSV file
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, encoded_password])

 

# Routes
@app.route('/')
def index():
    return "WELCOME"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encoded_password = encode_password(password)
        ans = check_user_credentials(username, password)
        if not ans:
            add_user_to_csv(username, encoded_password)
            return redirect('/login')
        else:
            return ans
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if check_user_credentials(username, password):
            session['username'] = username
            return redirect('/lobby')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')



@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    # if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            #todo:create room.txt
            path=os.getenv('ROOM_FILES_PATH')+room_name+".txt"
            room =  open(path, 'w')  
            return room_name
        return render_template('lobby.html')  
    # else:
    #     return redirect('/login')

@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        if request.method == 'POST':
            message = request.form['msg']
            print("MESSAGE RECEIVED IN CHAT " + message )
        return render_template('chat.html', room=room)
    else:
        return redirect('/login')

@app.route('/api/chat/<room>', methods=['POST'])
def update_chat(room):
    message = request.json['message']
    username = session['username']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Append the message to the room's unique .txt file
    with open(f'{room_files_path}/{room}.txt', 'a') as file:
        file.write(f'[{timestamp}] {username}: {message}\n')
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
