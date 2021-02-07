from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, length
from app.models.blog import Category


choices = [(category.id, category.name) for category in
           Category.query.filter_by( active=True ).order_by( Category.name.asc() ).all()]


class CreateBlogForm( FlaskForm ):
    title = StringField( "Title", validators=[DataRequired(), length( min=24, max=255 )] )
    content = TextAreaField( "Content", validators=[DataRequired()] )
    featured_image_id = IntegerField( "Feature Image Id" )
    categories = SelectMultipleField( "Select category", choices=choices )

    def validate_title(self):
        pass


class UpdateBlogForm( FlaskForm ):
    title = StringField( "Title", validators=[DataRequired(), length( min=24, max=255 )] )
    content = TextAreaField( "Content", validators=[DataRequired()] )
    featured_image_id = IntegerField( "Feature Image Id" )
    categories = SelectMultipleField( "Select category", choices=choices )


class CategoryForm( FlaskForm ):
    name = StringField( "Name", validators=[DataRequired(), length( min=24, max=64 )] )

    def validate_name(self):
        pass
