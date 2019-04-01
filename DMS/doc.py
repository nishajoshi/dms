import functools
import io

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    send_file
)
from werkzeug.security import check_password_hash, generate_password_hash

from DMS import db

from sqlalchemy import ForeignKey, LargeBinary

bp = Blueprint('doc', __name__, url_prefix='/doc')



class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    

@bp.route('/files', methods=('GET',))
def files():
    documents = Document.query.filter_by(user_id=session['user_id']).all()
    return render_template('doc/file_operations.html', documents=documents)



@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == "POST":
        file = request.files['fileupload']
        document = Document()
        document.name = file.filename
        document.file = file.stream.read()
        document.user_id = session['user_id']
        db.session.add(document)
        db.session.commit()
        return redirect(url_for("doc.files"))

    return render_template('doc/file_operations.html')



@bp.route('/download/<int:id>', methods=('GET',))
def download(id):
    #import pdb;pdb.set_trace();
    document = Document.query.get(id) 
    return send_file(
        io.BytesIO(document.file),
        as_attachment=True,
        attachment_filename=document.name,
        mimetype="application/pdf"
    )



@bp.route('/delete/<int:id>', methods=('POST',))
def delete(id):
   # import pdb;pdb.set_trace();
    document = Document.query.get(id)
    db.session.delete(document)
    db.session.commit()
    return 'deleted'


