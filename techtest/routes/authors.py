from flask import jsonify, flash, redirect, url_for, request, render_template

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author

# Settings
app.secret_key = 'really-secret-key'


# Shows a JSON with all the Authors data
@app.route('/authors', methods=['GET'])
@db_session_wrap
def get_authors(session):
    query = session.query(
        Author
    ).order_by(
        Author.id
    )

    return jsonify([author.asdict() for author in query.all()])


# Add a new Author getting the data from a form
@app.route('/add_author', methods=['POST'])
@db_session_wrap
def add_author(session):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        if not firstname or not lastname:
            flash("Can not create a empty Author")
            return redirect(url_for('show_authors_table'))
        author = Author(first_name=firstname, last_name=lastname)
        session.add(author)
        session.commit()
        flash('New author :' + author.first_name + " " + author.last_name)
        return redirect(url_for('show_authors_table'))


# This method load the edit-author-page with the data of the Author
# Gets the id of the Author
@app.route('/edit_author/<author_id>', methods=['GET', 'POST'])
@db_session_wrap
def edit_author(session, author_id):
    query = session.query
    author_to_edit = query(Author).filter_by(id=author_id).one()
    return render_template('edit-author-page.html', author=author_to_edit)


# Modify the Author's data who has been changed on edit-author.page and redirects to the main page
@app.route('/update_author/<author_id>', methods=['POST'])
@db_session_wrap
def update_author(session, author_id):
    query = session.query
    author_to_edit = query(Author).filter_by(id=author_id).one()
    author_to_edit.first_name = request.form['firstname']
    author_to_edit.last_name = request.form['lastname']
    session.add(author_to_edit)
    session.commit()
    flash('Author edited correctly!')
    return redirect(url_for('show_authors_table'))
