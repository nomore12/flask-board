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
    articles = get_articles()
    user = session.get("user", False)

    if request.method != "POST" and user is False:
        return render_template(
            "base.html",
            context={"user": None, "articles": articles},
        )
    elif request.method != "POST":
        return render_template(
            "base.html",
            context={"user": user, "articles": articles},
        )
    email = request.form.get("email")
    password = request.form.get("password")
    user = login_user(email, password)
    if user is False:
        return render_template(
            "base.html", context={"user": None, "articles": articles}
        )
    if email != user.get("email", "") or password != user.get("password", ""):
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
    logger.debug(
        f"---------------index session: {session.get('user', '없음')}-------------------"
    )
    if user is None:
        return redirect(url_for(".index"))
    session.pop("user")
    logger.debug(
        f"---------------index session: {session.get('user', '없음')}-------------------"
    )
    return redirect(url_for(".index"))


@app.route("/users")
def users():
    users = get_users()
    return render_template("user_list.html", context=users)


@app.route("/user_create", methods=["POST", "GET"])
def user_create():
    user = session.get("user", None)
    context = {"user": user}
    if request.method == "GET":
        return render_template("user_create.html", context=context)
    elif request.method == "POST":
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")
        if password != password_confirm or password == "":
            return redirect(url_for(".users"))
        name = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_user(name, email, password, now)
        return redirect(url_for(".index"))


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
    user = session.get("user", None)
    if request.method == "GET":
        if user is not None:
            return render_template(
                "article_create.html",
                context={
                    "user": user,
                },
            )
        elif user is None:
            return redirect(url_for(".index"))
    elif request.method == "POST":
        title = request.form.get("title", None)
        content = request.form.get("content", None)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_article(user.get("id", ""), title, content, now)
        return redirect(url_for(".index"))


@app.route("/article/<id>")
def article_detail(id):
    article = get_article(id)
    article["content"] = article["content"].replace("\r\n", "<br />")
    user = session.get("user", None)
    context = {"user": user, "article": article}
    return render_template("article_detail.html", context=context)


@app.route("/article/<id>/delete")
def article_delete(id):
    user = session.get("user", None)
    if user is not None:
        delete_article(id)
        return redirect(url_for(".index"))
    else:
        return redirect(url_for(".article_detail", id=id))


@app.route("/article/<id>/update", methods=["POST", "GET"])
def article_update(id):
    user = session.get("user", None)
    logger.debug("update start")
    if user is None:
        logger.debug("no user")
        return redirect(url_for(".article_update", id=id))
    article = get_article(id)
    context = {"user": user, "article": article}
    logger.debug("method choice")
    if request.method == "GET":
        logger.debug("method get")
        return render_template("article_update.html", context=context)
    elif request.method == "POST":
        logger.debug("update post")
        user_id = request.form.get("user_id", None)
        if user["id"] != user_id:
            redirect(url_for("article_detail", id=id))
        title = request.form.get("title", None)
        content = request.form.get("content", None)
        if user_id is not None and title is not None and content is not None:
            update_article(id=id, user_id=user_id, title=title, content=content)
            return redirect(url_for("article_detail", id=id))


if __name__ == "__main__":
    app.config.update(DEBUG=True, SECRET_KEY="secretkey")
    app.run()