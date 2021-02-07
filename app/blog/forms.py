from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, length, ValidationError
from app.models.blog import Category

choices = [(category.id, category.name) for category in
           Category.query.filter_by( active=True ).order_by( Category.name.asc() ).all()]
print( choices )


class CreateBlogForm( FlaskForm ):
    title = StringField( "Title", validators=[DataRequired(), length( min=24, max=255 )] )
    content = TextAreaField( "Content", validators=[DataRequired()] )
    featured_image_id = IntegerField( "Feature Image Id" )
    categories = SelectMultipleField( "Select category", choices=choices )
    submit = SubmitField( "Create" )

    def validate_title(self, field):
        pass


class UpdateBlogForm( FlaskForm ):
    title = StringField( "Title", validators=[DataRequired(), length( min=24, max=255 )] )
    content = TextAreaField( "Content", validators=[DataRequired()] )
    featured_image_id = IntegerField( "Feature Image Id" )
    categories = SelectMultipleField( "Select category", choices=choices )
    submit = SubmitField( "Update" )


class CategoryForm( FlaskForm ):
    name = StringField( "Name", validators=[DataRequired(), length( min=3, max=64 )] )
    submit = SubmitField( "Create" )

    def validate_name(self, field):
        category = Category.query.filter_by( name=field.data.lower() ).first()
        if category:
            raise ValidationError( "Category already exists" )


class UpdateCategoryForm( FlaskForm ):
    name = StringField( "Name", validators=[DataRequired(), length( min=3, max=64 )] )
    submit = SubmitField( "Create" )

    def __init__(self, category, *args, **kwargs):
        super( UpdateCategoryForm, self ).__init__( *args, **kwargs )
        self.category = category

    def validate(self):
        rv = FlaskForm.validate( self )
        if not rv:
            return False

        category = Category.query.filter( Category.name.is_( self.name.data ),
                                          Category.id.isnot( self.category.id ) ).first()
        if category is not None:
            self.name.errors.append( 'Category already exists!' )
            return False

        return True
