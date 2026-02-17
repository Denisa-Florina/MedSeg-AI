import React, { useState } from 'react';
import { User, Upload, FileText, CheckCircle, ArrowLeft, Download } from 'lucide-react';
import patientService from '../../services/patientService';

function PatientProfile({ patient, onBack, onUpdate }) {
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [downloading, setDownloading] = useState(false);

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    setUploading(true);
    setUploadResult(null);

    try {
      const result = await patientService.uploadDicom(patient.id, files);
      setUploadResult(result);
      onUpdate();
    } catch (err) {
      alert('Eroare la încărcare: ' + err.message);
    } finally {
      setUploading(false);
      patient.status = 'completed';
    }
  };

  const handleDownloadScan = async () => {
    setDownloading(true);
    try {
      await patientService.downloadScan(patient.id);
    } catch (error) {
      alert('Eroare la descărcarea scan-ului: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  const handleDownloadMask = async () => {
    setDownloading(true);
    try {
      await patientService.downloadMask(patient.id);
    } catch (error) {
      alert('Eroare la descărcarea segmentării: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  const handleDownloadBoth = async () => {
    setDownloading(true);
    try {
      await patientService.downloadBoth(patient.id);
    } catch (error) {
      alert('Eroare la descărcarea fișierelor: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="p-8">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition"
      >
        <ArrowLeft className="w-5 h-5" />
        Înapoi la pacienți
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
            <div className="text-center mb-6">
              <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <User className="w-12 h-12 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-1">{patient.name}</h2>
              <p className="text-gray-400">{patient.age} ani</p>
            </div>

            <div className="space-y-3 border-t border-gray-700 pt-6">
              <div className="flex justify-between">
                <span className="text-gray-400">ID Pacient:</span>
                <span className="text-white font-medium">#{patient.id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Data scanării:</span>
                <span className="text-white font-medium">{patient.date}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Status:</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  patient.status === 'completed' 
                    ? 'bg-green-600/20 text-green-400' 
                    : 'bg-yellow-600/20 text-yellow-400'
                }`}>
                  {patient.status === 'completed' ? 'Completat' : 'In procesare'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Confidence:</span>
                <span className="text-white font-medium">
                  {((patient.confidence || 0) * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>
        </div>


        <div className="lg:col-span-2 space-y-6">
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
            <h3 className="text-xl font-bold text-white mb-4">
              Încarcă fișiere DICOM pentru predicție
            </h3>
            
            <label className="block">
              <div className="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-blue-500 transition cursor-pointer">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-white font-medium mb-2">
                  {uploading ? 'Se procesează...' : 'Click pentru a încărca fișier DICOM'}
                </p>
                <p className="text-sm text-gray-400">Formatul acceptat: .dcm</p>
                <input
                  type="file"
                  accept=".dcm" multiple
                  onChange={handleFileUpload}
                  disabled={uploading}
                  className="hidden"
                />
              </div>
            </label>

            {uploading && (
              <div className="mt-4 bg-blue-600/20 border border-blue-500 rounded-lg p-4">
                <div className="flex items-center gap-3">
                  <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                  <span className="text-blue-400">Se procesează segmentarea...</span>
                </div>
              </div>
            )}

            {uploadResult && (
              <div className="mt-4 bg-green-600/20 border border-green-500 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-2">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-green-400 font-medium">Segmentare completă!</span>
                </div>
                <p className="text-sm text-gray-300">
                  Confidence: {((uploadResult.confidence || 0) * 100).toFixed(1)}%
                </p>
              </div>
            )}
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
            <h3 className="text-xl font-bold text-white mb-4">Rezultate Segmentare</h3>
            
            <div className="bg-gray-700/50 rounded-lg p-4 mb-4">
              <div className="aspect-video bg-gray-900 rounded-lg flex items-center justify-center">
                <FileText className="w-16 h-16 text-gray-600" />
              </div>
              <p className="text-sm text-gray-400 mt-2 text-center">
                Vizualizare rezultate segmentare
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-700/50 rounded-lg p-4">
                <p className="text-sm text-gray-400 mb-1">Confidence Score</p>
                <p className="text-2xl font-bold text-white">
                  {((patient.confidence || 0) * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-gray-700/50 rounded-lg p-4">
                <p className="text-sm text-gray-400 mb-1">Fișier</p>
                <p className="text-sm font-medium text-white truncate">
                  {patient.filename || 'N/A'}
                </p>
                {patient.file_size && (
                  <p className="text-xs text-gray-400 mt-1">
                    Size: {(patient.file_size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                )}
              </div>
            </div>

            {patient.status === 'completed' && (
              <div className="space-y-3">
                <h4 className="text-sm font-semibold text-gray-400 mb-3">Descarcă Rezultate:</h4>
                
                <button
                  onClick={handleDownloadScan}
                  disabled={downloading}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition font-medium"
                >
                  <Download className="w-5 h-5" />
                  {downloading ? 'Se descarcă...' : 'Descarcă CT Scan (.nii.gz)'}
                </button>

                <button
                  onClick={handleDownloadMask}
                  disabled={downloading}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white rounded-lg transition font-medium"
                >
                  <Download className="w-5 h-5" />
                  {downloading ? 'Se descarcă...' : 'Descarcă Segmentare (.nii.gz)'}
                </button>

                <button
                  onClick={handleDownloadBoth}
                  disabled={downloading}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-black rounded-lg transition font-medium"
                >
                  <Download className="w-5 h-5" />
                  {downloading ? 'Se descarcă...' : 'Descarcă Ambele (ZIP)'}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PatientProfile;