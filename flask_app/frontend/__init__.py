from flask import url_for, render_template
from flask_imp import Blueprint
from pyhead import Head

bp = Blueprint(__name__)


@bp.before_app_request
def before_app_request():
    bp.init_session()


@bp.route("/")
def index():
    head = Head()
    head.set_title("Blueprint | frontend")

    vite_assets = bp.location / "static" / "assets"

    find_vite_js = vite_assets.glob("*.js")
    find_vite_css = vite_assets.glob("*.css")

    for file in find_vite_js:
        head.set_script_tag(
            src=url_for("frontend.static", filename=f"assets/{file.name}"),
            type="module",
            crossorigin="anonymous",
        )

    for file in find_vite_css:
        head.set_link_tag(
            rel="stylesheet",
            href=url_for("frontend.static", filename=f"assets/{file.name}"),
        )

    return render_template(bp.tmpl("index.html"), head=head)
