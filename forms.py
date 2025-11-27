from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class PersonalInformationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    college = StringField('College/University', validators=[DataRequired()])
    country = SelectField('Country', choices=[
        ('', 'Select Country'),
        ('US', 'United States'),
        ('IN', 'India'),
        ('UK', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('JP', 'Japan'),
        ('SG', 'Singapore'),
        ('OTHER', 'Other')
    ], validators=[DataRequired()])
    degree = SelectField('Degree Program', choices=[
        ('', 'Select Degree'),
        ('Computer Science', 'Computer Science'),
        ('Engineering', 'Engineering'),
        ('Business Administration', 'Business Administration'),
        ('Data Science', 'Data Science'),
        ('Information Technology', 'Information Technology'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Economics', 'Economics'),
        ('Psychology', 'Psychology'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    year_of_study = SelectField('Year of Study', choices=[
        ('', 'Select Year'),
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
        ('Graduate', 'Graduate'),
        ('Postgraduate', 'Postgraduate')
    ], validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    linkedin = StringField('LinkedIn Profile', validators=[Optional()])
    submit = SubmitField('Continue to Skills Assessment')