#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

# Generate a list of 4 random usernames
usernames = [fake.first_name() for _ in range(4)]

# Ensure "Duane" is always in the list
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    # Clear out all existing records in the Message table
    Message.query.delete()

    # Create a list of 20 new message objects
    messages = [
        Message(
            body=fake.sentence(),
            username=rc(usernames)  # Randomly choose a username
        )
        for _ in range(20)
    ]

    # Add all the new messages to the session and commit to the database
    db.session.add_all(messages)
    db.session.commit()        

if __name__ == '__main__':
    with app.app_context():
        make_messages()
        print(f"Seeded {len(usernames)} usernames and 20 messages.")
