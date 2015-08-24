from flask import Flask, render_template, json, request, redirect, session, jsonify, flash
import os

app = Flask(__name__)

@app.route('/')
def home():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('landingPage.html')

if __name__ == "__main__":
    app.run(port=80 , debug = True)