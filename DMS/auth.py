import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from DMS import db

bp = Blueprint('auth', __name__, url_prefix='/auth')



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False);
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        mail = request.form['mail']
        passwd = request.form['passwd']
        error = None
        user = User(username=uname, email=mail, password=passwd)
        #result = db.session.query(db.exists().where(User.email == 'davidism')).scalar()
        result = User.query.filter_by(email=mail).first()
        if not uname:
            error = 'Username is required.'
        elif not passwd:
            error = 'Password is required.'
        elif result is not None:
            error = 'User {} is already registered.'.format(uname)

        if error is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        passwd = request.form['passwd']
        error = None
        user = User.query.filter_by(username=uname, password=passwd).first()

        if user is None:
            error = 'Incorrect username.'
        elif check_password_hash(user.password, passwd):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['logged_in'] = True
            return redirect(url_for('doc.files'))

        flash(error)

    return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

