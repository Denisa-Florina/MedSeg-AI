import React from 'react';
import { Activity, BarChart3, Users, Settings, LogOut, User } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

function Sidebar({ activeView, setActiveView, setShowSettings }) {
  const { doctor, logout } = useAuth();

  return (
    <aside className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col">
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">MedSeg AI</h1>
            <p className="text-xs text-gray-400">Medical Imaging</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        <button
          onClick={() => setActiveView('dashboard')}
          className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
            activeView === 'dashboard' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
          }`}
        >
          <BarChart3 className="w-5 h-5" />
          <span className="font-medium">Dashboard</span>
        </button>

        <button
          onClick={() => setActiveView('patients')}
          className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
            activeView === 'patients' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'
          }`}
        >
          <Users className="w-5 h-5" />
          <span className="font-medium">Pacienți</span>
        </button>

        <button
          onClick={() => setShowSettings(true)}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-700 transition"
        >
          <Settings className="w-5 h-5" />
          <span className="font-medium">Setări</span>
        </button>
      </nav>

      <div className="p-4 border-t border-gray-700">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <User className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">{doctor.name}</p>
            <p className="text-xs text-gray-400 truncate">{doctor.specialization}</p>
          </div>
        </div>
        <button 
          onClick={logout}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-sm font-medium">Deconectare</span>
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;