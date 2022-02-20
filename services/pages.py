from services.db import db
from services import notebooks

def create(title, notebook_id, user_id):

    notebook = notebooks.get(notebook_id, user_id)

    if notebook:
        try:
            sql = """INSERT INTO pages (title, notebook_id) VALUES (:title, :notebook_id)"""
            db.session.execute(sql, {"title":title, "notebook_id":notebook.id})
            db.session.commit()
        except:
            return False
        return True

    return False

def get_all(notebook_id, user_id):
    try:
        sql = """SELECT pages.id, pages.title FROM pages INNER JOIN notebooks ON notebook_id = notebooks.id WHERE user_id=:user AND notebook_id=:notebook_id"""
        result = db.session.execute(sql, {"user":user_id, "notebook_id":notebook_id})
        notebooks = result.fetchall()
    except:
        return []
    return notebooks
