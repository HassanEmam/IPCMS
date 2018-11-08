from IPCMS import app, db
from flask import render_template
from base.users.models import User
from base.users.decorators import *
from base.messages.form import MessageForm
from base.messages.models import Message
from datetime import datetime

@app.route('/sendmessage/<recipient>')
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    if not user:
        flash('Specified user not found. Please enter a valid username','alert-danger')
        print('redirecting')
        return redirect(url_for('sendmessage'))
    return render_template('messages/send_message.html', title=('Send Message'),
                           form=form, recipient=recipient)

@app.route('/sendmessage', methods=['GET', 'POST'])
@login_required
def sendmessage():

    form = MessageForm()
    if request.method== 'POST':
        current_user = User.query.filter_by(id=session.get('user_id')).first()
        recipient = User.query.filter_by(username= form.to.data).first()
        msg = Message(sender=current_user, recipient=recipient,
                      body=form.message.data)
        print(form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.', 'alert-success')
        return redirect(url_for('login_success'))
    users1 = User.query.filter_by(organisation_id = session.get('organisation_id'), is_active=True).all()
    users=[]
    for user in users1:
        users.append(user.username)

    return render_template('messages/send_message.html', title=('Send Message'),
                           form=form, users=users)


@app.route('/messageinbox')
@login_required
def messages(page=1):
    page = request.args.get('page', 1, type=int)
    current_user = User.query.filter_by(id=session.get('user_id')).first()
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(recipient_id= current_user.id, is_active=True).order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    print(messages.next_num, messages.has_next, messages.has_prev)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('/messages/messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, msg =" Inbox")

@app.route('/readmail/<id>')
@login_required
def readmessage(id):
    current_user = User.query.filter_by(id=session.get('user_id')).first()
    message = Message.query.filter_by(id= id).first()

    return render_template('/messages/readmessage.html', message=message)

@app.route('/deletemessage/<id>')
@login_required
def deletemessage(id):
    message = Message.query.filter_by(id= id).first()
    message.is_active = False
    db.session.commit()
    flash('Message deleted successfully', 'alert-success')
    return redirect(url_for('messages'))

@app.route('/deletemessage')
@login_required
def delmessage():
    id = request.args.get('id')
    return redirect(url_for('deletemessage', id = id))

@app.route('/messagesdelete')
@login_required
def deletedmessages(page=1):
    page = request.args.get('page', 1, type=int)
    current_user = User.query.filter_by(id=session.get('user_id')).first()
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(recipient_id= current_user.id, is_active=False).order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    print(messages.next_num, messages.has_next, messages.has_prev)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('/messages/messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, msg =" Deleted")

@app.route('/messagessent')
@login_required
def sentmessages(page=1):
    page = request.args.get('page', 1, type=int)
    current_user = User.query.filter_by(id=session.get('user_id')).first()
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(sender_id= current_user.id).order_by(
        Message.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    print(messages.next_num, messages.has_next, messages.has_prev)
    next_url = url_for('messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('/messages/messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, msg =" Sent")