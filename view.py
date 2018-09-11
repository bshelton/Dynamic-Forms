from rami import app, db
from flask import url_for, render_template, request, flash
from forms import newForm, lectureForm, newPageForm
from model import studentNotes, Student, studentPages
from wtforms import TextAreaField
import os
import json
import sqlalchemy

'''
This method renders a page. It requires a page id passed in.
'''

@app.route('/pages/<int:page>', methods=['GET'])
def displayPage(page):

    #This subclass is necessary to dynamically add fields to the form since we don't have a static amount of notes.
    class F(lectureForm):
        pass

    #Querying database to render notes/pages on the page
    all_notes = studentNotes.query.filter_by(page_id=page).all()
    all_pages = studentPages.query.filter_by(student_id=1).all()
    numnotes = len(all_notes)

    print ("number of notes for page: " + str(numnotes))

    #Dynmanically Setting the form fields with all notes from the database.
    for n in all_notes:
        setattr(F, str(n.notenum) ,TextAreaField(default=str(n.note)))

    #Creating the form object
    form1 = F()
    return render_template('pages.html', all_notes=all_notes, all_pages=all_pages, form1=form1, numnotes=numnotes, page=page)

'''
This method is used to pass the page clicked from ajax.
'''
@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.json # Receives data from the ajax post request

    newpageForm = newPageForm()
    all_pages = studentPages.query.filter_by(student_id=1).all()

    return render_template('index.html', newpageForm=newpageForm, all_pages=all_pages)

@app.route('/', methods=['GET','POST'])
def index():
    newpageForm = newForm()
    all_pages = studentPages.query.filter_by(student_id=1).all()
    return render_template('index.html', newpageForm=newpageForm, all_pages=all_pages) #Renders all forms on /index.html

'''
This method creates adds a new page to the database table "student_pages"
'''
@app.route('/createpage', methods=['POST'])
def createPage():

    newpageForm = newForm()

    #Receiving the data that was input on the form
    if request.method == "POST":
        title = request.form['message']

        #Adding the page to the database
        sp = studentPages(1,title)
        db.session.add(sp)
        db.session.commit()

    all_pages = studentPages.query.filter_by(student_id=1).all()
    all_notes = studentNotes.query.filter_by(page_id=all_pages[-1].id).all()
    numnotes = len(all_notes)

    return render_template('pages.html', all_pages=all_pages, newpageForm=newpageForm, title=title, numnotes=numnotes)

def get_notes():
    return studentNotes.query.filter_by(student_id=1).all()

@app.route('/addnotefield/pages/<int:page>', methods=['POST'])
def addnotefield(page):

    class F(lectureForm):
        pass

    #Getting the last note in the database
    notenum = getlastnotenum()
    
    stu = Student.query.filter_by(id=1).first()

    #Incrementing the number of fields for student by 1
    numfields = stu.numfields
    numfields = numfields + 1
    
    #Storing it back in the database
    stu.numfields = numfields
    db.session.commit()

    all_notes = studentNotes.query.filter_by(page_id=page).all()
    all_pages = studentPages.query.filter_by(student_id=1).all()
    numnotes = len(all_notes)


    #If number of notes is 0, then we need to create an empty note.
    if numnotes == 0:
        
        note = studentNotes('',1,1,page)

        #Setting field of form with no text and starting the id with 1.
        setattr(F, "1" ,TextAreaField(default="" , _name="1", id="1"))

        numnotes = numnotes +1
        db.session.add(note)
        db.session.commit()
    else:

        #Else the student already has some notes so just add
        numnotes = numnotes + 1
        newnote = studentNotes('', numnotes, 1, page)
        db.session.add(newnote)
        db.session.commit()

        #After adding a new note, query all to display on page
        notes = studentNotes.query.filter_by(student_id=1, page_id=page).all()

        for n in notes:
            print (str(n.notenum))
            setattr(F, str(n.notenum) ,TextAreaField(default=str(n.note),id=n.notenum))

    #Creating the form object
    form1 = F()

    return render_template('pages.html', form1=form1, numnotes=numnotes, all_pages=all_pages, all_notes=all_notes, page=page)

'''
This is a helper method that returns the last note
'''
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

        # This searches through what was submitted on the form, removing msg since it's the default field name.
        f = request.form
        for key in f.keys():
            for value in f.getlist(key):
                if not key == "msg":
                    if not key == "csrf_token":
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
