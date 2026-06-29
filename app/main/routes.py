from flask import Blueprint, render_template, request

from app.models import Doctor

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    public_doctors_query = Doctor.query.filter_by(is_deleted=False, is_archived=False)
    popular_doctors = public_doctors_query.order_by(Doctor.experience_years.desc()).limit(3).all()
    cities = sorted({doctor.city for doctor in public_doctors_query.with_entities(Doctor.city).all()})
    specialties = sorted(
        {
            specialty.strip()
            for doctor in public_doctors_query.with_entities(Doctor.specializations).all()
            for specialty in (doctor.specializations or "").split(",")
            if specialty.strip()
        }
    )
    animal_types = ["Cats", "Dogs", "Rodents", "Birds", "Fish"]
    return render_template(
        "main/index.html",
        popular_doctors=popular_doctors,
        cities=cities,
        specialties=specialties,
        animal_types=animal_types,
    )


@bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    doctors = []
    if query:
        doctors = Doctor.query.filter_by(is_deleted=False, is_archived=False).filter(
            Doctor.full_name.ilike(f"%{query}%")
            | Doctor.specializations.ilike(f"%{query}%")
            | Doctor.city.ilike(f"%{query}%")
            | Doctor.animal_types.ilike(f"%{query}%")
        ).all()
    return render_template("main/search.html", query=query, doctors=doctors)
