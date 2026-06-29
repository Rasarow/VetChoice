from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ReviewForm
from app.models import Doctor, Pet, Review

bp = Blueprint("reviews", __name__)


@bp.route("/doctor/<int:doctor_id>/new", methods=["GET", "POST"])
@login_required
def create(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = ReviewForm()
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    form.pet_id.choices = [(0, "No pet selected")] + [(pet.id, pet.name) for pet in pets]
    if form.validate_on_submit():
        review = Review(
            author_id=current_user.id,
            doctor_id=doctor.id,
            pet_id=form.pet_id.data or None,
            rating=form.rating.data,
            text=form.text.data,
            visit_date=form.visit_date.data,
            treatment_reason=form.treatment_reason.data,
            treatment_result=form.treatment_result.data,
            recommend=form.recommend.data,
            verified=False,
            verification_type="Document upload",
            verification_status="Pending",
            moderation_status="Pending",
            trust_weight=1.0,
        )
        db.session.add(review)
        db.session.commit()
        flash("Thank you — your review was submitted and is pending verification/moderation.", "success")
        return redirect(url_for("doctors.detail", doctor_id=doctor.id))
    return render_template("reviews/form.html", form=form, doctor=doctor)
