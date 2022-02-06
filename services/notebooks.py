from services.db import db

def create(title, user):
    try:
        sql = """INSERT INTO notebooks (title, user_id) VALUES (:title, :user)"""
        db.session.execute(sql, {"title":title, "user":user})
        db.session.commit()
    except:
        return 
    return True