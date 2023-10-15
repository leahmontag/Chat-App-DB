from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chat@secret'  # Set a secret key for session management

#-----------------------------------------------------------------------------
# MySQL Configuration
#-----------------------------------------------------------------------------

db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'chat_app_db'
}

#-----------------------------------------------------------------------------
# Helper functions
#-----------------------------------------------------------------------------

def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def check_user_credentials(username, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT Pw FROM users WHERE Username = %s", (username,))
    existing_password = cursor.fetchone()

    if existing_password and existing_password[0] == password:
        cursor.close()
        connection.close()
        return "you already registered, please login"
    else:
        cursor.close()
        connection.close()
        return "User with that name already exists" if existing_password else None

def add_user_to_db(username, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (Username, Pw) VALUES (%s, %s)", (username, password))
    connection.commit()
    cursor.close()
    connection.close()


def create_room(room_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO rooms (Room_Name) VALUES (%s)", (room_name,))
        connection.commit()

        # Retrieve the Room_ID of the created room
        cursor.execute("SELECT Room_ID FROM rooms WHERE Room_Name = %s", (room_name,))
        room_id = cursor.fetchone()[0]
        return room_id

    finally:
        cursor.close()
        connection.close()
    

def create_room_message(room_id, sender, message, timestamp):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO room_messages (Room_ID, Sender, Message, Timestamp) VALUES (%s, %s, %s, %s)",
            (room_id, sender, message, timestamp)
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

def get_room_messages(room_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT Sender, Message, Timestamp FROM room_messages "
            "INNER JOIN rooms ON room_messages.Room_ID = rooms.Room_ID "
            "WHERE rooms.Room_Name = %s", (room_name,)
        )
        messages = cursor.fetchall()

        message_list = []
        for message in messages:
            message_dict = {
                'Timestamp': message['Timestamp'],
                'Sender': message['Sender'],
                'Message': message['Message']
            }
            message_list.append(message_dict)

    finally:
        cursor.close()
        connection.close()

    return message_list


def valid_room_name(new_room_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT Room_Name FROM rooms WHERE Room_Name = %s", (new_room_name,))
    existing_room = cursor.fetchone()
    cursor.close()
    connection.close()
    return existing_room is None

def get_all_rooms():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT Room_Name FROM rooms")
    rooms = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return rooms


#-----------------------------------------------------------------------------
# MySQL
#-----------------------------------------------------------------------------

def users_data():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'chat_app_db'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT Username, Pw FROM users')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_room_id_by_name(room_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT Room_ID FROM rooms WHERE Room_Name = %s", (room_name,))
    room_id = cursor.fetchone()
    cursor.close()
    connection.close()
    return room_id[0] if room_id else None


#-----------------------------------------------------------------------------
# Routes
#-----------------------------------------------------------------------------

@app.route('/')
def index():
    return jsonify({'user Data': users_data()})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ans = check_user_credentials(username, password)
        if not ans:
            add_user_to_db(username, password)
            return redirect('/login')
        else:
            return ans
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if check_user_credentials(username, password) == "you already registered, please login":
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
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            if valid_room_name(room_name):
                room_id = create_room(room_name)  # Retrieve the Room_ID
            else:
                return "Oops... There is already an existing room named " + room_name + ". Please try another name"
        rooms = get_all_rooms()
        return render_template('lobby.html', all_rooms=rooms)
    else:
        return redirect('/login')

@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        return render_template('chat.html', room=room)
    else:
        return redirect('/login')

@app.route('/api/chat/<room>', methods=['GET', 'POST'])
def update_chat(room):
    if request.method == 'POST':
        message = request.form['msg']
        username = session['username']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Use the Room_ID when creating a message
        room_id = get_room_id_by_name(room)
        create_room_message(room_id, username, message, timestamp)

    # Retrieve chat history for the specified room
    messages = get_room_messages(room)

    return messages

        

@app.route("/health")
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
