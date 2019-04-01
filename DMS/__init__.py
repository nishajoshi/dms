import os

from flask import Flask

from flask import (
        render_template, redirect, session, url_for
)

from flask_sqlalchemy import SQLAlchemy



project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"]='dev'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)


from . import auth
app.register_blueprint(auth.bp)
#app.add_url_rule('/', endpoint='login')


from . import doc
app.register_blueprint(doc.bp)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('doc.files'))

    return render_template('auth/index.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
