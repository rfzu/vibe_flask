"""Main routes blueprint."""
from flask import Blueprint, jsonify, render_template

from app.services.quotes import get_all_quotes

main_bp = Blueprint("main", __name__)

# Статические посты блога (позже можно заменить на БД)
BLOG_POSTS = [
    {"slug": "pervyj-post", "title": "Первый пост", "date": "2025-03-01", "excerpt": "Краткое описание первого поста в блоге."},
    {"slug": "flask-i-cloud", "title": "Flask и облачный хостинг", "date": "2025-02-28", "excerpt": "Как развернуть Flask-приложение в Yandex Cloud."},
    {"slug": "kotirovki-akcij", "title": "Котировки акций в реальном времени", "date": "2025-02-25", "excerpt": "Интеграция с MOEX ISS API для отображения котировок."},
]


@main_bp.route("/")
def index():
    """Главная."""
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Обо мне."""
    return render_template("about.html")


@main_bp.route("/project")
def project():
    """О проекте — описание для GitHub (vibe coding pet project)."""
    return render_template("project.html")


@main_bp.route("/quotes")
def quotes():
    """Котировки Сбера и Совкомбанка."""
    return render_template("quotes.html", quotes=get_all_quotes())


@main_bp.route("/quotes/refresh")
def quotes_refresh():
    """API: обновлённые котировки (для кнопки «Обновить»)."""
    return jsonify(get_all_quotes())


@main_bp.route("/blog")
def blog():
    """Блог — список постов."""
    return render_template("blog.html", posts=BLOG_POSTS)


@main_bp.route("/blog/<slug>")
def blog_post(slug):
    """Блог — один пост."""
    post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    if not post:
        return render_template("404.html"), 404
    return render_template("blog_post.html", post=post)


@main_bp.route("/health")
def health():
    """Health check для Yandex Load Balancer / Serverless Containers."""
    return jsonify({"status": "ok"}), 200
