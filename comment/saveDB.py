from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define Comment model
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    comment_text = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'

# Define API endpoint for comment submission
@app.route('/comments', methods=['POST'])
def submit_comment():
    # Validate input data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    if 'name' not in data or 'email' not in data or 'comment_text' not in data:
        return jsonify({'error': 'Name, email or comment text missing'}), 400

    # Save the comment data to the database
    comment = Comment(
        name=data['name'],
        email=data['email'],
        comment_text=data['comment_text']
    )
    db.session.add(comment)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Comment submitted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
