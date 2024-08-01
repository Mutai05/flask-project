# flask-recap

Flask is a lightweight web framework for Python, often chosen for its simplicity and flexibility. Here’s a comprehensive guide from the basics of Flask to deploying a Flask application.

### Basics of Flask

#### 1. Setting Up Flask

First, ensure you have Python installed. You can create a virtual environment to keep your project dependencies isolated:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Next, install Flask:

```bash
pip install Flask
```

#### 2. Creating a Simple Flask Application

Create a new file named `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
```

Run the application:

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your web browser, and you should see "Hello, Flask!".

#### 3. Routing

Routing in Flask is straightforward. You define routes using the `@app.route` decorator.

```python
@app.route('/about')
def about():
    return "This is the about page."

@app.route('/user/<username>')
def show_user_profile(username):
    return f"User: {username}"
```

#### 4. Templates

Flask uses Jinja2 for templating. Create a directory named `templates` and add an `index.html` file:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Home</title>
  </head>
  <body>
    <h1>Hello, {{ name }}!</h1>
  </body>
</html>
```

Modify `app.py` to render this template:

```python
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html', name='Flask')
```

#### 5. Handling Forms

Create a simple form in `templates/form.html`:

```html
<form method="POST" action="/submit">
  <input type="text" name="name" />
  <input type="submit" />
</form>
```

Modify `app.py` to handle the form:

```python
from flask import request

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return f"Hello, {name}!"
```

### Deployment

Deploying a Flask application involves several steps, including configuring a production server and setting up a WSGI server.

#### 1. Preparing for Deployment

It's important to avoid running the built-in Flask server in production. Instead, use a WSGI server like Gunicorn.

First, install Gunicorn:

```bash
pip install gunicorn
```

Test your application with Gunicorn:

```bash
gunicorn -w 4 app:app
```

#### 2. Using a Production Server

One common setup is using Nginx as a reverse proxy in front of Gunicorn.

##### Nginx Configuration

Create an Nginx configuration file, typically located at `/etc/nginx/sites-available/your_project`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site by creating a symlink to `sites-enabled`:

```bash
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled
```

Test the Nginx configuration and restart the service:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

##### Systemd Service

Create a systemd service file for your Flask application, typically located at `/etc/systemd/system/your_project.service`:

```ini
[Unit]
Description=Gunicorn instance to serve your_project
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start your_project
sudo systemctl enable your_project
```

### Summary

- **Setting Up Flask**: Create a virtual environment, install Flask.
- **Creating a Simple Application**: Define routes, render templates, and handle forms.
- **Deploying Flask**: Use Gunicorn as the WSGI server and Nginx as a reverse proxy. Configure systemd for managing the Gunicorn service.

This guide provides a foundation for developing and deploying a Flask application. For more advanced features, you can explore Flask extensions, database integration, and more.
