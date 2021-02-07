import os
from flask import redirect, request, render_template, url_for, Blueprint
from app import app, BLOG_IMAGE_PATH, BLOG_UPLOAD_PATH
from app.blog.forms import CreateBlogForm, UpdateBlogForm, CategoryForm, UpdateCategoryForm
from flask_login import login_required, current_user
from app.models.blog import Category, Blog
from app.models.attachment import Attachment
from werkzeug.utils import secure_filename


blogs = Blueprint( "blogs", __name__, template_folder="templates" )


@login_required
@app.route( "/blogs", methods=["GET", "POST"] )
def create_blog():
    blog_form = CreateBlogForm()

    if blog_form.validate_on_submit():
        f = request.files['featured_image']
        mimetype = f.content_type
        f_split = f.filename.split( '.' )
        extension = ''
        if len(f_split) == 2:
            extension = f_split[1]
        secure_name = secure_filename( f.filename)
        file_path = os.path.join( BLOG_IMAGE_PATH, secure_name )

        f.save( file_path )
        attachment = Attachment( secure_name, mimetype, extension, os.path.join(BLOG_UPLOAD_PATH, secure_name), current_user.get_id() )
        attachment.save()
        if attachment:
            blog = Blog(
                blog_form.title.data,
                blog_form.content.data,
                blog_form.categories.data,
                current_user.get_id(),
                attachment.id
            )
            blog.save()
            return redirect(url_for("home"))
        return redirect( url_for( "home" ) )
    else:
        print(blog_form.errors.items())

    return render_template( "blog/create.html", blog_form=blog_form )


@login_required
@app.route( "/blogs/<blog_id>", methods=["GET", "POST"] )
def update_blog(blog_id):
    blog = Blog.query.get(blog_id)
    blog_form = UpdateBlogForm()
    file_url = ''
    if blog_form.validate_on_submit():
        if blog_form.featured_image.data:
            f = request.files['featured_image']
            mimetype = f.content_type
            f_split = f.filename.split( '.' )
            extension = ''
            if len( f_split ) == 2:
                extension = f_split[1]
            secure_name = secure_filename( f.filename )
            file_path = os.path.join( BLOG_IMAGE_PATH, secure_name )
            f.save( file_path )
            attachment = Attachment( secure_name, mimetype, extension, os.path.join(BLOG_UPLOAD_PATH, secure_name), current_user.get_id() )
            attachment.save()
            blog.featured_image_id = attachment.id

        blog.title = blog_form.title.data
        blog.content = blog_form.content.data
        blog.categories = blog_form.categories.data
        blog.save()

        return redirect( url_for( "home" ) )
    else:
        blog_form.title.data = blog.title
        blog_form.content.data = blog.content
        blog_form.categories.data = blog.categories
        if blog.featured_image_id:
            attachemt = Attachment.query.get(blog.featured_image_id)
            file_url = attachemt.file_url

        print(blog_form.errors.items())
    return render_template( "blog/update.html", blog_form=blog_form, file_url=file_url )


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