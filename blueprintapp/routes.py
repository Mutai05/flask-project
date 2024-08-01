from flask import render_template, redirect, url_for, request, session, make_response, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from models import Person
from models import User

def register_routes(app, db, bcrypt):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about_us.html')

    @app.route('/who-we-are')
    def redirect_endpoint():
        return redirect(url_for('about'))
    
    @app.route('/admin')
    def admin():
        return render_template('admin.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username=username, password=hashed_password)

            db.session.add(user)
            db.session.commit()
            return 'Registration Successful'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username). first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('admin'))
            else:
                return 'Login Failed'

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/restricted')
    @login_required
    def restricted():
        return 'Content Restricted!'

    @app.route('/file-upload', methods=['GET', 'POST'])
    def file_upload():
        if request.method == 'POST':
            if 'file' not in request.files:
                return 'No file part in the request', 400
            file = request.files['file']
            if file.filename == '':
                return 'No file selected for uploading', 400
            if file.content_type == 'text/plain':
                return file.read().decode()
        return render_template('file_upload.html')

    @app.route('/set_data')
    def set_data():
        session['name'] = 'Kelvin'
        session['other'] = 'Hello Kelvin, Flask Dev'
        return render_template('index.html', message='Session data set.')

    @app.route('/get_data')
    def get_data():
        if 'name' in session.keys() and 'other' in session.keys():
            name = session['name']
            other = session['other']
            return render_template('index.html', message=f'Name: {name}, Other: {other}')
        else:
            return render_template('index.html', message='No session found.')
        

    @app.route('/clear_session')
    def clear_session():
        session.clear()
        return render_template('index.html', message='Session cleared.')

    @app.route('/set_cookie')
    def set_cookie():
        response = make_response(render_template('index.html', message='Cookie Set.'))
        response.set_cookie('cookie_name', 'cookie_value')
        return response

    @app.route('/get_cookie')
    def get_cookie():
        cookie_value = request.cookies['cookie_name']
        return render_template('index.html', message=f'Cookie Value: {cookie_value}')

    @app.route('/remove_cookie')
    def remove_cookie():
        response = make_response(render_template('index.html', message='Cookie Removed.'))
        response.set_cookie('cookie_name', expires=0)
        return response

    @app.route('/leads', methods=['GET', 'POST'])
    def leads():
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('leads.html', people=people)
        elif request.method == 'POST':
            name = request.form.get('name')
            age = int(request.form.get('age'))
            job = request.form.get('job')

            person = Person(name=name, age=age, job=job)

            db.session.add(person)
            db.session.commit()

            people = people = Person.query.all()
            return render_template('leads.html', people=people)
        
        
    @app.route('/delete/<pid>', methods=['DELETE'])
    def delete(pid):
        person = Person.query.get(pid)
        if person:
            db.session.delete(person)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Person deleted successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Person not found'}), 404
        
    @app.route('/details/<pid>')
    def details(pid):
        person = Person.query.filter(Person.pid == pid).first()
        return render_template('lead-detail.html', person=person)