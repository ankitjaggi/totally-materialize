from flask import Flask, render_template, json, request, redirect, session, jsonify, flash
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

mysql = MySQL()
app = Flask(__name__)
app.secret_key = "vingardium leviosa"

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'golchacr7'
app.config['MYSQL_DATABASE_DB'] = 'lrlr'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Home Page Route
# If found a session, then re-direct to userHome
@app.route('/')
def home():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('landing_mat.html')

# Connecting the Signup with the database to handle the requests
@app.route('/signup', methods = ['POST'])
def signUp():
	_name = request.form['username_reg']
	_email = request.form['email_reg']
	_password = request.form['reg_password']

	# validate the form values
	if _name and _email and _password:
		return json.dumps({'html':'<span>All fields good !!</span>'})

		# all good. lets call MySQL
		conn = mysql.connect()
		cursor = conn.cursor()
		_hashed_password = generate_password_hash(_password)
		# Call the stored procedure for creating users
		cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
		data = cursor.fetchall()

		# if all went well
		if len(data) is 0:
			conn.commit()
			return json.dumps({'message':'User Created Successfully!'})
		# if error happended
		else:
			return json.dumps({'error': str(data[0])})

	else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run(port=80 , debug = True)