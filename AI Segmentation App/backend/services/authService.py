from backend.services.firebaseService import firebase_service
import hashlib

class AuthService:
    @staticmethod
    def authenticate_doctor(email, password):
        """
        Authenticate a doctor using email and password.
        Passwords are stored as SHA-256 hashes in Firebase.
        """
        doctor = firebase_service.get_doctor_by_email(email)
        if not doctor:
            return None, "Doctor not found"

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if doctor.get('password') != password_hash:
            return None, "Invalid password"

        safe_doctor = {k: v for k, v in doctor.items() if k != 'password'}
        return safe_doctor, None

    @staticmethod
    def validate_session(doctor_id):
        """
        Validate a session. (For now, always True if doctor exists)
        """
        doctor = firebase_service.get_doctor_by_id(doctor_id)
        return bool(doctor)

    @staticmethod
    def logout_doctor(doctor_id):
        """
        For now, we just clear session on client side.
        """
        return True
