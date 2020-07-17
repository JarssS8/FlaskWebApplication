from flask import abort,render_template
from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author
from techtest.models.region import Region
from techtest.models.article import Article


# This method is going to get and show all the authors data from the
# database in a HTML file with controllers for add, edit
# or remove an Author.
@app.route('/', methods=['GET'])
@db_session_wrap
def show_authors_table(session):
    # Get Authors Data
    query_author = session.query(
        Author
    ).order_by(
        Author.id
    )
    authors_data = query_author.all()
    if not authors_data:
        abort(404)

    # Get Regions Data
    query_regions = session.query(
        Region
    ).order_by(
        Region.name
    )
    regions_data = query_regions.all()
    if not regions_data:
        abort(404)
    # Get Articles Data
    query_articles = session.query(
        Article
    ).order_by(
        Article.id
    )
    articles_data = query_articles.all()
    if not authors_data:
        abort(404)
    return render_template('index.html', authors=authors_data, regions=regions_data, articles=articles_data)


