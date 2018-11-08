from IPCMS import app, db
from base.calendars.form import CycleForm
from base.calendars.models import ReportingCycle
from flask import render_template, redirect, url_for, request, session, flash
from base.users.decorators import login_required, admin_required
from base.organisations.models import Organisation
from sqlalchemy import exc

'''
This code controls the creation, editing, viewing and deleting of organisations
'''


@app.route('/newcycle', methods=['POST', 'GET'])
@admin_required
def add_cycle():
    form = CycleForm()
    
    if request.method == "POST" and form.validate():
        cycle = ReportingCycle (code= form.code.data, 
                            name= form.name.data, 
                            cycle_type= form.cycle_type.data,
                            cycle_value = form.cycle_value.data,
                            week_start = form.week_start.data,
                            organisation = Organisation.query.filter_by(id=session['organisation_id']).first(),
                            is_active= form.is_active.data)
        try:
            db.session.add(cycle)
            db.session.commit()
        except exc.IntegrityError:
            flash('The cycle ' + form.code.data + ' already defined for the organisation')
            db.session.rollback()
        return redirect(url_for('view_cycles'))
        
    return render_template('calendars/cycleform.html', form=form, action='new')


@app.route('/viewcycles')
@login_required
def view_cycles():
    cycles = ReportingCycle.query.filter_by(organisation_id = session['organisation_id'], is_active=True).all()
    return render_template('calendars/view.html', cycles=cycles)

@app.route('/editcycle/<id>', methods=['GET', 'POST'])
@admin_required
def edit_cycle(id):
    cycle = ReportingCycle.query.filter_by(id= id).first()
    form = CycleForm(obj= cycle)
    
    if request.method == "POST" and form.validate():
        cycle.code = form.code.data
        cycle.is_active = form.is_active.data
        cycle.name = form.name.data
        cycle.cycle_type = form.cycle_type.data
        cycle.cycle_value = form.cycle_value.data
        cycle.week_start= form.week_start.data
        try:
            db.session.add(cycle)
            db.session.flush()
            db.session.commit()
            flash('Reporting cycle has been saved successfully','alert-success')
        except exc.IntegrityError:
            flash('The cycle ' + form.code.data + ' already defined for the organisation')
            db.session.rollback()
        return redirect(url_for('view_cycles'))
    return render_template('calendars/cycleform.html', form = form, cycle=cycle, action='edit')

@app.route('/deletecycle/<id>')
def delete_cycle(id):
    cycle = ReportingCycle.query.filter_by(id= id).first()
    if cycle:
        cycle.is_active = False
        try:
            db.session.add(cycle)
            db.session.commit()
            flash('Reporting cycle has been deleted successfully','alert-success')
        except:
            flash('An unexpected error occurred', 'alert-danger')
    return redirect(url_for('view_organisations'))
    
