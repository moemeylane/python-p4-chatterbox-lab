from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from sqlalchemy.orm import session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_json = [message.to_dict() for message in messages]
        return make_response(jsonify(messages_json), 200)
    except Exception as e:
        return make_response({'error': str(e)}, 500)

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    try:
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username'),
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)
    except IntegrityError as e:
        db.session.rollback()  # Rollback in case of failure
        return make_response({'error': 'Failed to create message, invalid data.'}, 400)
    except Exception as e:
        return make_response({'error': str(e)}, 500)

# Route to update an existing message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    try:
        message = db.session.get(Message, id)  # Updated to use session.get()
        if message is None:
            return make_response({'error': 'Message not found'}, 404)

        data = request.get_json()
        message.body = data.get('body', message.body)  # Update the body if provided
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)
    except Exception as e:
        return make_response({'error': str(e)}, 500)

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        message = db.session.get(Message, id)  # Updated to use session.get()
        if message is None:
            return make_response({'error': 'Message not found'}, 404)

        db.session.delete(message)
        db.session.commit()
        return make_response({'message': 'Message deleted successfully'}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 500)

if __name__ == '__main__':
    app.run(port=5555)
