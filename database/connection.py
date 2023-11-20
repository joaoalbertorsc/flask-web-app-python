def conectionDB(app):
    app.config['MYSQL_HOST'] = 'yourHost'
    app.config['MYSQL_USER'] = 'yourUser'
    app.config['MYSQL_PASSWORD'] = 'yourPassWord'
    app.config['MYSQL_DB'] = 'nameOfYourDB'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'