from app.app_and_db import db
            
class Blast(db.Model):
    """ Blast """
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime)
    status = db.Column(db.String(), nullable=False, default="Pending")
    creater = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserBlasts(db.Model):
    """ User has many blasts (join table)"""
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    blast_id = db.Column(db.Integer(), db.ForeignKey('blast.id', ondelete='CASCADE'))
    

class ThunderStorm(db.Model):
    """ User has many thunderstorms """
    id = db.Column(db.Integer, primary_key=True)
    creation = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(), nullable=False, default="Pending")


