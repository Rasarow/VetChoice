from flask import Blueprint, render_template, request

from app.models import Doctor

bp = Blueprint("doctors", __name__)


@bp.route("/")
def index():
    doctors_query = Doctor.query.filter_by(is_deleted=False, is_archived=False)
    city = request.args.get("city", "").strip()
    specialty = request.args.get("specialty", "").strip()
    animal = request.args.get("animal", "").strip()
    home_visit = request.args.get("home_visit") == "1"
    sort = request.args.get("sort", "rating")

    if city:
        doctors_query = doctors_query.filter(Doctor.city.ilike(f"%{city}%"))
    if specialty:
        doctors_query = doctors_query.filter(Doctor.specializations.ilike(f"%{specialty}%"))
    if animal:
        doctors_query = doctors_query.filter(Doctor.animal_types.ilike(f"%{animal}%"))
    if home_visit:
        doctors_query = doctors_query.filter_by(home_visit=True)

    if sort == "price":
        doctors_query = doctors_query.order_by(Doctor.price_from.asc())
    elif sort == "experience":
        doctors_query = doctors_query.order_by(Doctor.experience_years.desc())
    else:
        doctors_query = doctors_query.order_by(Doctor.verified.desc(), Doctor.experience_years.desc())

    doctors = doctors_query.all()
    return render_template("doctors/index.html", doctors=doctors)


@bp.route("/<int:doctor_id>")
def detail(doctor_id):
    doctor = Doctor.query.filter_by(id=doctor_id, is_deleted=False, is_archived=False).first_or_404()
    similar = Doctor.query.filter(Doctor.id != doctor.id, Doctor.city == doctor.city, Doctor.is_deleted.is_(False), Doctor.is_archived.is_(False)).limit(3).all()
    return render_template("doctors/detail.html", doctor=doctor, similar=similar)
