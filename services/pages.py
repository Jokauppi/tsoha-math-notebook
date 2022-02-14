from services.db import db

def get_all(notebook_id, user):
    try:
        sql = """SELECT id, title FROM pages WHERE user_id=:user AND notebook_id=:user"""
        result = db.session.execute(sql, {"user":user})
        notebooks = result.fetchall()
    except:
        return []
    return notebooks
