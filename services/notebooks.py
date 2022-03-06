from services.db import db


def create(title, user):
    try:
        sql = """INSERT INTO notebooks (title, user_id) VALUES (:title, :user)"""
        db.session.execute(sql, {"title": title, "user": user})
        db.session.commit()
    except:
        return False
    return True


def get_all(user):
    try:
        sql = """SELECT id, title FROM notebooks WHERE user_id=:user"""
        result = db.session.execute(sql, {"user": user})
        notebooks = result.fetchall()
    except:
        return []
    return notebooks


def get_shared(user):
    try:
        sql = """SELECT DISTINCT notebooks.id, notebooks.title
        FROM notebooks
        INNER JOIN pages ON notebook_id = notebooks.id
        INNER JOIN access ON page_id = pages.id
        WHERE access.user_id=:user"""
        result = db.session.execute(sql, {"user": user})
        notebooks = result.fetchall()
    except:
        return []
    return notebooks


def get(notebook_id, user):
    
    try:
        sql = """SELECT notebooks.id, notebooks.title
        FROM notebooks
        LEFT JOIN pages ON notebook_id = notebooks.id
        LEFT JOIN access ON page_id = pages.id
        WHERE (notebooks.user_id = :user OR access.user_id = :user) AND notebooks.id=:notebook_id"""
        result = db.session.execute(
            sql, {"user": user, "notebook_id": notebook_id})
        notebook = result.fetchone()
        return notebook
    except Exception as err:
        print(err)
        return ()


def delete(notebook_id, user):
    try:
        sql = """DELETE FROM notebooks WHERE user_id=:user AND id=:notebook_id"""
        db.session.execute(sql, {"user": user, "notebook_id": notebook_id})
        db.session.commit()
    except:
        return False
    return True
