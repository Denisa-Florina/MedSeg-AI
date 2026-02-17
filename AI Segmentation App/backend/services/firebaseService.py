import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
import hashlib
import base64
import json
from io import BytesIO


service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
if service_account_json:
    cred_dict = json.loads(service_account_json)
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate('backend/serviceAccountKey.json')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


class FirebaseService:
    
    @staticmethod
    def get_doctor_by_email(email):
        """Get doctor by email from Firestore"""
        try:
            docs = db.collection('doctors').where('email', '==', email).limit(1).stream()
            for doc in docs:
                return {'id': doc.id, **doc.to_dict()}
            return None
        except Exception as e:
            print(f"Error getting doctor: {e}")
            return None
    
    @staticmethod
    def get_doctor_by_id(doctor_id):
        """Get doctor by ID from Firestore"""
        try:
            doc = db.collection('doctors').document(doctor_id).get()
            if doc.exists:
                return {'id': doc.id, **doc.to_dict()}
            return None
        except Exception as e:
            print(f"Error getting doctor: {e}")
            return None
    
    @staticmethod
    def create_doctor(doctor_data):
        """Create a new doctor in Firestore"""
        try:
            if 'password' in doctor_data:
                doctor_data['password'] = hashlib.sha256(
                    doctor_data['password'].encode()
                ).hexdigest()
            
            doctor_data['created_at'] = datetime.now()
            doc_ref = db.collection('doctors').document()
            doc_ref.set(doctor_data)
            return {'id': doc_ref.id, **doctor_data}
        except Exception as e:
            print(f"Error creating doctor: {e}")
            return None
    
    @staticmethod
    def update_doctor(doctor_id, updates):
        """Update doctor in Firestore"""
        try:
            updates['updated_at'] = datetime.now()
            db.collection('doctors').document(doctor_id).update(updates)
            return FirebaseService.get_doctor_by_id(doctor_id)
        except Exception as e:
            print(f"Error updating doctor: {e}")
            return None
    
    @staticmethod
    def add_patient(patient_data):
        """Add a new patient to Firestore"""
        try:
            patient_data['created_at'] = datetime.now()
            patient_data['updated_at'] = datetime.now()
            
            doc_ref = db.collection('patients').document()
            doc_ref.set(patient_data)
            
            return {'id': doc_ref.id, **patient_data}
        except Exception as e:
            print(f"Error adding patient: {e}")
            return None
    
    @staticmethod
    def get_patients_by_doctor(doctor_id):
        """Get all patients for a specific doctor (without file data to reduce size)"""
        try:
            patients = []
            docs = db.collection('patients').where('doctor_id', '==', str(doctor_id)).stream()
            
            for doc in docs:
                patient_data = doc.to_dict()

                if 'file_data' in patient_data: patient_data.pop('file_data')
                if 'scan_data' in patient_data: patient_data.pop('scan_data')
                if 'mask_data' in patient_data: patient_data.pop('mask_data')
                
                if 'created_at' in patient_data:
                    patient_data['created_at'] = patient_data['created_at'].isoformat() if hasattr(patient_data['created_at'], 'isoformat') else str(patient_data['created_at'])
                if 'updated_at' in patient_data:
                    patient_data['updated_at'] = patient_data['updated_at'].isoformat() if hasattr(patient_data['updated_at'], 'isoformat') else str(patient_data['updated_at'])
                
                patients.append({'id': doc.id, **patient_data})
            
            return patients
        except Exception as e:
            print(f"Error getting patients: {e}")
            return []
    
    @staticmethod
    def get_patient_by_id(patient_id, include_file=False):
        """Get a specific patient by ID"""
        try:
            doc = db.collection('patients').document(patient_id).get()
            if doc.exists:
                patient_data = doc.to_dict()
                
                if not include_file:
                    if 'file_data' in patient_data: patient_data.pop('file_data')
                    if 'scan_data' in patient_data: patient_data.pop('scan_data')
                    if 'mask_data' in patient_data: patient_data.pop('mask_data')
                
                if 'created_at' in patient_data:
                    patient_data['created_at'] = patient_data['created_at'].isoformat() if hasattr(patient_data['created_at'], 'isoformat') else str(patient_data['created_at'])
                if 'updated_at' in patient_data:
                    patient_data['updated_at'] = patient_data['updated_at'].isoformat() if hasattr(patient_data['updated_at'], 'isoformat') else str(patient_data['updated_at'])
                
                return {'id': doc.id, **patient_data}
            return None
        except Exception as e:
            print(f"Error getting patient: {e}")
            return None
    
    @staticmethod
    def update_patient(patient_id, updates):
        """Update patient in Firestore"""
        try:
            updates['updated_at'] = datetime.now()
            db.collection('patients').document(patient_id).update(updates)
            return FirebaseService.get_patient_by_id(patient_id)
        except Exception as e:
            print(f"Error updating patient: {e}")
            return None
    
    @staticmethod
    def delete_patient(patient_id):
        """Delete patient from Firestore"""
        try:
            db.collection('patients').document(patient_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False
    
    @staticmethod
    def save_file_to_patient(patient_id, file_data, filename, storage_key='file_data'):
        """
        Save file as base64 in patient document.
        Args:
            storage_key: 'scan_data' for original file, 'mask_data' for result
        """
        try:
            # Prepare data stream for reading
            file_data.seek(0)
            file_bytes = file_data.read()
            file_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
            file_size = len(file_bytes)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"Saving {storage_key} ({file_size_mb:.2f} MB)...")
            
            if file_size_mb > 0.5: 
                return FirebaseService._save_large_file(patient_id, file_base64, filename, file_size, storage_key)
            
            updates = {
                storage_key: file_base64,
                f'{storage_key}_filename': filename,
                f'{storage_key}_size': file_size,
                'updated_at': datetime.now()
            }
            
            db.collection('patients').document(patient_id).update(updates)
            return True
            
        except Exception as e:
            print(f"Error saving file for {storage_key}: {e}")
            return False
    
    @staticmethod
    def _save_large_file(patient_id, file_base64, filename, file_size, storage_key):
        """Save large files by splitting into chunks in a subcollection"""
        try:
            chunk_size = 800 * 1024 
            chunks = [file_base64[i:i+chunk_size] for i in range(0, len(file_base64), chunk_size)]
            
            chunks_ref = db.collection('patients').document(patient_id).collection(f'{storage_key}_chunks')
            
            old_chunks = chunks_ref.stream()
            for chunk in old_chunks:
                chunk.reference.delete()
            
            for i, chunk_data in enumerate(chunks):
                chunks_ref.document(f'chunk_{i}').set({
                    'data': chunk_data,
                    'order': i,
                    'created_at': datetime.now()
                })
            
            updates = {
                f'{storage_key}_filename': filename,
                f'{storage_key}_size': file_size,
                f'{storage_key}_chunks_count': len(chunks),
                f'{storage_key}_is_chunked': True,
                'updated_at': datetime.now()
            }
            
            db.collection('patients').document(patient_id).update(updates)
            return True
            
        except Exception as e:
            print(f"Error saving large file for {storage_key}: {e}")
            return False
    
    @staticmethod
    def get_file_from_patient(patient_id, storage_key='file_data'):
        """Retrieve file data from patient document"""
        try:
            patient = FirebaseService.get_patient_by_id(patient_id, include_file=True)
            if not patient: return None
            
            if patient.get(f'{storage_key}_is_chunked', False):
                return FirebaseService._get_large_file(patient_id, patient.get(f'{storage_key}_chunks_count', 0), storage_key)
            
            if storage_key in patient:
                file_bytes = base64.b64decode(patient[storage_key])
                return {
                    'data': file_bytes,
                    'filename': patient.get(f'{storage_key}_filename', 'file.nii.gz'),
                    'size': patient.get(f'{storage_key}_size', 0),
                    'storage_key': storage_key
                }
            return None
        except Exception as e:
            print(f"Error getting file for {storage_key}: {e}")
            return None
    
    @staticmethod
    def _get_large_file(patient_id, chunks_count, storage_key):
        try:
            chunks_ref = db.collection('patients').document(patient_id).collection(f'{storage_key}_chunks')
            chunks = chunks_ref.order_by('order').stream()
            
            file_base64 = ''
            for chunk in chunks:
                chunk_data = chunk.to_dict()
                if 'data' in chunk_data:
                    file_base64 += chunk_data['data']
            
            file_bytes = base64.b64decode(file_base64)
            patient = FirebaseService.get_patient_by_id(patient_id, include_file=False)
            
            return {
                'data': file_bytes,
                'filename': patient.get(f'{storage_key}_filename', 'file.nii.gz'),
                'size': patient.get(f'{storage_key}_size', 0),
                'storage_key': storage_key
            }
        except Exception as e:
            print(f"Error getting large file for {storage_key}: {e}")
            return None

firebase_service = FirebaseService()