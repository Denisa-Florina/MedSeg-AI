import React, { useState } from 'react';
import { X, Save } from 'lucide-react';

function SettingsView({ doctor, onClose }) {
  const [formData, setFormData] = useState({
    name: doctor.name,
    email: doctor.email,
    specialization: doctor.specialization,
    hospital: doctor.hospital
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = () => {
    // TODO: Implement save functionality
    alert('Funcționalitate în dezvoltare');
  };

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Setări</h2>
          <p className="text-gray-400">Configurează contul și preferințele</p>
        </div>
        <button 
          onClick={onClose} 
          className="text-gray-400 hover:text-white transition"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      <div className="max-w-2xl space-y-6">
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <h3 className="text-lg font-bold text-white mb-4">Informații Profil</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Nume</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Specializare</label>
              <input
                type="text"
                name="specialization"
                value={formData.specialization}
                onChange={handleChange}
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Spital</label>
              <input
                type="text"
                name="hospital"
                value={formData.hospital}
                onChange={handleChange}
                className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
              />
            </div>
          </div>
          <button 
            onClick={handleSave}
            className="mt-4 flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
          >
            <Save className="w-4 h-4" />
            Salvează modificări
          </button>
        </div>
        
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <h3 className="text-lg font-bold text-white mb-4">Securitate</h3>
          <button className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition">
            Schimbă parola
          </button>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
          <h3 className="text-lg font-bold text-white mb-4">Notificări</h3>
          <div className="space-y-3">
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-gray-300">Email pentru pacienți noi</span>
              <input type="checkbox" className="w-5 h-5" defaultChecked />
            </label>
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-gray-300">Email pentru segmentări complete</span>
              <input type="checkbox" className="w-5 h-5" defaultChecked />
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SettingsView;