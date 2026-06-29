from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import Appointment, Notification, Review

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    appointments = Appointment.query.filter_by(owner_id=current_user.id).order_by(Appointment.starts_at.desc()).limit(5).all()
    reviews = Review.query.filter_by(author_id=current_user.id).order_by(Review.created_at.desc()).limit(5).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5).all()
    return render_template("dashboard/index.html", appointments=appointments, reviews=reviews, notifications=notifications)
