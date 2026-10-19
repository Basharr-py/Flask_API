from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort
from config import Config
from flask_migrate import Migrate
from flask_moment import Moment
from form import LoginForm, RegistrationForm, CourseForm, AddMaterial, EditProfileForm
from models import db, User, sa, so, Post, login, Files, datetime, timezone, Materials
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlsplit
import os

import uuid
import boto3


from botocore.exceptions import BotoCoreError, ClientError
from werkzeug.utils import secure_filename

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

S3_BUCKET = os.environ["S3_MATERIALS_BUCKET"]

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
moment = Moment(app)
login.init_app(app)
login.login_view = 'login'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

MAX_PDF_SIZE = 20 * 1024 * 1024


def validate_pdf(file):
    filename = secure_filename(file.filename or "")

    if not filename or not filename.lower().endswith(".pdf"):
        return False, "Only PDF files are allowed."

    # Check the file's actual size
    file.stream.seek(0, 2)
    file_size = file.stream.tell()
    file.stream.seek(0)

    if file_size == 0:
        return False, "The PDF file is empty."

    if file_size > MAX_PDF_SIZE:
        return False, "PDF files must not exceed 10 MB."

    # Check the PDF file signature
    signature = file.stream.read(5)
    file.stream.seek(0)

    if signature != b"%PDF-":
        return False, "Invalid PDF file."

    return True, filename

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

from werkzeug.exceptions import RequestEntityTooLarge

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(error):
    flash("File is too large. Maximum upload size is 10 MB.", "error")
    return redirect(url_for("new_dash")), 303


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('registered', None)
    form=LoginForm()
    if form.validate_on_submit():
        print('Logging in user...')
        u = form.username.data
        passw = form.password.data
        query = sa.select(User).where(User.username==u)
        user = db.session.scalar(query)
        if user is None or not user.check_password(passw):
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('new_dash'))
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('new_dash')
        return redirect(next_page)
    return render_template('/extra_log.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('Registering user...')
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, created_at=datetime.now(timezone.utc))
        user.set_password(form.password.data)
        user.avatar_url_generator()
        db.session.add(user)
        db.session.commit()
        print('User registered successfully, username is ', form.username.data)
        flash('Congratulations, you are now a registered user!')
        session['registered'] = True
        return redirect(url_for('reg_success'))
    return render_template('register2.html', form=form)

@app.route('/regSucc')
def reg_success():
    print(session)
    
        
    if not session.get('registered'):
        return redirect(url_for('register'))
    return render_template('reg_succ.html')


    
@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm()
    print('Testing edit profile...')
    if request.method=='POST':
        print('Testing request...')
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.name = form.name.data
        db.session.commit()
        print('Your profile has been updated.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        form.location.data = "" 
        form.name.data = current_user.name
        
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    return render_template('my_profile.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_route():
    form = CourseForm()
    if form.validate_on_submit():
        print('Done')
        

        doc = Files(
            course_code = form.course_code.data,
            status = form.status.data,
            credit_unit = form.credit_unit.data

        )
        db.session.add(doc)
        db.session.commit()
        flash('uploaded succesfully')
        print('uploaded succesfully')
        docs = Files.query.all()
        return redirect(url_for('new_dash'))
    return render_template('upload.html', form=form, docs=docs)

@app.route('/addmaterial', methods=['GET', 'POST'])
@login_required
def addmaterial():
    
    form = AddMaterial()

    if form.validate_on_submit():
        file = form.material.data

        valid, result = validate_pdf(file)

        if not valid:
            flash(result, "error")
            return redirect(url_for("new_dash"))

        filename = result
        course_id = form.courseID.data

        object_key = (
            f"materials/{course_id}/"
            f"{uuid.uuid4().hex}-{filename}"
        )

        try:
            s3.upload_fileobj(
                file.stream,
                S3_BUCKET,
                object_key,
                ExtraArgs={
                    "ContentType": "application/pdf",
                    "ContentDisposition": "inline"
                }
            )

            mats = Materials(
                filename=filename,
                filepath=object_key,
                c_id=course_id
            )

            db.session.add(mats)
            db.session.commit()

        except Exception:
            db.session.rollback()

            # Remove S3 object if the database operation fails.
            try:
                s3.delete_object(
                    Bucket=S3_BUCKET,
                    Key=object_key
                )
            except Exception:
                app.logger.exception("S3 cleanup failed")

            app.logger.exception("Material upload failed")
            flash("Upload failed", "error")
            return redirect(url_for("new_dash"))

        flash("Material uploaded successfully", "success")
        return redirect(url_for("new_dash"))

    return render_template("newdash.html", form=form)

@app.route('/view/<int:material_id>')
@login_required
def view_file(material_id):

    docs = db.session.get(Materials, material_id)

    if docs is None:
        abort(404)

    # Add any course-level viewing authorization here.

    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': docs.filepath,
                'ResponseContentType': 'application/pdf',
                'ResponseContentDisposition': 'inline'
            },
            ExpiresIn=300
        )

    except (ClientError, BotoCoreError):
        app.logger.exception("S3 URL generation failed")
        abort(500)

    return redirect(presigned_url)

@app.route('/newdash')
@login_required
def new_dash():
    form = CourseForm()
    username ='admin'
    docs = Files.query.all()
    files = Files.query.all()
    
    
    return render_template('new_dash.html', username=username, form=form, files=files, docs=docs)


@app.route('/notifications')
@login_required
def notifications():
    return render_template('notification.html')
    
if __name__ == '__main__':
    app.run(debug=True)
