from flask import Flask    

app = Flask(__name__)

@app.route('/')
def hello():
	return '<h1Hello World! This is my first app tutorial</h1>'
