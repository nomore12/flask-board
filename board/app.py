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
    login_user,
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


@app.route("/", methods=["POST", "GET"])
def index():
    logger.debug("post")
    articles = get_articles()
    if request.method != "POST":
        return render_template(
            "base.html",
            context={"user": None, "articles": articles},
        )
    email = request.form.get("email")
    password = request.form.get("password")
    user = login_user(email, password)

    if user is False:
        return render_template(
            "base.html", context={"user": user, "articles": articles}
        )
    logger.debug("auth")
    if email != user["email"] or password != user["password"]:
        return render_template(
            "base.html",
            context={"user": None, "articles": articles},
        )
    session["user"] = user
    return render_template(
        "base.html",
        context={
            "user": user,
            "articles": articles,
        },
    )


@app.route("/logout")
def logout():
    user = session.get("user", None)
    if user is None:
        return redirect(url_for(".index"))
    session.pop("user")
    return redirect(url_for(".index"))


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
    app.config.update(DEBUG=True, SECRET_KEY="secretkey")
    app.run()