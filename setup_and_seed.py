from techtest.models.article import Article
from techtest.models.region import Region
from techtest.models.author import Author
from techtest.connector import engine, BaseModel, db_session

BaseModel.metadata.create_all(engine)

with db_session() as session:

    joan = Author(first_name='Joan', last_name='Smith')
    luka = Author(first_name='Luka', last_name='Brazy')
    au = Region(code="AU", name="Australia")
    uk = Region(code="UK", name="United Kingdom")
    us = Region(code="US", name="United States of America")
    session.add_all([
        joan,
        luka,
        au,
        uk,
        us,
        Article(
            title='Post 1',
            content='This is a post body',
            regions=[au, uk],
            author=joan
        ),
        Article(
            title='Post 2',
            content='This is the second post body',
            regions=[au, us],
            author=luka
        ),
    ])
