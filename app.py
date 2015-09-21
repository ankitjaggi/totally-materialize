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
def signup():
	try:
		_name = request.form['username_reg']
		_email = request.form['email_reg']
		_password = request.form['reg_password']

		# validate the form values
		if _name and _email and _password:
			# return json.dumps({'html':'<span>All fields good !!</span>'})

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
				return json.dumps({'message': (data[0])})

		else:
			return json.dumps({'message':'<span>Enter the required fields</span>'})
	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()
		conn.close()

@app.route('/validateLogin', methods = ['POST'])
def validateLogin():
	try:
		_username = request.form['login_email']
		_password = request.form['login_password']

		if _username and _password:

			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.callproc('sp_validateLogin', (_username,))
			data = cursor.fetchall()

			if len(data) > 0:
				if check_password_hash(str(data[0][3]), _password):
					session['user'] = data[0][0]
					return redirect('/userHome')
				else:
					return json.dumps({'message':"Password don't match. Try again"})
			else:
				return json.dumps({'message':'Username either wrong or not registered.'})
		else:
			return json.dumps({'message':'Enter the required fields'})
	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()
		conn.close()

@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html', error = "Unauthorised Access!.Login or Register.")

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')

if __name__ == "__main__":
    app.run(port=80 , debug = True)