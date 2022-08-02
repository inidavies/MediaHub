import pandas as pd
import sqlalchemy as db


def create_database(user_id):
    """Creates database"""
    engine = db.create_engine(f"sqlite:///{user_id}.db")
    return engine

def create_tables(user_id, saved_tiles):
    """Creates tables for each type of tile"""
    
    engine = create_database(user_id)
    # Create a table for each saved tile
    try:
        for type in saved_tiles:
            if saved_tiles[type] != []:
                content = saved_tiles[type]
                df = pd.DataFrame(content)
                df.to_sql(type, con=engine, if_exists='replace', index=True)
    except:
        return -1

def get_table(user_id, type):
    """ Fetches required table from the db """
    engine = create_database(user_id)
    try:
        #print(table_data)
        return engine.execute(f"SELECT * FROM {type};").fetchall()
    except:
        return ()

def reset_table(user_id, type):
    """ Deletes the table content """
    engine = create_database(user_id)
    try:
        engine.execute("DELETE FROM {type};")
    except:
        return ()



'''def delete_row(user_id, type, index):
    """ Fetches required table from the db """
    engine = create_database(user_id)

    #engine.execute(f"SHOW COLUMNS FROM {type};")
    engine.execute(f"DROP INDEX {type}.{index};")
    table_data = engine.execute(f"SELECT * FROM {type};").fetchall()
    return table_data


engine = create_database("test")
create_tables("test", {'book': [{'name': 'Teaching Developmentally Disabled Children', 'author': 'Ole Ivar Lovaas', 'link': 'http://books.google.com/books?id=qcW_QgAACAAJ&dq=me&hl=&cd=1&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=qcW_QgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 'search':"IDK"}, {'name': 'Test Addition', 'author': 'Jon Doe', 'link': 'http://books.google.com/books?id=qcW_QgAACAAJ&dq=me&hl=&cd=1&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=qcW_QgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 'search':"IDK"}], 'music': None, 'movie': None, 'anime': None, 'food': None})
print(get_table("test", "book"))
print(delete_row("test", "book", 0))'''
