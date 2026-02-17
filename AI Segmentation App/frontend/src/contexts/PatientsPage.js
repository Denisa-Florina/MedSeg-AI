import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import patientService from '../services/patientService';

export default function PatientsPage() {
  const { doctor } = useAuth();
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [newPatient, setNewPatient] = useState({ name: '', age: '', dicomFile: null });
  const [editPatientId, setEditPatientId] = useState(null);
  const [editPatientData, setEditPatientData] = useState({ name: '', age: '' });
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchPatients();
  }, [doctor]);

  const fetchPatients = async () => {
    if (!doctor) return;
    setLoading(true);
    try {
      const list = await patientService.getPatients(doctor.id);
      setPatients(list);
    } catch (err) {
      setError(err.message || 'Nu s-au putut încărca pacienții');
    } finally {
      setLoading(false);
    }
  };

  const handleAddPatient = async (e) => {
    e.preventDefault();
    if (!newPatient.name || !newPatient.age || !newPatient.dicomFile) return;
    setActionLoading(true);
    try {
      await patientService.createPatient(
        { name: newPatient.name, age: parseInt(newPatient.age) },
        newPatient.dicomFile,
        doctor.id
      );
      setNewPatient({ name: '', age: '', dicomFile: null });
      fetchPatients();
    } catch (err) {
      alert(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleEditPatient = (patient) => {
    setEditPatientId(patient.id);
    setEditPatientData({ name: patient.name, age: patient.age });
  };

  const handleUpdatePatient = async (patientId) => {
    setActionLoading(true);
    try {
      await patientService.updatePatient(patientId, {
        name: editPatientData.name,
        age: parseInt(editPatientData.age),
      });
      setEditPatientId(null);
      fetchPatients();
    } catch (err) {
      alert(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeletePatient = async (patientId) => {
    if (!window.confirm('Sigur vrei să ștergi pacientul?')) return;
    setActionLoading(true);
    try {
      await patientService.deletePatient(patientId);
      fetchPatients();
    } catch (err) {
      alert(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReSegment = async (patientId) => {
    setActionLoading(true);
    try {
      await patientService.reSegmentPatient(patientId);
      fetchPatients();
    } catch (err) {
      alert(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <p className="loading-text">Se încarcă pacienții...</p>;
  if (error) return <p className="error-text">{error}</p>;

  return (
    <div className="patients-container">
      <h1 className="patients-title">Lista pacienților pentru {doctor.name}</h1>

      {/* Add Patient Form */}
      <form className="patient-form" onSubmit={handleAddPatient}>
        <h2 className="form-title">Adaugă pacient nou</h2>
        <div className="form-row">
          <input
            type="text"
            placeholder="Nume"
            className="form-input"
            value={newPatient.name}
            onChange={(e) => setNewPatient({ ...newPatient, name: e.target.value })}
          />
          <input
            type="number"
            placeholder="Vârsta"
            className="form-input-small"
            value={newPatient.age}
            onChange={(e) => setNewPatient({ ...newPatient, age: e.target.value })}
          />
          <input
            type="file"
            accept=".dcm"
            className="form-input-file"
            onChange={(e) => setNewPatient({ ...newPatient, dicomFile: e.target.files[0] })}
          />
          <button type="submit" className="form-button" disabled={actionLoading}>
            Adaugă
          </button>
        </div>
      </form>

      {/* Patients List */}
      <div className="patients-grid">
        {patients.map((p) => (
          <div key={p.id} className="patient-card">
            {editPatientId === p.id ? (
              <div className="edit-section">
                <input
                  type="text"
                  className="patient-input"
                  value={editPatientData.name}
                  onChange={(e) => setEditPatientData({ ...editPatientData, name: e.target.value })}
                />
                <input
                  type="number"
                  className="patient-input"
                  value={editPatientData.age}
                  onChange={(e) => setEditPatientData({ ...editPatientData, age: e.target.value })}
                />
                <div className="patient-actions">
                  <button
                    onClick={() => handleUpdatePatient(p.id)}
                    className="patient-btn save-btn"
                    disabled={actionLoading}
                  >
                    Salvează
                  </button>
                  <button
                    onClick={() => setEditPatientId(null)}
                    className="patient-btn cancel-btn"
                  >
                    Renunță
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <p><strong>Nume:</strong> {p.name}</p>
                <p><strong>Vârsta:</strong> {p.age}</p>
                <p><strong>Data scanării:</strong> {p.date}</p>
                <p><strong>Segmentat:</strong> {p.segmented ? 'Da' : 'Nu'}</p>

                {p.dicom_file && (
                  <div className="relative w-64 h-64 border mt-2">
                    <img
                      src={`http://localhost:5000/uploads/${p.dicom_file}`}
                      alt={p.name}
                      className="w-full h-full object-contain"
                    />
                    {p.dot_position && p.image_shape && (
                      <div
                        className="absolute bg-red-500 rounded-full"
                        style={{
                          width: '8px',
                          height: '8px',
                          top: `${(p.dot_position.y / p.image_shape[0]) * 100}%`,
                          left: `${(p.dot_position.x / p.image_shape[1]) * 100}%`,
                          transform: 'translate(-50%, -50%)'
                        }}
                      />
                    )}
                  </div>
                )}

                <div className="metrics">
                  <p><strong>Dice:</strong> {p.metrics?.dice_score}</p>
                  <p><strong>IOU:</strong> {p.metrics?.iou_score}</p>
                  <p><strong>Confidence:</strong> {p.metrics?.confidence}</p>
                </div>

                <div className="patient-actions">
                  <button
                    onClick={() => handleEditPatient(p)}
                    className="patient-btn edit-btn"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeletePatient(p.id)}
                    className="patient-btn delete-btn"
                  >
                    Delete
                  </button>
                  <button
                    onClick={() => handleReSegment(p.id)}
                    className="patient-btn resegment-btn"
                  >
                    Re-segment
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
