from services.db import db
from services import notebooks

def create(title, notebook_id, user_id):

    print("2")

    notebook = notebooks.get(notebook_id, user_id)

    print("3")

    print(notebook)

    if notebook:
        print("4")
        try:
            sql = """INSERT INTO pages (title, notebook_id) VALUES (:title, :notebook_id)"""
            db.session.execute(sql, {"title":title, "notebook_id":notebook.id})
            db.session.commit()
        except:
            return False
        return True
    

    return False

def get_all(notebook_id, user):
    try:
        sql = """SELECT id, title FROM pages WHERE user_id=:user AND notebook_id=:notebook_id"""
        result = db.session.execute(sql, {"user":user, "notebook_id":notebook_id})
        notebooks = result.fetchall()
    except:
        return []
    return notebooks
