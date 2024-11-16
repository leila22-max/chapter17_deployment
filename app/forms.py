from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Email, ValidationError, EqualTo
from app.models import User


class EditProfileForm(FlaskForm):
    """Edit Profile Form"""
    username = StringField('Username', validators= [DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Edit Profile')

    def __init__(self, original_username, *args, **kwargs) -> None:
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Username Already In Use. Please Use A Diffrent Username')



class RegisterForm(FlaskForm):
    """Register Form"""
    username = StringField('Username', validators= [DataRequired(), Length(1, 64)])
    email = StringField('Email', validators= [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Validate New User Username"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username Already In Use. Please Use A Diffrent Username')
    def validate_email(self, email):
        
        """Validate New User Email"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Already In Use. Please Use A Diffrent Email')

    
class AddProductForm(FlaskForm):
    """ Add Product Form """
    product_name = StringField('Product Name', validators= [DataRequired(), Length(1, 64)])
    product_description = StringField('Product Description', validators= [DataRequired(), Length(1, 64)])
    stock_available = SelectField('Stock Available', choices = [(1,1),(2,2),(3,3),(4,4),(5,5)])
    submit = SubmitField('Add Product')


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username', validators= [DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators= [DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class PostForm(FlaskForm):
    """Comment Form"""
    body = TextAreaField('body', validators=[DataRequired()])
    submit = SubmitField('Post Now')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),EqualTo('password')]
    )
    submit = SubmitField('Reset Password')