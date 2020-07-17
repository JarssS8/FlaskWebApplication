from flask import abort, jsonify, request, \
    render_template, flash, redirect, url_for

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.article import Article
from techtest.models.region import Region
from techtest.models.author import Author


@db_session_wrap
def add_regions_to_article(article, region_ids, session):
    region_query = session.query(
        Region,
    ).filter(
        Region.id.in_(region_ids),
    )
    regions = region_query.all()
    if len(region_ids) != len(regions):
        raise Exception('One or more regions don\'t exist')

    article.regions = regions


# This method is used for add an Author to an Article using the Author's id and the Article Object
@db_session_wrap
def add_author_to_article(article, author_id, session):
    author_query = session.query(
        Author,
    ).filter(
        Author.id.in_(author_id),
    )
    author = author_query.one()

    if not author:
        raise Exception('The Author don\'t exist')
    article.author = author


# Method used for test add author to an article works well
@app.route('/articles/<id_article>/<id_author>', methods=['PUT'])
@db_session_wrap
def modify_article_author(session, id_article, id_author):
    article = session.query(Article).filter_by(id=id_article).one()
    add_author_to_article(article, id_author, session=session)


@app.route('/articles', methods=['GET'])
@db_session_wrap
def get_articles(session):
    query = session.query(
        Article
    ).order_by(
        Article.id
    )
    return jsonify([
        article.asdict(follow=['regions', 'author']) for article in query.all()
    ])


@app.route('/add_article', methods=['POST'])
@db_session_wrap
def add_article(session):
    request_data = request.get_json()
    article = Article.fromdict(Article(), request_data)
    session.add(article)
    session.flush()
    if 'regions' in request_data:
        add_regions_to_article(
            article, [x['id'] for x in request_data['regions']],
            session=session,
        )
    if 'author' in request_data:
        add_author_to_article(
            article, [x['id'] for x in request_data['author']],
            session=session,
        )

    return jsonify(article.asdict(follow=['regions', 'author']))


@app.route('/articles/<int:article_id>', methods=['GET'])
@db_session_wrap
def get_article_route(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    return jsonify(articles[0].asdict(follow=['regions', 'author']))


# Redirect to the edit-article-page with all the data needed for shows the Article
@app.route('/edit_article/<article_id>', methods=['GET', 'POST'])
@db_session_wrap
def edit_article(session, article_id):
    # Get article to edit
    query = session.query
    article_to_edit = query(Article).filter_by(id=article_id).one()
    # Get Authors Data
    query_author = query(
        Author
    ).order_by(
        Author.id
    )
    authors_data = query_author.all()
    if not authors_data:
        abort(404)
    # Get Regions Data
    query_regions = query(
        Region
    ).order_by(
        Region.id
    )
    regions_data = query_regions.all()
    if not regions_data:
        abort(404)
    return render_template('edit-article-page.html',
                           article=article_to_edit,
                           authors=authors_data,
                           regions=regions_data)


# Modify the data from an existing Article
@app.route('/update_article/<int:article_id>', methods=['GET', 'POST'])
@db_session_wrap
def update_article(article_id, session):
    query = session.query
    article_to_edit = query(Article).filter_by(id=article_id).one()
    article_to_edit.title = request.form['title-article']
    article_to_edit.content = request.form['content-article']
    author_id = request.form.get('authors-select')
    article_to_edit.author = get_author_by_id(query,author_id)
    regions = []
    for region_id in request.form.getlist('regions-checkbox'):
        regions.append(query(Region).filter_by(id=region_id).one())
    article_to_edit.regions = regions
    session.add(article_to_edit)
    session.commit()
    flash('Article edited correctly!')
    return redirect(url_for('show_authors_table'))


# Creates a new Article getting the data from a form
@app.route('/create_article', methods=['GET', 'POST'])
@db_session_wrap
def create_article(session):
    query = session.query
    article_to_edit = Article()
    title = request.form['title-article']
    content = request.form['content-article']
    author_id = request.form.get('authors-select')
    if not title or not content or not author_id:
        flash('Can not create a article without title, content or author')
        return redirect(url_for('show_authors_table'))
    article_to_edit.title = title
    article_to_edit.content = content
    article_to_edit.author = get_author_by_id(query, author_id)
    regions = []
    for region_id in request.form.getlist('regions-checkbox'):
        regions.append(query(Region).filter_by(id=region_id).one())
    article_to_edit.regions = regions
    session.add(article_to_edit)
    session.commit()
    flash('Article created correctly!')
    return redirect(url_for('show_authors_table'))


@app.route('/articles/<int:article_id>', methods=['PUT'])
@db_session_wrap
def update_articles(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    article = articles[0]

    request_data = request.get_json()
    article.fromdict(request_data)
    if 'regions' in request_data:
        add_regions_to_article(
            article,
            [x['id'] for x in request_data['regions']],
            session=session
        )

    if 'author' in request_data:
        add_author_to_article(
            article, [x['id'] for x in request_data['author']],
            session=session,
        )

    return jsonify(article.asdict(follow=['regions', 'author']))


@app.route('/articles/<int:article_id>', methods=['DELETE'])
@db_session_wrap
def delete_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    article = articles[0]
    session.delete(article)
    return jsonify(article.asdict(follow=['regions', 'author']))


# Returns an Author from an Author's id
def get_author_by_id(query, author_id):
    return query(Author).filter_by(id=author_id).one()
