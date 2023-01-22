from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
api = Api(app)


class HelloWorld(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)


class HelloWorldResource(Resource):
    def get(self):
        message = HelloWorld.query.first()
        return {"message": message.message}


db.create_all()
db.session.add(HelloWorld(message="Hello World!"))
db.session.commit()

api.add_resource(HelloWorldResource, '/helloworld')

if __name__ == '__main__':
    app.run(debug=True)
