from rami import app, db
from flask import url_for, render_template, request, flash
from forms import DataForm, newForm, lectureForm, newPageForm
from model import Data, studentNotes, Student, studentPages
from wtforms import TextAreaField
import os
import json
import sqlalchemy

@app.route('/pages/<int:page>', methods=['GET'])
def displayPage(page):

    class F(lectureForm):
        pass
    print ("page: " + str(page))

    all_notes = studentNotes.query.filter_by(page_id=page).all()
    all_pages = studentPages.query.filter_by(student_id=1).all()
    numnotes = len(all_notes)

    print ("number of notes for page: " + str(numnotes))

    for n in all_notes:
        setattr(F, str(n.notenum) ,TextAreaField(default=str(n.note)))

    form1 = F()
    return render_template('pages.html', all_notes=all_notes, all_pages=all_pages, form1=form1, numnotes=numnotes, page=page)

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.json

    print (jsdata['javascript_data'])


    newpageForm = newPageForm()
    all_pages = studentPages.query.filter_by(student_id=1).all()

    return render_template('index.html', newpageForm=newpageForm, all_pages=all_pages)

@app.route('/', methods=['GET','POST'])
def index():
    newpageForm = newForm()
    all_pages = studentPages.query.filter_by(student_id=1).all()
    return render_template('index.html', newpageForm=newpageForm, all_pages=all_pages) #Renders all forms on /index.html

@app.route('/createpage', methods=['POST'])
def createPage():

    newpageForm = newForm()

    if request.method == "POST":
        title = request.form['message']
        print (title)

        sp = studentPages(1,title)
        db.session.add(sp)
        db.session.commit()

        flash("Page Created")

    all_pages = studentPages.query.filter_by(student_id=1).all()
    all_notes = studentNotes.query.filter_by(page_id=all_pages[-1].id).all()
    numnotes = len(all_notes)

    return render_template('pages.html', all_pages=all_pages, newpageForm=newpageForm, title=title, numnotes=numnotes)


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

     all_pages = studentPages.query.filter_by(student_id=1).all()

     return render_template('lecture_notes.html', notes=notes, form1=form1, numnotes=numnotes, all_pages=all_pages)


def get_notes():
    return studentNotes.query.filter_by(student_id=1).all()

@app.route('/addnotefield/pages/<int:page>', methods=['POST'])
def addnotefield(page):
    class F(lectureForm):
        pass

    notenum = getlastnotenum()
    
    stu = Student.query.filter_by(id=1).first()

    numfields = stu.numfields

    numfields = numfields + 1

    stu.numfields = numfields
    db.session.commit()

    all_notes = studentNotes.query.filter_by(page_id=page).all()
    all_pages = studentPages.query.filter_by(student_id=1).all()
    numnotes = len(all_notes)

    print ("Page that field was added: " + str(page))

    if numnotes == 0:
        print ("null")
        note = studentNotes('',1,1,page)
        setattr(F, "1" ,TextAreaField(default="" , _name="1", id="1"))

        numnotes = numnotes +1
        db.session.add(note)
        db.session.commit()
    else:
        numnotes = numnotes + 1
        newnote = studentNotes('', numnotes, 1, page)
        db.session.add(newnote)
        db.session.commit()

        print ("numnotes: " +str(numnotes))
        notes = studentNotes.query.filter_by(student_id=1, page_id=page).all()
        for n in notes:
            print (str(n.notenum))
            setattr(F, str(n.notenum) ,TextAreaField(default=str(n.note),id=n.notenum))

    form1 = F()
    return render_template('pages.html', form1=form1, numnotes=numnotes, all_pages=all_pages, all_notes=all_notes, page=page)

def getlastnotenum():

    lastnotenum = studentNotes.query.filter_by(student_id=1).first()
    
    if lastnotenum is None:
        return "null"
    else:
        return lastnotenum.notenum

@app.route('/savenotes/pages/<int:page>', methods=['POST'])
def savenotes(page):
    class F(lectureForm):
        pass
    
    print ("Page: " + str(page))

    if request.method == "POST":
    
        index = 0

        #Get student
        stu = Student.query.filter_by(id=1).first()

        #number of student feilds currently
        numfields = stu.numfields
  
        #Number of fields in the notes tables that the student has
        stunotes = studentNotes.query.filter_by(student_id=1, page_id=page).all()
        
        stunotesnum = len(stunotes)
        print ("Number of student notes: " + str(stunotesnum))

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

        index = 0

        #Retreives all notes to render on page
        notes = get_notes()

        numnotes = len(notes)
        form1 = F()

        all_pages = studentPages.query.filter_by(student_id=1).all()

    return render_template('pages.html',notes=notes, form1=form1, numnotes=numnotes, all_pages=all_pages, page=page)
