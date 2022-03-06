from services.db import db
from services import users

def add(page_id, username):
    
    user_id = users.get_id(username)

    if user_id:
      try:
          sql = "INSERT INTO access (user_id, page_id) VALUES (:user_id, :page_id)"
          db.session.execute(sql, {"user_id":user_id, "page_id":page_id})
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
          db.session.execute(sql, {"user_id":user_id, "page_id":page_id})
          db.session.commit()
          return True
      except:
          return False
    else:
      return False

def is_own_notebook(notebook_id, user_id):
  pass

def is_own_page(notebook_id, user_id):
  pass