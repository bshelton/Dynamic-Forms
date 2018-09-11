from rami import db
from datetime import datetime

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
    page_id = db.Column(db.Integer, db.ForeignKey('student_pages.id'))

    def __init__(self, note, notenum, student_id,page_id):
        self.note = note
        self.notenum = notenum
        self.student_id = student_id
        self.page_id = page_id

'''
This class is to keep track of pages created.

'''
class studentPages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    page_name = db.Column(db.String(30), nullable=False)

    def __init__(self, student_id, page_name):
        self.student_id = student_id
        self.page_name = page_name