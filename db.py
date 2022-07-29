import pandas as pd
import sqlalchemy as db


def create_database():
    """Creates database"""
    engine = db.create_engine("sqlite:///saved.db")
    return engine

def create_tables(saved_tiles):
    """Creates tables for each type of tile"""
    
    engine = create_database()
    # Create a table for each saved tile
    for type in saved_tiles:
        if saved_tiles[type] != []:
            content = saved_tiles[type]
            df = pd.DataFrame(content)
            df.to_sql(type, con=engine, if_exists='replace', index=False)

def get_table(type):
    """ Fetches required table from the db """
    engine = create_database()
    return engine.execute(f"SELECT * FROM {type};").fetchall()

# engine = create_database()
# create_tables({'book': [{'name': 'Teaching Developmentally Disabled Children', 'author': 'Ole Ivar Lovaas', 'link': 'http://books.google.com/books?id=qcW_QgAACAAJ&dq=me&hl=&cd=1&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=qcW_QgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'}], 'music': None, 'movie': None, 'anime': None, 'food': None})
# print(get_table("books"))
