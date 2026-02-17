import React from 'react';
import { Users, CheckCircle, BarChart3, Clock, TrendingUp, User } from 'lucide-react';

function DashboardView({ stats, patients, onViewPatient, loading }) {
  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Se încarcă...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Dashboard</h2>
        <p className="text-gray-400">Prezentare generală activitate medicală</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center">
              <Users className="w-6 h-6 text-blue-400" />
            </div>
            <TrendingUp className="w-5 h-5 text-green-400" />
          </div>
          <p className="text-gray-400 text-sm mb-1">Total Pacienți</p>
          <p className="text-3xl font-bold text-white">{stats.totalPatients}</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-green-600/20 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-400" />
            </div>
          </div>
          <p className="text-gray-400 text-sm mb-1">Segmentări Complete</p>
          <p className="text-3xl font-bold text-white">{stats.completed}</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-purple-600/20 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-purple-400" />
            </div>
          </div>
          <p className="text-gray-400 text-sm mb-1">Confidence Medie</p>
          <p className="text-3xl font-bold text-white">{stats.avgConfidence}%</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-orange-600/20 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-orange-400" />
            </div>
          </div>
          <p className="text-gray-400 text-sm mb-1">Luna Curentă</p>
          <p className="text-3xl font-bold text-white">{stats.thisMonth}</p>
        </div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
        <h3 className="text-xl font-bold text-white mb-4">Pacienți Recenți</h3>
        {patients.length === 0 ? (
          <p className="text-gray-400 text-center py-8">Nu există pacienți încă</p>
        ) : (
          <div className="space-y-3">
            {patients.slice(0, 5).map(patient => (
              <div
                key={patient.id}
                onClick={() => onViewPatient(patient)}
                className="flex items-center justify-between p-4 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="font-medium text-white">{patient.name}</p>
                    <p className="text-sm text-gray-400">{patient.age} ani • {patient.date}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                    patient.status === 'completed' 
                      ? 'bg-green-600/20 text-green-400' 
                      : 'bg-yellow-600/20 text-yellow-400'
                  }`}>
                    {patient.status === 'completed' ? 'Completat' : 'In procesare'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default DashboardView;