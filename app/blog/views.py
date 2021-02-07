from flask import redirect, request, render_template, url_for, Blueprint
from app import app
from app.blog.forms import CreateBlogForm, UpdateBlogForm, CategoryForm, UpdateCategoryForm
from flask_login import login_required, current_user
from app.models.blog import Category


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


@login_required
@app.route('/category', methods=["GET", "POST"])
def create_category():

    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(form.name.data.lower(), current_user.get_id())
        category.save()

        return redirect(url_for("home"))
    else:
        print(form.errors.items())

    return render_template("category/create.html", form=form)


@login_required
@app.route('/category/<id>', methods=["GET", "POST"])
def update_category(id):
    category = Category.query.get(int(id))
    form = UpdateCategoryForm(category)

    if form.validate_on_submit():
        category.name = form.name.data
        category.active = True
        category.save()

        return redirect(url_for("home"))
    else:
        form.name.data = category.name
        # print(form.errors.items())

    return render_template("category/update.html", form=form)