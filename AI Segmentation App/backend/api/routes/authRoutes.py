from flask import Blueprint, request, jsonify, session, current_app
from backend.services.authService import AuthService
from backend.services.firebaseService import firebase_service

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email']
        password = data['password']
        
        doctor, error = AuthService.authenticate_doctor(email, password)
        current_app.logger.info(f"Received login doctor: {doctor}") 
        current_app.logger.info(f"Received login id: {doctor['id']}") 
        if error:
            return jsonify({'error': error}), 401
        
        session['doctor_id'] = doctor['id']
        session['doctor_email'] = doctor['email']
        
        return jsonify({
            'message': 'Login successful',
            'doctor': doctor
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        doctor_id = session.get('doctor_id')
        if doctor_id:
            AuthService.logout_doctor(doctor_id)
        
        session.clear()
        return jsonify({'message': 'Logout successful'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_doctor():
    try:
        doctor_id = session.get('doctor_id')
        if not doctor_id:
            return jsonify({'error': 'Not authenticated'}), 401
        
        doctor = firebase_service.get_doctor_by_id(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        safe_doctor = {k: v for k, v in doctor.items() if k != 'password'}
        return jsonify({'doctor': safe_doctor}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
