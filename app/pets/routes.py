from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import PetForm
from app.models import Pet
from app.utils.breeds import BREED_CHOICES

bp = Blueprint("pets", __name__)


@bp.route("/")
@login_required
def index():
    pets = Pet.query.filter_by(owner_id=current_user.id).order_by(Pet.created_at.desc()).all()
    return render_template("pets/index.html", pets=pets)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = PetForm()
    form.breed.choices = BREED_CHOICES
    if form.validate_on_submit():
        pet = Pet(owner_id=current_user.id)
        form.populate_obj(pet)
        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.name}'s profile was created.", "success")
        return redirect(url_for("pets.detail", pet_id=pet.id))
    return render_template("pets/form.html", form=form, title="Add pet")


@bp.route("/<int:pet_id>")
@login_required
def detail(pet_id):
    pet = Pet.query.filter_by(id=pet_id, owner_id=current_user.id).first_or_404()
    return render_template("pets/detail.html", pet=pet)


@bp.route("/<int:pet_id>/edit", methods=["GET", "POST"])
@login_required
def edit(pet_id):
    pet = Pet.query.filter_by(id=pet_id, owner_id=current_user.id).first_or_404()
    form = PetForm(obj=pet)
    form.breed.choices = BREED_CHOICES
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        flash("Pet profile updated.", "success")
        return redirect(url_for("pets.detail", pet_id=pet.id))
    return render_template("pets/form.html", form=form, title="Edit pet")
