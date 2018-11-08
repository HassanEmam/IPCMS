from flask import Flask, render_template, request, flash, redirect, url_for
from base.contact.form import ContactForm
from IPCMS import app
from flask_mail import Mail, Message

mail = Mail()



mail.init_app(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
          flash('All fields are required.', 'alert-danger')
          return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@example.com', recipients=['eng.hassanemam@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            flash('Message has been sent successfully ', 'alert-success')
            return redirect(url_for('contact'))

    elif request.method == 'GET':
        return render_template('contact/contact.html', form=form)