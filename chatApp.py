from flask import Flask, render_template
# import os 
app = Flask(__name__)
# IS_DEV = app.env == 'development'
# relative_path = os.environ.get('RELATIVE_PATH', './templates')


@app.route('/register')
def homePage():
    return render_template('register.html')

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    # guaranteed to not be run on a production server
    # assert os.path.exists('.env')  # for other environment variables...
    # os.environ['FLASK_ENV'] = 'development'  # HARD CODE since default is production
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)