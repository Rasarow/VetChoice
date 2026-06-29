from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegisterForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(max=160)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class PetForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    species = SelectField("Species", choices=[("Dog", "Dog"), ("Cat", "Cat"), ("Rodent", "Rodent"), ("Bird", "Bird"), ("Fish", "Fish"), ("Other", "Other")])
    breed = SelectField("Breed", validators=[Optional(), Length(max=120)])
    birth_date = DateField("Birth date", validators=[Optional()])
    gender = SelectField("Gender", choices=[("", "Not specified"), ("Female", "Female"), ("Male", "Male")], validators=[Optional()])
    color = StringField("Color", validators=[Optional(), Length(max=80)])
    special_marks = StringField("Special marks", validators=[Optional(), Length(max=255)])
    photo_url = StringField("Photo URL", validators=[Optional(), Length(max=500)])
    chip_number = StringField("Chip number", validators=[Optional(), Length(max=120)])
    diseases = TextAreaField("Diseases", validators=[Optional()])
    submit = SubmitField("Save pet")


class ReviewForm(FlaskForm):
    rating = IntegerField("Rating", validators=[DataRequired(), NumberRange(min=1, max=5)])
    pet_id = SelectField("Pet", coerce=int, validators=[Optional()])
    visit_date = DateField("Visit date", validators=[Optional()])
    treatment_reason = StringField("Treatment reason", validators=[Optional(), Length(max=255)])
    treatment_result = StringField("Treatment result", validators=[Optional(), Length(max=255)])
    text = TextAreaField("Review", validators=[DataRequired(), Length(min=20)])
    recommend = BooleanField("I recommend this specialist", default=True)
    submit = SubmitField("Publish review")


class DoctorAdminForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=80)])
    middle_name = StringField("Middle name", validators=[Optional(), Length(max=80)])
    profile_photo = StringField("Profile photo URL", validators=[Optional(), Length(max=500)])
    biography = TextAreaField("Biography / About", validators=[Optional()])
    gender = SelectField("Gender", choices=[("", "Not specified"), ("Female", "Female"), ("Male", "Male"), ("Other", "Other")], validators=[Optional()])
    date_of_birth = DateField("Date of birth", validators=[Optional()])
    years_of_experience = IntegerField("Years of experience", validators=[Optional(), NumberRange(min=0)])
    primary_specialization = StringField("Primary specialization", validators=[DataRequired(), Length(max=160)])
    specializations = StringField("Additional specializations", validators=[Optional(), Length(max=500)])
    education = TextAreaField("Education", validators=[Optional()])
    certifications = TextAreaField("Certifications", validators=[Optional()])
    languages = StringField("Languages spoken", validators=[Optional(), Length(max=255)])
    clinic_name = StringField("Clinic", validators=[Optional(), Length(max=180)])
    city = StringField("City", validators=[DataRequired(), Length(max=120)])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    phone_number = StringField("Phone number", validators=[Optional(), Length(max=80)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=255)])
    website = StringField("Website", validators=[Optional(), Length(max=255)])
    animal_types = StringField("Animal types", validators=[Optional(), Length(max=255)])
    price_from = IntegerField("Price from", validators=[DataRequired(), NumberRange(min=0)])
    services_data = TextAreaField("Services", validators=[Optional()])
    documents_data = TextAreaField("Documents", validators=[Optional()])
    gallery_data = TextAreaField("Gallery images", validators=[Optional()])
    create_anyway = BooleanField("Create anyway if duplicate is found")
    submit = SubmitField("Save doctor")
