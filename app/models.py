from hashlib import md5
import re
from app import db
from app import app



class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    out0 = db.Column(db.Integer)
    out1 = db.Column(db.Integer)
    out2 = db.Column(db.Integer)
    out3 = db.Column(db.Integer)
    out4 = db.Column(db.Integer)
    out5 = db.Column(db.Integer)
    out6 = db.Column(db.Integer)
    di0 = db.Column(db.Integer)
    di1 = db.Column(db.Integer)
    di2 = db.Column(db.Integer)
    di3 = db.Column(db.Integer)
    ia0 = db.Column(db.Integer)
    ia1 = db.Column(db.Integer)
    ia2 = db.Column(db.Integer)
    ia3 = db.Column(db.Integer)
    ia4 = db.Column(db.Integer)
    ia5 = db.Column(db.Integer)
    ia6 = db.Column(db.Integer)
    ia7 = db.Column(db.Integer)
    ia8 = db.Column(db.Integer)
    ia9 = db.Column(db.Integer)
    ia10 = db.Column(db.Integer)
    ia11 = db.Column(db.Integer)
    ia12 = db.Column(db.Integer)
    ia13 = db.Column(db.Integer)
    ia14 = db.Column(db.Integer)
    ia15 = db.Column(db.Integer)
    ia16 = db.Column(db.Integer)
    ia17 = db.Column(db.Integer)
    ia18 = db.Column(db.Integer)
    ia19 = db.Column(db.Integer)
    freq = db.Column(db.Integer)
    duty = db.Column(db.Integer)
    pwm = db.Column(db.Integer),
    sec0 = db.Column(db.Integer)
    sec1 = db.Column(db.Integer)
    sec2 = db.Column(db.Integer)
    sec3 = db.Column(db.Integer)
    sec4 = db.Column(db.Integer)
    dt = db.Column(db.DateTime)
