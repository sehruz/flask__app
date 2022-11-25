import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext



"""
g is special opject that we can store data during request, it is uniqe for every request
we create db connection and store it inside g
sqlite3.Row is used because it returns not simple tuple, it returns dict that we can access any row with column name
"""
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

"""
if request end , it is important to close connection
we check if db in g, otherwise pop will return None 
"""
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# for creating CLI inorder install DATABSE File
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# for creating CLI inorder install DATABSE File
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# we need to register with app inorder to use CLI and close connection after response
def init_app(app):
    # will call it after returning response 
    app.teardown_appcontext(close_db)
    # will call with flask command
    app.cli.add_command(init_db_command)