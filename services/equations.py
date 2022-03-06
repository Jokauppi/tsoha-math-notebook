from services.db import db

def create(content, page_id, after_id, type):

    if type != "t" and "m":
      return False

    print(content, page_id, after_id, type)

    try:
        sql = """INSERT INTO equations (content, page_id, order_num, type) VALUES (:content, :page, :order, :type)"""
        db.session.execute(sql, {"content":content, "page":page_id, "order": after_id + 1, "type": type})
        db.session.commit()
    except:
        return False
    return True

def get_all(page_id, user_id):
    try:
        sql = """SELECT equations.id, content
          FROM equations
          INNER JOIN pages ON page_id = pages.id
          INNER JOIN notebooks ON notebook_id = notebooks.id
          WHERE user_id=:user AND pages.id=:page
          ORDER BY order_num"""
        result = db.session.execute(sql, {"user":user_id, "page":page_id})
        notebooks = result.fetchall()
    except:
        return None
    return notebooks

def change(content, eq_id, type, user_id):

    try:
        sql = """UPDATE equations e
        SET content=:content, type=:type
        FROM (SELECT pages.id, user_id FROM pages INNER JOIN notebooks ON notebook_id = notebooks.id) p
        WHERE e.id = :eq AND page_id = p.id AND p.user_id = :user"""
        db.session.execute(sql, {"content":content, "type":type, "eq":eq_id, "user":user_id})
        db.session.commit()
    except:
        return False
    
    return True
