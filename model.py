from rami import db
from datetime import datetime

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime)


    def __init__(self, message):
        self.message = message
        self.creation_date = datetime.utcnow()


class Forms(db.Model):
    __tablename__ = 'forms'
    id = db.Column(db.Integer, primary_key=True)
    formtype = db.Column(db.String(20))

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    numfields = db.Column(db.Integer, nullable=False)

    def __init__(self, name, numfields):
        self.name = name
        self.numfields = numfields

class studentNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(2323))
    notenum = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, note, notenum, student_id):
        self.note = note
        self.notenum = notenum
        self.student_id = student_id