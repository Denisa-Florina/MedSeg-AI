from flask import Blueprint, request, jsonify, send_file, session
from backend.services.segmentationService import segmentation_service
from backend.services.firebaseService import firebase_service
import io
from datetime import datetime
import zipfile

patient_bp = Blueprint('patients', __name__, url_prefix='/api/patients')

@patient_bp.route('/', methods=['GET'])
def get_patients():
    doctor_id = request.args.get('doctor_id') or session.get('doctor_id')
    if not doctor_id:
        return jsonify({'error': 'doctor_id is required'}), 400
    
    patients = firebase_service.get_patients_by_doctor(doctor_id)
    
    transformed_patients = []
    for p in patients:
        transformed_patients.append({
            'id': p['id'],
            'name': p['name'],
            'age': p['age'],
            'date': p['date'],
            'dicomFile': p.get('dicom_file', ''),
            'status': 'completed' if p.get('segmented') else 'processing',
            'confidence': p.get('metrics', {}).get('confidence', 0)
        })
    
    return jsonify({'patients': transformed_patients}), 200

@patient_bp.route('/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = firebase_service.get_patient_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    transformed_patient = {
        'id': patient['id'],
        'name': patient['name'],
        'age': patient['age'],
        'date': patient['date'],
        'dicomFile': patient.get('dicom_file', ''),
        'status': 'completed' if patient.get('segmented') else 'processing',
        'confidence': patient.get('metrics', {}).get('confidence', 0),
        'metrics': patient.get('metrics', {})
    }
    
    return jsonify({'patient': transformed_patient}), 200

@patient_bp.route('/', methods=['POST'])
def create_patient():
    try:
        name = request.form.get('name')
        age = request.form.get('age')
        doctor_id = request.form.get('doctor_id')
        dicom_files = request.files.getlist('dicom_file')
        
        print(f"Received: Name={name}, Age={age}, DocID={doctor_id}, Files={len(dicom_files)} uploaded")

        if not name or not age or not doctor_id:
            return jsonify({'error': 'Name, age, and doctor_id are required'}), 400

        try:
            age = int(age)
            if age < 1 or age > 150:
                return jsonify({'error': 'Age must be between 1 and 150'}), 400
        except ValueError:
            return jsonify({'error': 'Age must be a valid number'}), 400
        
        patient_data = {'name': name, 'age': age}
        
        if dicom_files and len(dicom_files) > 0:
            patient = segmentation_service.process_dicom(dicom_files, patient_data, doctor_id)
        else:
            new_patient_data = {
                'name': name,
                'age': age,
                'doctor_id': str(doctor_id), 
                'segmented': False, 
                'date': datetime.now().strftime("%Y-%m-%d"),
                'metrics': {'confidence': 0}
            }
            patient = firebase_service.add_patient(new_patient_data)

        if not patient:
            return jsonify({'error': 'Failed to create patient'}), 500

        transformed_patient = {
            'id': patient['id'],
            'name': patient['name'],
            'age': patient['age'],
            'date': patient['date'],
            'dicomFile': patient.get('dicom_file', ''),
            'status': 'completed' if patient.get('segmented') else 'pending',
            'confidence': patient.get('metrics', {}).get('confidence', 0)
        }
        
        return jsonify({
            'message': 'Patient created successfully',
            'patient': transformed_patient
        }), 201
    except Exception as e:
        print(f"Error creating patient: {str(e)}")
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>/upload-dicom', methods=['POST'])
def upload_dicom(patient_id):
    try:
        dicom_files = request.files.getlist('dicom_file')
        if not dicom_files or len(dicom_files) == 0:
            return jsonify({'error': 'No DICOM file uploaded'}), 400
        
        patient = firebase_service.get_patient_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        result = segmentation_service.process_uploaded_dicom(dicom_files, patient_id)
        
        return jsonify({
            'message': 'DICOM uploaded and processed successfully',
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        allowed_fields = {'name', 'age'}
        updates = {k: v for k, v in data.items() if k in allowed_fields}
        
        patient = firebase_service.update_patient(patient_id, updates)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify({
            'message': 'Patient updated successfully',
            'patient': patient
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        patient = firebase_service.get_patient_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        firebase_service.delete_patient(patient_id)
        return jsonify({'message': 'Patient deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>/re-segment', methods=['POST'])
def re_segment_patient(patient_id):
    try:
        patient = segmentation_service.re_segment(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify({
            'message': 'Re-segmentation completed',
            'patient': patient
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/<patient_id>/download/scan', methods=['GET'])
def download_scan(patient_id):
    """Download the original CT scan (.nii.gz)"""
    try:
        file_info = firebase_service.get_file_from_patient(patient_id, storage_key='scan_data')
        if not file_info:
            return jsonify({'error': 'Scan file not found'}), 404
        
        file_data = io.BytesIO(file_info['data'])
        filename = file_info.get('filename', 'scan.nii.gz')
        
        return send_file(
            file_data,
            mimetype='application/gzip',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error downloading scan: {str(e)}")
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>/download/mask', methods=['GET'])
def download_mask(patient_id):
    """Download the AI segmentation mask (.nii.gz)"""
    try:
        file_info = firebase_service.get_file_from_patient(patient_id, storage_key='mask_data')
        if not file_info:
            return jsonify({'error': 'Segmentation mask not found'}), 404
        
        file_data = io.BytesIO(file_info['data'])
        filename = file_info.get('filename', 'segmentation_mask.nii.gz')
        
        return send_file(
            file_data,
            mimetype='application/gzip',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error downloading mask: {str(e)}")
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>/download/both', methods=['GET'])
def download_both(patient_id):
    """Download both scan and mask as a ZIP file"""
    try:
        print(f"Creating ZIP for patient {patient_id}...")
        
        scan_info = firebase_service.get_file_from_patient(patient_id, storage_key='scan_data')
        mask_info = firebase_service.get_file_from_patient(patient_id, storage_key='mask_data')
        
        if not scan_info:
            print("Scan file not found")
            return jsonify({'error': 'Scan file not found'}), 404
        if not mask_info:
            print("Mask file not found")
            return jsonify({'error': 'Mask file not found'}), 404
        
        print(f"Scan size: {len(scan_info['data'])} bytes")
        print(f"Mask size: {len(mask_info['data'])} bytes")
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            scan_filename = scan_info.get('filename', 'scan.nii.gz')
            print(f"Adding scan: {scan_filename}")
            zip_file.writestr(scan_filename, scan_info['data'])
            
            mask_filename = mask_info.get('filename', 'mask.nii.gz')
            print(f"Adding mask: {mask_filename}")
            zip_file.writestr(mask_filename, mask_info['data'])
        
        zip_buffer.seek(0)
        zip_size = len(zip_buffer.getvalue())
        print(f"ZIP created successfully: {zip_size} bytes")
        
        patient = firebase_service.get_patient_by_id(patient_id)
        patient_name = patient.get('name', 'patient').replace(' ', '_')
        zip_filename = f"{patient_name}_segmentation_results.zip"
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )
    except Exception as e:
        print(f"Error creating ZIP: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/<patient_id>/download', methods=['GET'])
def download_patient_file(patient_id):
    """Legacy endpoint - downloads scan by default"""
    return download_scan(patient_id)