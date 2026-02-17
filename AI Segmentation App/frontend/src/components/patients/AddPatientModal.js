import React, { useState } from 'react';
import { X, Upload } from 'lucide-react';
import patientService from '../../services/patientService';

function AddPatientModal({doctorId, onClose, onSuccess }) {
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [dicomFiles, setDicomFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !age) {
      setError('Numele și vârsta sunt obligatorii');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      await patientService.createPatient(
        { name, age: parseInt(age) },
        dicomFiles, 
        doctorId
      );
      onSuccess();
    } catch (err) {
      console.error('Error adding patient:', err);
      setError(err.message || 'Eroare la adăugare pacient');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-800 rounded-2xl p-6 w-full max-w-md border border-gray-700">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold text-white">Adaugă Pacient Nou</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Nume <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
              placeholder="Nume complet"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Vârstă <span className="text-red-400">*</span>
            </label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
              placeholder="Vârstă"
              min="1"
              max="150"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Fișier DICOM <span className="text-gray-500">(opțional)</span>
            </label>
            <label className="block border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-blue-500 transition cursor-pointer">
              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-300">
                {dicomFiles.length ? dicomFiles.length + 'fișiere încărcate' : 'Click pentru a încărca (opțional)'}
              </p>
              <input
                type="file"
                accept=".dcm" multiple
                onChange={(e) => setDicomFiles(Array.from(e.target.files))}
                className="hidden"
              />
            </label>
          </div>

          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-200 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
            >
              Anulează
            </button>
            <button
              type="submit"
              disabled={loading || !name || !age}
              className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Se adaugă...' : 'Adaugă'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddPatientModal;