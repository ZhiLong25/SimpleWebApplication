from wtforms import Form, StringField, RadioField, SelectField, PasswordField, IntegerField, validators,DecimalField, TextAreaField, FileField
from wtforms.fields import EmailField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

from flask_wtf import FlaskForm

class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    membership = RadioField('Membership', choices=[('Y', 'Yes'), ('N', 'No')], default='Y')
    username = StringField('Username', [validators.length(min=1, max=150), validators.DataRequired()])

    password = PasswordField('Password', [validators.length(min=1, max=150), validators.DataRequired(message="Password cannot be empty"), EqualTo('c_password', message='Passwords must match')])
    c_password = PasswordField('Confirm Password', [validators.length(min=1, max=150), validators.DataRequired()])

    phoneno = IntegerField('Phone Number', [validators.DataRequired()])

class CreateAdminForm(Form):
    first_name = StringField('First Name', validators=[InputRequired(message="First name cannot be empty")])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    username = StringField('Username', [validators.length(min=1, max=150), validators.DataRequired()])

    password = PasswordField('Password', [validators.length(min=1, max=150), validators.DataRequired(message="Password cannot be empty"), EqualTo('c_password', message='Passwords must match')])
    c_password = PasswordField('Confirm Password', [validators.length(min=1, max=150), validators.DataRequired()])

    email = EmailField('Email', [validators.length(min=1, max=150), validators.DataRequired()])
    phoneno = StringField('Phone Number', [validators.length(min=1, max=150), validators.DataRequired()])
    role = SelectField('Admin Role', [validators.DataRequired()], choices=[('', 'Select'), ('S', 'Semi'), ('F', 'Full')], default='')

class SearchProduct(Form):
    product = StringField('Search Product', [validators.Length(min=1, max=150), validators.DataRequired()])


class CreateProductForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(message="Please upload jpg or png files"), FileAllowed(['jpg', 'png'])])
    prod_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired(message="Product name cannot be empty")])
    description = TextAreaField('Description', [validators.Length(min=1, max=150), validators.DataRequired(message="Description cannot be empty")])
    price = IntegerField('Price', [validators.DataRequired(message="Price cannot be empty and must be an integer")])
    stock = IntegerField('Stock', [validators.DataRequired(message="Stock cannot be empty and must be an integer")])
    ref_no = IntegerField('Reference Number', [validators.DataRequired(message="Reference Number cannot be empty and must be an integer")])

class IndivProductForm(Form):
    quantity = IntegerField('Quantity: ', [validators.DataRequired("Quantity cannot be empty"), validators.NumberRange(min=1, message="Must be at least 1")])

class delivery_info(Form):
    address = StringField('Address', [validators.Length(min=1, max=150,), validators.DataRequired(message='Please enter an address')])
    postal = IntegerField('Postal Code', [validators.DataRequired(message='Please enter a postal code')])
    card_number = IntegerField('Card Number', [ validators.DataRequired(message='Please enter a card number')])
    name_on_card = StringField('Name on Card', [validators.Length(min=1, max=150), validators.DataRequired(message='Please enter the Name on Card')])
    expiry_date = StringField('Expiry Date (mm/yy)', [validators.Length(min=1, max=5), validators.DataRequired(message='Please enter a date(mm/yy)')])
    cvv = StringField('CVV', [validators.Length(min=1, max=3), validators.DataRequired(message='Please enter your CVV')])
