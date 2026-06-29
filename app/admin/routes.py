from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import DoctorAdminForm
from app.models import Clinic, Doctor, DoctorDocument, DoctorService

bp = Blueprint("admin", __name__)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role != "admin":
            flash("Admin access required.", "warning")
            return redirect(url_for("dashboard.index"))
        return view(*args, **kwargs)
    return wrapped


@bp.route("/")
@admin_required
def index():
    return redirect(url_for("admin.doctors"))


@bp.route("/doctors")
@admin_required
def doctors():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    query = Doctor.query
    if q:
        query = query.filter(
            Doctor.full_name.ilike(f"%{q}%") | Doctor.city.ilike(f"%{q}%") | Doctor.primary_specialization.ilike(f"%{q}%")
        )
    if status == "archived":
        query = query.filter_by(is_archived=True, is_deleted=False)
    elif status == "deleted":
        query = query.filter_by(is_deleted=True)
    else:
        query = query.filter_by(is_deleted=False)
    return render_template("admin/doctors/index.html", doctors=query.order_by(Doctor.created_at.desc()).all(), q=q, status=status)


@bp.route("/doctors/new", methods=["GET", "POST"])
@admin_required
def doctor_create():
    form = DoctorAdminForm()
    duplicate = _find_duplicate(form) if request.method == "POST" else None
    if form.validate_on_submit() and duplicate and not form.create_anyway.data:
        return render_template("admin/doctors/form.html", form=form, title="Add Doctor", duplicate=duplicate)
    if form.validate_on_submit():
        doctor = Doctor(profile_status="UNCLAIMED", verification_status="NOT_VERIFIED", owner_user_id=None)
        _save_doctor(doctor, form)
        flash("Doctor profile created.", "success")
        return redirect(url_for("admin.doctors"))
    return render_template("admin/doctors/form.html", form=form, title="Add Doctor", duplicate=None)


@bp.route("/doctors/<int:doctor_id>/edit", methods=["GET", "POST"])
@admin_required
def doctor_edit(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorAdminForm(obj=doctor)
    if request.method == "GET":
        form.clinic_name.data = doctor.clinic.name if doctor.clinic else form.clinic_name.data
        form.services_data.data = _services_to_text(doctor)
        form.documents_data.data = _documents_to_text(doctor, exclude="GALLERY")
        form.gallery_data.data = _documents_to_text(doctor, only="GALLERY")
    if form.validate_on_submit():
        _save_doctor(doctor, form)
        flash("Doctor profile updated.", "success")
        return redirect(url_for("admin.doctors"))
    return render_template("admin/doctors/form.html", form=form, title="Edit Doctor", duplicate=None, doctor=doctor)


@bp.route("/doctors/<int:doctor_id>/archive", methods=["POST"])
@admin_required
def doctor_archive(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_archived = not doctor.is_archived
    db.session.commit()
    flash("Doctor archive status updated.", "success")
    return redirect(url_for("admin.doctors"))


@bp.route("/doctors/<int:doctor_id>/delete", methods=["POST"])
@admin_required
def doctor_delete(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_deleted = True
    db.session.commit()
    flash("Doctor soft deleted.", "success")
    return redirect(url_for("admin.doctors"))


def _find_duplicate(form):
    if not form.first_name.data or not form.last_name.data or not form.city.data:
        return None
    return Doctor.query.filter(
        Doctor.first_name.ilike(form.first_name.data),
        Doctor.last_name.ilike(form.last_name.data),
        Doctor.city.ilike(form.city.data),
        Doctor.is_deleted.is_(False),
    ).first()


def _save_doctor(doctor, form):
    clinic = None
    if form.clinic_name.data:
        clinic = Clinic.query.filter_by(name=form.clinic_name.data, city=form.city.data).first()
        if not clinic:
            clinic = Clinic(name=form.clinic_name.data, city=form.city.data, address=form.address.data or "Address not set")
            db.session.add(clinic)
            db.session.flush()
    doctor.first_name = form.first_name.data
    doctor.last_name = form.last_name.data
    doctor.middle_name = form.middle_name.data
    doctor.full_name = " ".join(part for part in [form.first_name.data, form.middle_name.data, form.last_name.data] if part)
    doctor.title = form.primary_specialization.data
    doctor.primary_specialization = form.primary_specialization.data
    doctor.specializations = form.specializations.data
    doctor.profile_photo = form.profile_photo.data
    doctor.photo_url = form.profile_photo.data
    doctor.biography = form.biography.data
    doctor.bio = form.biography.data
    doctor.gender = form.gender.data
    doctor.date_of_birth = form.date_of_birth.data
    doctor.years_of_experience = form.years_of_experience.data or 0
    doctor.experience_years = form.years_of_experience.data or 0
    doctor.education = form.education.data
    doctor.certifications = form.certifications.data
    doctor.languages = form.languages.data
    doctor.city = form.city.data
    doctor.address = form.address.data
    doctor.phone_number = form.phone_number.data
    doctor.email = form.email.data
    doctor.website = form.website.data
    doctor.animal_types = form.animal_types.data or "Cats, Dogs"
    doctor.price_from = form.price_from.data or 0
    doctor.clinic = clinic
    db.session.add(doctor)
    db.session.flush()
    _replace_services(doctor, form.services_data.data)
    _replace_documents(doctor, form.documents_data.data, "DOCUMENT")
    _replace_documents(doctor, form.gallery_data.data, "GALLERY")
    db.session.commit()


def _replace_services(doctor, raw):
    DoctorService.query.filter_by(doctor_id=doctor.id).delete()
    for line in (raw or "").splitlines():
        parts = [part.strip() for part in line.split("|")]
        if parts and parts[0]:
            db.session.add(DoctorService(doctor_id=doctor.id, service_name=parts[0], description=parts[1] if len(parts) > 1 else "", price=int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0))


def _replace_documents(doctor, raw, default_type):
    if default_type == "GALLERY":
        DoctorDocument.query.filter_by(doctor_id=doctor.id, document_type="GALLERY").delete()
    else:
        DoctorDocument.query.filter(DoctorDocument.doctor_id == doctor.id, DoctorDocument.document_type != "GALLERY").delete()
    for line in (raw or "").splitlines():
        parts = [part.strip() for part in line.split("|")]
        if parts and parts[0]:
            doc_type = default_type if default_type == "GALLERY" else parts[0]
            file_url = parts[0] if default_type == "GALLERY" else (parts[1] if len(parts) > 1 else "")
            if file_url:
                db.session.add(DoctorDocument(doctor_id=doctor.id, document_type=doc_type, file_url=file_url, verified=False))


def _services_to_text(doctor):
    return "\n".join(f"{s.service_name} | {s.description or ''} | {s.price}" for s in doctor.doctor_services)


def _documents_to_text(doctor, only=None, exclude=None):
    docs = doctor.documents
    if only:
        docs = [doc for doc in docs if doc.document_type == only]
        return "\n".join(doc.file_url for doc in docs)
    if exclude:
        docs = [doc for doc in docs if doc.document_type != exclude]
    return "\n".join(f"{doc.document_type} | {doc.file_url}" for doc in docs)