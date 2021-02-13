from datetime import datetime

from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    current_app,
)

from db_manager import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    create_article,
    get_articles,
    get_article,
    update_article,
    delete_article,
)
from logger import logger

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/users")
def users():
    users = get_users()
    return render_template("user_list.html", context=users)


@app.route("/user_create", methods=["POST", "GET"])
def user_create():
    if request.method == "POST":
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        if password != password_confirm or password == "":
            return redirect(url_for(".users"))

        name = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_user(name, email, password, now)
        return redirect(url_for(".users"))
    return render_template("user_create.html")


@app.route("/update_user/<id>", methods=["POST", "GET"])
def user_update(id):
    user = get_user(id)
    if request.method == "POST":
        name = request.form.get("username", "")
        if name == "":
            return render_template("user_update.html", context=user)
        update_user(id, name)
        return redirect(url_for(".users"))
    return render_template("user_update.html", context=user)


@app.route("/delete_user/<id>", methods=["POST"])
def user_delete(id):
    if request.method != "POST":
        redirect(url_for(".users"))
    delete_user(id)
    return redirect(url_for(".users"))


@app.route("/articles")
def articles():
    context = get_articles()
    return render_template("article_list.html", context=context)


@app.route("/article_create", methods=["GET", "POST"])
def article_create():
    if request.method == "POST":
        pass
    return render_template("article_create.html")


if __name__ == "__main__":
    app.debug = True
    app.run()