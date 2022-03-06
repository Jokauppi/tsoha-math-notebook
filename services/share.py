from services.db import db
from services import users


def add(page_id, username):

    user_id = users.get_id(username)

    if user_id:
        try:
            sql = "INSERT INTO access (user_id, page_id) VALUES (:user_id, :page_id)"
            db.session.execute(sql, {"user_id": user_id, "page_id": page_id})
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def remove(page_id, username):

    user_id = users.get_id(username)

    if user_id:
        try:
            sql = "DELETE FROM access WHERE user_id=:user_id AND page_id=:page_id"
            db.session.execute(sql, {"user_id": user_id, "page_id": page_id})
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def get_shared_to(page_id):
    try:
        sql = """SELECT username
        FROM users
        INNER JOIN access ON id = user_id
        WHERE page_id=:page_id"""
        result = db.session.execute(sql, {"page_id": page_id})
        users = list(map(lambda u: u[0], result.fetchall()))
        return users
    except:
        return []


def is_own_notebook(notebook_id, user_id):
    notebook = None
    try:
        sql = """SELECT id FROM notebooks WHERE user_id=:user AND id=:notebook_id"""
        result = db.session.execute(
            sql, {"user": user_id, "notebook_id": notebook_id})
        notebook = result.fetchone()
    except:
        return False
    if notebook == None:
        return False
    else:
        return True


def is_own_page(page_id, user_id):
    page = None
    try:
        sql = """SELECT pages.id FROM pages INNER JOIN notebooks ON notebooks.id = notebook_id WHERE user_id=:user AND pages.id=:page_id"""
        result = db.session.execute(sql, {"user": user_id, "page_id": page_id})
        page = result.fetchone()
    except:
        return False
    if page == None:
        return False
    else:
        return True
