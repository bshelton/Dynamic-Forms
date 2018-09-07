from rami import app, db
from flask import url_for, render_template, request, flash
from forms import DataForm, newForm, lectureForm
from model import Data, studentNotes, Student
from wtforms import TextAreaField
import os
import sqlalchemy

forms = [] # Array that holds all the forms ever created
pagenum =0

lecturenotefields = []
counter = len(lecturenotefields)

@app.route('/', methods=['GET','POST'])
def index():
    newpageForm = newForm()
    return render_template('index.html', newpageForm=newpageForm) #Renders all forms on /index.html

@app.route('/createpage', methods=['POST'])
def createPage():
    newpageForm = newForm()

    global pagenum
    filename = str(pagenum)
    f = open("page"+filename+".html",'w+')
    for i in range(10):
        f.write("<html> </html>")
    f.close()
    pagenum = pagenum + 1
    flash("Page Created")

    return render_template('index.html', newpageForm=newpageForm)


@app.route('/lecture_notes', methods=['GET', 'POST'])
def lecture_notes():
     class F(lectureForm):
        pass

     stu = Student.query.filter_by(id=1).first()

     numfields = stu.numfields

     notes = studentNotes.query.filter_by(student_id=1).all()
     
     numnotes = len(notes)

     for n in notes:
        setattr(F, str(n.notenum) ,TextAreaField(default=str(n.note)))

     form1 = F()

     return render_template('lecture_notes.html', notes=notes, form1=form1, numnotes=numnotes)


def get_notes():
    return studentNotes.query.filter_by(student_id=1).all()

@app.route('/addnotefield', methods=['POST'])
def addnotefield():
    class F(lectureForm):
        pass

    notenum = getlastnotenum()
    
    stu = Student.query.filter_by(id=1).first()

    numfields = stu.numfields

    numfields = numfields + 1

    stu.numfields = numfields
    db.session.commit()

    notes = studentNotes.query.filter_by(student_id=1).all()
    numnotes = len(notes)

    if notenum == "null":
        print ("null")
        note = studentNotes('',1,1)
        setattr(F, "1" ,TextAreaField(default="" , _name="1", id="1"))

        numnotes = numnotes +1
        db.session.add(note)
        db.session.commit()
    else:
        newnote = studentNotes('', numfields, 1)
        db.session.add(newnote)
        db.session.commit()

        numnotes = numnotes + 1

        print ("numnotes: " +str(numnotes))
        notes = studentNotes.query.filter_by(student_id=1).all()
        for n in notes:
            print (str(n.notenum))
            setattr(F, str(n.notenum) ,TextAreaField(default=str(n.note),id=n.notenum))

    form1 = F()
    return render_template('lecture_notes.html', form1=form1, numnotes=numnotes)

def getlastnotenum():

    lastnotenum = studentNotes.query.filter_by(student_id=1).first()
    
    if lastnotenum is None:
        return "null"
    else:
        return lastnotenum.notenum

@app.route('/savenotes', methods=['POST'])
def savenotes():
    class F(lectureForm):
        pass

    if request.method == "POST":
        print("posted")
    
        index = 0

        #Get student
        stu = Student.query.filter_by(id=1).first()

        #number of student feilds currently
        numfields = stu.numfields

        #Number of fields sent from the page
        numsavedfields = len(request.form.getlist('text'))
  
        #Number of fields in the notes tables that the student has
        stunotes = studentNotes.query.filter_by(student_id=1).all()
        
        stunotesnum = len(stunotes)

        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                if not key == "msg":
                    if not key == "csrf_token":
    
                        print (key, value)
                        print ("index:" + str(index))
                        setattr(F ,key, TextAreaField(default= value))
                        stunotes[index].note = value
                        db.session.commit()
                        index=index+1
                

        if numfields > stunotesnum:
            print ("student added new fields")

            #Adding a new note into the db
            newnote = studentNotes('', getlastnotenum()+1, 1)
            db.session.add(newnote)
            db.session.commit()
            setattr(F,getlastnotenum()+1,'')
            stunotesnum = stunotesnum + 1
        else:
            print("no fields added")

        index = 0

        #Retreives all notes to render on page
        notes = get_notes()

        numnotes = len(notes)
        form1 = F()
    return render_template('lecture_notes.html',notes=notes, form1=form1, numnotes=numnotes)

'''
This method will create a new form and add it the forms array
Then it will return refresh the screen.
'''
@app.route('/addform', methods=['GET','POST'])
def addform():
    with app.app_context(): #Needed since forms is a global variable
        if request.method == "POST": 
            forms.append(newForm(message="asd"))
            global counter 
            counter = counter+1
        
        return render_template('index.html', forms=forms, counter=counter)

