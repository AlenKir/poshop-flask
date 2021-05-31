from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    cost = FloatField('Cost In $', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    submit = SubmitField('Save')
