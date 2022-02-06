from app import app
from flask import redirect, render_template, request, session
from services import users
from services import notebooks

@app.route("/")
def index():
    return render_template("index.html", title="Notebooks", notebooks=[(1, "palceholder")])

@app.route("/new/notebook",methods=["GET", "POST"])
def new_notebook():
    if request.method == "GET":
        
        return render_template("createnotebook.html", title="Notebooks")
    
    if request.method == "POST":
    
        users.check_csrf()

        if not notebooks.create(request.form["title"], users.user_id()):
            return render_template("error.html", redirect="/", message="Notebook creation failed")

        return redirect("/")

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