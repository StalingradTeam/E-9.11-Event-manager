from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event


@app.route('/')
def index():
    events = Event.query.order_by(Event.start_dt).all()
    return render_template('index.html', title='Events list', events=events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/addevent', methods=['GET', 'POST'])
@login_required
def addevent():
    form = EventForm()
    form.submit.label.text = 'Add'

    if form.validate_on_submit():
        event = Event(title=form.title.data, body=form.body.data,
                start_dt = form.start_dt.data.datetime,
                user_id=int(current_user.get_id()))
        if form.end_dt.data:
            event.end_dt = form.end_dt.data.datetime

        db.session.add(event)
        db.session.commit()
        flash('New Event added!')
        return redirect(url_for('event', event_id=event.id))

    return render_template('event.html', title='Add Event', form=form)


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        flash('Event does not exist', 'error')
        return redirect(url_for('index'))

    form = EventForm(
            title = event.title, body = event.body,
            start_dt = event.start_dt, end_dt = event.end_dt
            )
    form.submit.label.text = 'Change'

    event_owner = False
    if current_user.get_id() and event.user_id == int(current_user.get_id()):
        event_owner = True

    if not event_owner:
        form.disable_form()

    if form.validate_on_submit():
        if not event_owner:
            flash('Permission denied to modify Event id {}'.format(event_id))
            return redirect(url_for('event', event_id=event.id))

        event.title = form.title.data
        event.body = form.body.data
        event.start_dt = form.start_dt.data.datetime

        if form.end_dt.data:
            event.end_dt = form.end_dt.data.datetime
        else:
            event.end_dt = None

        db.session.commit()
        flash('Event id {} updated'.format(event.id))
        return redirect(url_for('event', event_id=event.id))

    return render_template('event.html', title='Modify Event', form=form, eid=(event.id if event_owner else None))


@app.route('/delevent/<int:event_id>', methods=['GET', 'POST'])
def delevent(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        flash('Event does not exist', 'error')
        return redirect(url_for('index'))

    form = EventForm(
            title = event.title, body = event.body,
            start_dt = event.start_dt, end_dt = event.end_dt
            )
    form.submit.label.text = 'Delete'
    form.disable_form(skip_submit=True)

    event_owner = False
    if current_user.get_id() and event.user_id == int(current_user.get_id()):
        event_owner = True

    if request.method=='POST':
        if not event_owner:
            flash('Permission denied to delete Event id {}'.format(event_id))
            return redirect(url_for('event', event_id=event.id))

        db.session.delete(event)
        db.session.commit()
        flash('Event id {} deleted'.format(event.id))
        return redirect(url_for('index'))

    flash('Delete Event id {}?'.format(event_id))
    return render_template('event.html', title='Delete Event', form=form)