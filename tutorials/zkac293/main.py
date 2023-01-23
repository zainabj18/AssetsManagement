from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)

class HelloWorldDB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(20))

def __init__(self, text):
    self.text = text

class HelloWorld(Resource):
    @app.route('/')
    def helloWorld(text):
        helloWorldTest = HelloWorldDB(text = text)
        db.session.add(helloWorldTest)
        db.session.commit()
        #return '<h1>Added new text</h1>'
        return render_template('helloWorldPage.html')

api.add_resource(HelloWorld, '/helloworld')

if __name__ == "__main__":
    app.run(debug = True)