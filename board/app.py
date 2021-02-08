from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    current_app,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("base.html")


if __name__ == "__main__":
    app.run()