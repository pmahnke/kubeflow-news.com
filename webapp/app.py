import datetime
import talisker.requests

from canonicalwebteam.blog import build_blueprint, BlogViews, BlogAPI
from canonicalwebteam.flask_base.app import FlaskBase


app = FlaskBase(
    __name__,
    "kubeflow-news.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

session = talisker.requests.get_session()

# Blog
blog_views = BlogViews(
    api=BlogAPI(
        session=session, api_url="https://ubuntu.com/blog/wp-json/wp/v2"
    ),
    blog_title="kubeflow-news",
    tag_ids=[3408],
    excluded_tags=[3184, 3265],
)


app.register_blueprint(build_blueprint(blog_views), url_prefix="/")


@app.template_filter("pluralize")
def pluralize_filter(total_posts):
    if int(total_posts) > 1:
        return "s"
    else:
        return ""


@app.template_filter("descending_years")
def descending_years_filter(end_year):
    now = datetime.datetime.now()
    return range(now.year, end_year, -1)


@app.template_filter("months_list")
def months_list_filter(year):
    months = []
    now = datetime.datetime.now()
    for i in range(1, 13):
        date = datetime.date(year, i, 1)
        if date < now.date():
            months.append({"name": date.strftime("%b"), "number": i})
    return months
