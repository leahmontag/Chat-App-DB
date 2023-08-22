from flask import Flask, render_template, request, redirect
# import os 
app = Flask(__name__)
# IS_DEV = app.env == 'development'
# relative_path = os.environ.get('RELATIVE_PATH', './templates')


@app.route('/register', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        return redirect('/login')
    if request.method == 'GET':
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        return redirect('/lobby')
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/lobby')
def lobby():
    return render_template('lobby.html')   

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    # guaranteed to not be run on a production server
    # assert os.path.exists('.env')  # for other environment variables...
    # os.environ['FLASK_ENV'] = 'development'  # HARD CODE since default is production
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)