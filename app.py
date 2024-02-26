from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

app.config['DIR'] = "static"

@app.route('/')
def send_main_page():
    return render_template('index.html')

connect = sqlite3.connect('database.db')
connect.execute('CREATE TABLE IF NOT EXISTS PARTICIPANTS (name Text,email Text)')

@app.route('/join', methods=['POST'])
def join_us():
    if request.method == 'post':  # <-- Should be lowercase 'post'
        name = request.form['name']
        email = request.form['email']

        file = request.files['file']  # <-- Corrected accessing files
        file.save(os.path.join(app.config['DIR'],file.filename))

        with sqlite3.connect('database.db') as users:
            cursor = users.cursor()
            cursor.execute('INSERT INTO PARTICIPANTS (name,email) VALUES (?,?)', (name, email))
            users.commit()
            return render_template('done.html')
    return render_template('index.html')

@app.route('/users')
def print_results():
    with sqlite3.connect('database.db') as user:
        cursor = user.cursor()
        cursor.execute('SELECT * FROM PARTICIPANTS')
        participants = cursor.fetchall()
        print(participants)
    return render_template('done.html', participants=participants)  # <-- Changed template name and passed correct data variable name


