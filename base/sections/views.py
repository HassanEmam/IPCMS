from IPCMS import app, db
from base.sections.form import SectionForm
from base.project.models import Project
from flask import render_template
from base.users.decorators import *
from base.sections.models import Section
import json

@app.route('/newsection', methods=['POST', 'GET'])
@login_required
@project_required
def new_section():
    
    form = SectionForm()
    form.parent.query = Section.query.filter_by(project_id = session.get('project_id'))
    print(session['project_id'])
    if request.method == "POST" and form.validate() and session.get('project_id'):
        
        section = Section (code= form.code.data, 
                            name= form.name.data, 
                            project= Project.query.filter_by(id=session['project_id']).first(),
                            parent= form.parent.data,
                            active= form.active.data)
        try:
            db.session.add(section)
            db.session.flush()
            db.session.commit()
        except:
            flash('Duplicate entries not allowed', 'alert-danger')
            return redirect(url_for('new_section'))
        return redirect(url_for('view_sections'))
    return render_template('sections/sectionform.html', form=form, action='new')
    
    
@app.route('/viewsections')
@login_required
@project_required
def view_sections():
    sections = Section.query.filter_by(project_id=session['project_id']).all()
    print (sections)
    return render_template('sections/view.html', sections=sections)
    
@app.route('/viewsection/<id>')
@login_required
@project_required
def section_details(id):
    section = Section.query.filter_by(id= id, project_id= session['project_id']).first()
    return render_template('sections/details.html', section=section)


@app.route('/editsection/<id>', methods=['GET', 'POST'])
@login_required
@project_required
def edit_section(id):
    section = Section.query.filter_by(id= id).first()
    form = SectionForm(obj=section)
    form.parent.query = Section.query.filter_by(project_id = session.get('project_id'))
    if request.method == "POST" and form.validate():
        section.code = form.code.data
        section.name = form.name.data
        secion.parent = form.parent.data
        section.active = form.active.data
        
        db.session.add(section)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('view_sections'))
    return render_template('sections/sectionform.html', form = form, section=section, action='edit')
    
def sub(sections, id, level):
    ul=[]
    level +=1
    for section in sections:
        if section.parent_id == id:
            sectionjson = section.json()
            sectionjson["level"] = level
            children = sub(sections, section.id, level)
            sectionjson["childs"] = children
            ul.append(sectionjson)
    return ul
            
@app.route('/sectionsorder')
def sections_ordered():
    sections = Section.query.filter_by(project_id= session.get('project_id')).all()
    ul=[]
    level = 1
    for section in sections:
        if section.parent == None:
            sectionjson = section.json()
            sectionjson["level"] = level
            #sectionjson["childs"]=[]
            children = sub(sections, section.id, level)
            sectionjson["childs"] = children
            ul.append(sectionjson)
    return json.dumps(ul)