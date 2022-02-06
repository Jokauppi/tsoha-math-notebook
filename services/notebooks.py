from services.db import db

def create(title, user):
    try:
        sql = """INSERT INTO notebooks (title, user_id) VALUES (:title, :user)"""
        db.session.execute(sql, {"title":title, "user":user})
        db.session.commit()
    except:
        return False
    return True

def get_all(user):
    try:
        sql = """SELECT id, title FROM notebooks WHERE user_id=:user"""
        result = db.session.execute(sql, {"user":user})
        notebooks = result.fetchAll()
    except:
        return []
    return notebooks