from datetime import date, datetime, timedelta

from app.extensions import db
from app.models import Appointment, Clinic, Doctor, DoctorDocument, DoctorService, Notification, Pet, Review, User


def seed_demo_data() -> None:
    db.drop_all()
    db.create_all()

    owner = User(email="owner@example.com", full_name="Sasha Pet Owner", is_verified=True, trust_score=85)
    owner.set_password("password123")
    db.session.add(owner)

    admin = User(email="admin@example.com", full_name="VetChoice Admin", role="admin", is_verified=True, trust_score=100)
    admin.set_password("password123")
    db.session.add(admin)

    clinic = Clinic(
        name="Purple Paw Veterinary Center",
        city="Moscow",
        address="Pet Care Avenue, 14",
        description="Premium multispecialty veterinary clinic with diagnostics and surgery.",
    )
    db.session.add(clinic)
    db.session.flush()

    doctors = [
        Doctor(first_name="Anna", last_name="Petrova", full_name="Dr. Anna Petrova", title="Veterinary cardiologist", primary_specialization="Cardiology", profile_status="UNCLAIMED", verification_status="NOT_VERIFIED", city="Moscow", address="Pet Care Avenue, 14", phone_number="+7 900 111-22-33", email="anna.petrova@example.com", website="https://vetchoice.local/anna", district="Tverskoy", gender="Female", experience_years=12, years_of_experience=12, price_from=3500, animal_types="Cats, Dogs", home_visit=True, specializations="Cardiology, Ultrasound, Preventive care", services="Consultation, ECG, ultrasound, treatment plan", education="Moscow State Academy of Veterinary Medicine", certifications="Veterinary cardiology certificate", languages="Russian, English", bio="Calm, evidence-based specialist focused on chronic heart disease and senior pets.", biography="Calm, evidence-based specialist focused on chronic heart disease and senior pets.", clinic_id=clinic.id),
        Doctor(first_name="Maksim", last_name="Orlov", full_name="Dr. Maksim Orlov", title="Veterinary surgeon", primary_specialization="Surgery", profile_status="UNCLAIMED", verification_status="NOT_VERIFIED", city="Moscow", address="Pet Care Avenue, 14", phone_number="+7 900 222-33-44", district="Arbat", gender="Male", experience_years=9, years_of_experience=9, price_from=4200, animal_types="Dogs, Cats, Rodents", home_visit=False, specializations="Surgery, Orthopedics, Emergency", services="Consultation, surgery, post-op care", education="Advanced veterinary surgery fellowship", certifications="Orthopedic surgery certificate", languages="Russian", bio="Experienced surgeon known for transparent communication and careful recovery plans.", biography="Experienced surgeon known for transparent communication and careful recovery plans.", clinic_id=clinic.id),
        Doctor(first_name="Elena", last_name="Smirnova", full_name="Dr. Elena Smirnova", title="Dermatology and nutrition vet", primary_specialization="Dermatology", profile_status="UNCLAIMED", verification_status="NOT_VERIFIED", city="Saint Petersburg", address="Central District, 8", phone_number="+7 900 333-44-55", district="Central", gender="Female", experience_years=7, years_of_experience=7, price_from=2800, animal_types="Cats, Dogs, Birds, Fish", home_visit=True, specializations="Dermatology, Nutrition, Allergies", services="Diet plans, allergy diagnostics, skin treatment", education="European dermatology continuing education", certifications="Veterinary nutrition certificate", languages="Russian, English", bio="Helps itchy pets and owners with practical long-term skin and nutrition plans.", biography="Helps itchy pets and owners with practical long-term skin and nutrition plans.", clinic_id=clinic.id),
    ]
    db.session.add_all(doctors)
    db.session.flush()

    db.session.add_all([
        DoctorService(doctor=doctors[0], service_name="Cardiology consultation", description="Exam, auscultation, ECG recommendation", price=3500),
        DoctorService(doctor=doctors[0], service_name="Ultrasound", description="Focused cardiac ultrasound", price=4500),
        DoctorService(doctor=doctors[1], service_name="Surgical consultation", description="Treatment options and recovery plan", price=4200),
        DoctorService(doctor=doctors[2], service_name="Dermatology consultation", description="Skin exam and allergy plan", price=2800),
    ])
    db.session.add_all([
        DoctorDocument(doctor=doctors[0], document_type="Diploma", file_url="https://example.com/documents/anna-diploma.pdf", verified=True),
        DoctorDocument(doctor=doctors[0], document_type="Certificate", file_url="https://example.com/documents/anna-cardio-certificate.pdf", verified=True),
        DoctorDocument(doctor=doctors[1], document_type="Certificate", file_url="https://example.com/documents/maksim-surgery-certificate.pdf", verified=True),
        DoctorDocument(doctor=doctors[2], document_type="GALLERY", file_url="https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?auto=format&fit=crop&w=1000&q=80", verified=False),
    ])

    pet = Pet(owner=owner, name="Mila", species="Dog", breed="Corgi", birth_date=date(2020, 5, 12), gender="Female", color="Red white", special_marks="White heart-shaped mark on chest", chip_number="643094100000001", diseases="None", photo_url="https://images.unsplash.com/photo-1612536057832-2ff7ead58194?auto=format&fit=crop&w=800&q=80")
    db.session.add(pet)
    db.session.flush()

    reviews = [
        Review(author=owner, doctor=doctors[0], pet=pet, rating=5, text="Dr. Anna explained every step and helped us build a clear treatment plan. The visit felt calm and premium.", visit_date=date.today() - timedelta(days=20), treatment_reason="Heart murmur check", treatment_result="Stable, monitoring plan", recommend=True, verified=True, verification_type="Uploaded invoice", verification_status="Approved", moderation_status="Approved", trust_weight=1.2),
        Review(author=owner, doctor=doctors[1], pet=pet, rating=5, text="Very professional surgical consultation. Prices and recovery timeline were explained before any decisions.", visit_date=date.today() - timedelta(days=55), treatment_reason="Limping", treatment_result="Conservative treatment", recommend=True, verified=True, verification_type="Uploaded invoice", verification_status="Approved", moderation_status="Approved", trust_weight=1.1),
    ]
    db.session.add_all(reviews)
    db.session.add(Appointment(owner_id=owner.id, doctor_id=doctors[0].id, pet_id=pet.id, starts_at=datetime.utcnow() + timedelta(days=4), comment="Vaccination reminder and cardiac follow-up"))
    db.session.add(Notification(user_id=owner.id, title="Vaccination reminder", body="Mila is due for annual vaccination next month."))
    db.session.commit()
