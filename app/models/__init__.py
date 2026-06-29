from datetime import date, datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(UserMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(160), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), default="owner", nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    trust_score = db.Column(db.Integer, default=0, nullable=False)

    pets = db.relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="author", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class City(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class Clinic(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    doctors = db.relationship("Doctor", back_populates="clinic")


class Doctor(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(160), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    middle_name = db.Column(db.String(80))
    title = db.Column(db.String(160), nullable=False)
    city = db.Column(db.String(120), nullable=False, index=True)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(80))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    district = db.Column(db.String(120))
    gender = db.Column(db.String(40))
    date_of_birth = db.Column(db.Date)
    experience_years = db.Column(db.Integer, default=0)
    years_of_experience = db.Column(db.Integer, default=0)
    price_from = db.Column(db.Integer, nullable=False)
    animal_types = db.Column(db.String(255), default="Cats, Dogs")
    home_visit = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=True)
    profile_status = db.Column(db.String(40), default="UNCLAIMED", nullable=False)
    verification_status = db.Column(db.String(40), default="NOT_VERIFIED", nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    photo_url = db.Column(db.String(500))
    profile_photo = db.Column(db.String(500))
    bio = db.Column(db.Text)
    biography = db.Column(db.Text)
    education = db.Column(db.Text)
    certifications = db.Column(db.Text)
    languages = db.Column(db.String(255))
    primary_specialization_id = db.Column(db.Integer)
    primary_specialization = db.Column(db.String(160))
    specializations = db.Column(db.String(500), index=True)
    services = db.Column(db.Text)
    working_hours = db.Column(db.String(255), default="Mon–Fri, 09:00–18:00")
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))

    clinic = db.relationship("Clinic", back_populates="doctors")
    owner_user = db.relationship("User", foreign_keys=[owner_user_id])
    reviews = db.relationship("Review", back_populates="doctor", cascade="all, delete-orphan")
    doctor_services = db.relationship("DoctorService", back_populates="doctor", cascade="all, delete-orphan")
    documents = db.relationship("DoctorDocument", back_populates="doctor", cascade="all, delete-orphan")

    @property
    def rating(self) -> float:
        if not self.reviews:
            return 0.0
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1)

    @property
    def recommendation_percent(self) -> int:
        if not self.reviews:
            return 0
        recommended = sum(1 for review in self.reviews if review.recommend)
        return round(recommended / len(self.reviews) * 100)

    @property
    def public_photo(self) -> str | None:
        return self.profile_photo or self.photo_url

    @property
    def public_bio(self) -> str | None:
        return self.biography or self.bio

    @property
    def public_experience_years(self) -> int:
        return self.years_of_experience or self.experience_years or 0


class DoctorService(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    service_name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False, default=0)

    doctor = db.relationship("Doctor", back_populates="doctor_services")


class DoctorDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    document_type = db.Column(db.String(120), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)

    doctor = db.relationship("Doctor", back_populates="documents")


class Pet(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(40))
    color = db.Column(db.String(80))
    special_marks = db.Column(db.String(255))
    chip_number = db.Column(db.String(120))
    diseases = db.Column(db.Text)
    photo_url = db.Column(db.String(500))

    owner = db.relationship("User", back_populates="pets")
    reviews = db.relationship("Review", back_populates="pet")

    @property
    def age_label(self) -> str:
        if not self.birth_date:
            return "Age not set"
        years = max(0, int((date.today() - self.birth_date).days / 365.25))
        return f"{years} years old"


class Review(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"))
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    visit_date = db.Column(db.Date)
    treatment_reason = db.Column(db.String(255))
    treatment_result = db.Column(db.String(255))
    recommend = db.Column(db.Boolean, default=True)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_type = db.Column(db.String(80))
    verification_status = db.Column(db.String(40), default="Pending", nullable=False)
    moderation_status = db.Column(db.String(40), default="Pending", nullable=False)
    trust_weight = db.Column(db.Float, default=1.0, nullable=False)

    author = db.relationship("User", back_populates="reviews")
    doctor = db.relationship("Doctor", back_populates="reviews")
    pet = db.relationship("Pet", back_populates="reviews")
    documents = db.relationship("ReviewDocument", back_populates="review", cascade="all, delete-orphan")


class ReviewDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    document_type = db.Column(db.String(120), nullable=False)
    ocr_text = db.Column(db.Text)
    extracted_data = db.Column(db.JSON)
    verification_result = db.Column(db.String(40), default="Pending", nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    review = db.relationship("Review", back_populates="documents")


class Appointment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    starts_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(40), default="scheduled", nullable=False)
    comment = db.Column(db.Text)


class Favorite(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint("owner_id", "doctor_id", name="uq_owner_doctor_favorite"),)


class Notification(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
