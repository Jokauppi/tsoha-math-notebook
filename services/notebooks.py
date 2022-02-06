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
        print(1)
        sql = """SELECT id, title FROM notebooks WHERE user_id=:user"""
        print(2)
        result = db.session.execute(sql, {"user":user})
        print(3)
        notebooks = result.fetchall()
        print(4)
    except:
        return []
    return notebooks