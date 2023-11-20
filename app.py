from functools import wraps
from model.articleForm import ArticleForm
from model.registerForm import RegisterForm
from database.connection import conectionDB
from database.queries import select_all_articles, select_article_by_id, insert_user_data, select_user_login, insert_new_article, update_article, delete_article_by_id

from flask import Flask,render_template, flash, redirect, request, url_for, session, logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)
# Config MySQL
conectionDB(app)
# init MySQL
mysql = MySQL(app)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Login Required', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    cursor = mysql.connection.cursor()
    query = cursor.execute(select_all_articles)
    articles = cursor.fetchall()
    cursor.close()
    if query > 0:
        return render_template('articles.html', articles = articles)
    else:
        msg = 'No article found.'
        return render_template('articles.html', msg = msg)

@app.route('/article/<string:id>')
def article(id):
    cursor = mysql.connection.cursor()
    cursor.execute(select_article_by_id, [id])
    article = cursor.fetchone()
    return render_template('article.html', article = article)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cursor = mysql.connection.cursor()
        cursor.execute(insert_user_data, [name, email, username, password])
        mysql.connection.commit()
        cursor.close()
        flash('You are now registered and can log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Get Forms Fields
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cursor = mysql.connection.cursor()
        result = cursor.execute(select_user_login, [username])
        if result > 0:
            # Get stored hash
            data = cursor.fetchone()
            password = data['password']
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                cursor.close()
                session['logged_in'] = True
                session['username'] = username
                flash('Login success!', 'success')
                return redirect(url_for('dashboard'))
            else:
                cursor.close()
                error = 'Invalid login'
                return render_template('login.html', error = error)
        else:
            error = 'Username not found'
            return render_template('login.html', error = error)
    return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out!', 'success')
    return render_template('home.html')

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cursor = mysql.connection.cursor()
    query = cursor.execute(select_all_articles)
    articles = cursor.fetchall()
    cursor.close()
    if query > 0:
        return render_template('dashboard.html', articles = articles)
    else:
        msg = 'No article found.'
        return render_template('dashboard.html', msg = msg)

# Add article
@app.route('/add_article', methods = ['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cursor = mysql.connection.cursor()
        cursor.execute(insert_new_article, [title, body, session['username']])
        mysql.connection.commit()
        cursor.close()

        flash('Article Created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

# Edit article
@app.route('/edit_article/<string:id>', methods = ['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cursor = mysql.connection.cursor()
    cursor.execute(select_article_by_id, [id])
    article = cursor.fetchone()
    cursor.close()

    form = ArticleForm(request.form)
    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cursor = mysql.connection.cursor()
        cursor.execute(update_article, [title, body, id])
        mysql.connection.commit()
        cursor.close()

        flash('Article edited with success!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute(delete_article_by_id, [id])
    mysql.connection.commit()
    cur.close()

    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='yourSecretKey'
    app.run(debug=True)