import json
from app import app
from flask import redirect, render_template, request, session, jsonify
from services import users
from services import notebooks
from services import pages
from services import equations

@app.route("/")
def index():
    notebook_list = notebooks.get_all(users.user_id())
    return render_template("index.html", title="Notebooks", notebooks=notebook_list)

@app.route("/new/notebook",methods=["GET", "POST"])
def new_notebook():
    if request.method == "GET":
        
        return render_template("createnotebook.html", title="Create Notebook")
    
    if request.method == "POST":
    
        users.check_csrf()

        if not notebooks.create(request.form["title"], users.user_id()):
            return render_template("error.html", redirect="/", message="Notebook creation failed")

        return redirect("/")

@app.route("/notebook/<notebook_id>/new_page/",methods=["GET", "POST"])
def new_page(notebook_id):
    if request.method == "GET":
        
        notebook = notebooks.get(notebook_id, users.user_id())

        if notebook is None:
            return redirect("/")

        return render_template("createpage.html", notebook=notebook, title="Create Page")
    
    if request.method == "POST":
    
        users.check_csrf()

        if not pages.create(request.form["title"], notebook_id, users.user_id()):
            return render_template("error.html", redirect="/", message="Page creation failed")

        return redirect(f"/notebook/{notebook_id}")

@app.route("/notebook/<notebook_id>",methods=["GET", "DELETE"])
def notebook(notebook_id):

    if request.method == "GET":
        notebook = notebooks.get(notebook_id, users.user_id())

        if notebook is None:
            return redirect("/")

        page_list = pages.get_all(notebook_id, users.user_id())

        if page_list is None:
            return redirect("/")

        return render_template("notebook.html", notebook=notebook, pages=page_list, title=notebook[1])

    if request.method == "DELETE":

        if not notebooks.delete(notebook_id, users.user_id()):
            return render_template("error.html", redirect="/", message="Notebook deletion failed")

        return redirect("/", code=303)

@app.route("/notebook/<notebook_id>/<page_id>",methods=["GET", "DELETE"])
def page(notebook_id, page_id):

    if request.method == "GET":
        page = pages.get(page_id, users.user_id())

        if page is None:
            return redirect("/")

        equation_list = equations.get_all(page_id, users.user_id())

        if equation_list is None:
            return redirect("/")

        return render_template("page.html", notebook_id=notebook_id, page=page, equations=equation_list, title=page.title, eq_toggle=True)

    if request.method == "DELETE":

        if not pages.delete(page_id, users.user_id()):
            return render_template("error.html", redirect="/", message="Page deletion failed")

        return redirect("/", code=303)

@app.route("/notebook/<notebook_id>/<page_id>/<eq_id>",methods=["POST", "PUT", "DELETE"])
def equation(notebook_id, page_id, eq_id):

    if request.method == "POST":
        data = json.loads(request.data)

        equation = equations.create(data["content"], page_id, eq_id, data["type"], users.user_id())

        if not equation:
            return jsonify({"success": False}), 400

        response_json = equation._asdict()
        response_json["after"] = eq_id
        return jsonify(response_json)

    if request.method == "PUT":

        data = json.loads(request.data)

        if not equations.change(data["content"], eq_id, data["type"], users.user_id()):
            return jsonify(success=False)

        return jsonify(success=True)

    if request.method == "DELETE":

        if not equations.delete(eq_id, users.user_id()):
            return render_template("error.html", redirect="/", message="Equation deletion failed")

        return jsonify(success=True)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    if users.login(username, password):
        session["username"] = username
        return redirect("/")

    return render_template("error.html", redirect="/", message="Invalid login")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", redirect="/register", message="Username too short or long")

        password = request.form["password1"]
        password_again = request.form["password2"]

        if len(password) < 4:
            return render_template("error.html", redirect="/register", message="Password too short")

        if password != password_again:
            return render_template("error.html", redirect="/register", message="Passwords dont match")

        if not users.register(username, password):
            return render_template("error.html", redirect="/register", message="Registration failed")

        return redirect("/")