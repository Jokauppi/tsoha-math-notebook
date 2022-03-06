from services.db import db
from services import notebooks
from services import equations

def create(title, notebook_id, user_id):

    notebook = notebooks.get(notebook_id, user_id)

    page = None

    if notebook:
        try:
            sql = """INSERT INTO pages (title, notebook_id) VALUES (:title, :notebook_id) RETURNING id"""
            result = db.session.execute(sql, {"title":title, "notebook_id":notebook.id})
            db.session.commit()
            page = result.fetchone()
        except:
            return False
        
        if not equations.create("\\text{LaTeX}", page.id, 0, "t"):
            try:
                delete(page.id, user_id)
            except:
                pass
            return False

        return True

    return False

def get(page_id, user_id):
    try:
        sql = """SELECT pages.id, pages.title FROM pages INNER JOIN notebooks ON notebook_id = notebooks.id WHERE user_id=:user AND pages.id=:page_id"""
        result = db.session.execute(sql, {"user":user_id, "page_id":page_id})
        page = result.fetchone()
    except:
        return None
    return page

def get_all(notebook_id, user_id):
    try:
        sql = """SELECT pages.id, pages.title FROM pages INNER JOIN notebooks ON notebook_id = notebooks.id WHERE user_id=:user AND notebook_id=:notebook_id"""
        result = db.session.execute(sql, {"user":user_id, "notebook_id":notebook_id})
        notebooks = result.fetchall()
    except:
        return None
    return notebooks

def delete(page_id, user_id):
    if get(page_id, user_id) != None:
        try:
            sql = """DELETE FROM pages WHERE id=:page_id"""
            db.session.execute(sql, {"page_id":page_id})
            db.session.commit()
        except:
            return False
        return True
    return False