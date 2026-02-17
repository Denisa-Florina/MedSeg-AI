import React from 'react';
import { Plus, Search, User } from 'lucide-react';

function PatientsView({ patients, searchTerm, setSearchTerm, onViewPatient, onAddPatient, loading }) {
  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Se încarcă pacienții...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Pacienți</h2>
          <p className="text-gray-400">Gestionează toți pacienții</p>
        </div>
        <button
          onClick={onAddPatient}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition font-medium"
        >
          <Plus className="w-5 h-5" />
          Adaugă Pacient
        </button>
      </div>

      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Caută pacient..."
            className="w-full bg-gray-800 text-white pl-12 pr-4 py-3 rounded-lg border border-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
        </div>
      </div>

      {patients.length === 0 ? (
        <div className="text-center py-12">
          <User className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 text-lg">Nu există pacienți</p>
          <button
            onClick={onAddPatient}
            className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
          >
            Adaugă primul pacient
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {patients.map(patient => (
            <div
              key={patient.id}
              onClick={() => onViewPatient(patient)}
              className="bg-gray-800 border border-gray-700 rounded-xl p-6 hover:border-blue-500 transition cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                    <User className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white">{patient.name}</h3>
                    <p className="text-sm text-gray-400">{patient.age} ani</p>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  patient.status === 'completed' 
                    ? 'bg-green-600/20 text-green-400' 
                    : 'bg-yellow-600/20 text-yellow-400'
                }`}>
                  {patient.status === 'completed' ? 'Completat' : 'Processing'}
                </span>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Data:</span>
                  <span className="text-white">{patient.date}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Confidence:</span>
                  <span className="text-white">{((patient.confidence || 0) * 100).toFixed(1)}%</span>
                </div>
                {patient.dicomFile && (
                  <div className="flex justify-between">
                    <span className="text-gray-400">Fișier:</span>
                    <span className="text-white text-xs truncate max-w-[150px]">{patient.dicomFile}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PatientsView;