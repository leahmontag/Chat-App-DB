import re
from flask import Flask, render_template, request, redirect, session
import csv 
app = Flask(__name__)
# IS_DEV = app.env == 'development'
# relative_path = os.environ.get('RELATIVE_PATH', './templates')


@app.route('/register', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        f = open('users.csv', 'a')
        writer = csv.writer(f)
        writer.writerow([username,password])
        f.close()
        return redirect('/login')
    if request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        return redirect('/lobby')
    if request.method == 'GET':
        return render_template('login.html')

# @app.route('/lobby', methods=['GET', 'POST'])
# def lobby():
#     # if request.method == 'POST':
#     #     return redirect('/chat')
#     # if request.method == 'GET':
#         return render_template('lobby.html')   



@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            #todo:create room.txt
            print("CREATED NEW ROOM NAMED: " + room_name )
        return render_template('lobby.html')  
    else:
        return redirect('/login')


# @app.route('/chat')
# def chat_room():
#     return render_template('chat.html')    





#def validation():






#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    # guaranteed to not be run on a production server
    # assert os.path.exists('.env')  # for other environment variables...
    # os.environ['FLASK_ENV'] = 'development'  # HARD CODE since default is production
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)