from app.app_and_db import db

class Message(db.Model):
    """ Message belongs to a conversation has many users """
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    conversation_id = db.Column(db.Integer(), db.ForeignKey('conversation.id', ondelete='CASCADE'))

    
class Conversation(db.Model):
    """ Conversation """
    id = db.Column(db.Integer, primary_key=True)

    
class UserConversations(db.Model):
    """ User has many conversations (join table)"""
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    conversation_id = db.Column(db.Integer(), db.ForeignKey('conversation.id', ondelete='CASCADE'))
    pass

