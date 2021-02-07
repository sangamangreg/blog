from flask import redirect, request, render_template, url_for, Blueprint
from app import app
from app.blog.forms import CreateBlogForm, UpdateBlogForm
from flask_login import login_required

blogs = Blueprint( "blogs", __name__, template_folder="templates" )


@login_required
@app.route( "/blogs", methods=["GET", "POST"] )
def create_blog():
    blog_form = CreateBlogForm()

    if blog_form.validate_on_submit():
        return redirect( url_for( "home" ) )

    return render_template( "blog/create.html", blog_form=blog_form )


@login_required
@app.route( "/blogs/<blog_id>", methods=["GET", "POST"] )
def update_blog(blog_id):
    blog_form = UpdateBlogForm()

    if blog_form.validate_on_submit():
        return redirect( url_for( "home" ) )

    return render_template( "blog/update.html", blog_form=blog_form )


@login_required
@app.route( "/blogs/<slug>", methods=["GET"] )
def get_blog(slug):
    return render_template( "blog/details.html" )