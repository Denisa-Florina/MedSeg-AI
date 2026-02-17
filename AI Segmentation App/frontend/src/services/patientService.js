import api from './api';

export const patientService = {
  async getPatients(doctorId) {
    const response = await api.get(`/patients?doctor_id=${doctorId}`);
    return response.data.patients;
  },

  async getPatient(patientId) {
    const response = await api.get(`/patients/${patientId}`);
    return response.data.patient;
  },

  async createPatient(patientData, dicomFiles, doctorId) {
    const formData = new FormData();
    formData.append('name', patientData.name);
    formData.append('age', patientData.age);

    console.log("Doctor ID:", doctorId);
    console.log("Name:", patientData.name);
    console.log("Age:", patientData.age);

    formData.append('doctor_id', doctorId);
    if (dicomFiles && dicomFiles.length > 0) {
      dicomFiles.forEach(element => {
        formData.append('dicom_file', element);
      });
    }

    for (let pair of formData.entries()) {
      console.log( 'formData: ' + pair[0] + ': ' + pair[1]);
    }

    const response = await api.post('/patients/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data.patient;
  },

  async updatePatient(patientId, updates) {
    const response = await api.put(`/patients/${patientId}`, updates);
    return response.data.patient;
  },

  async deletePatient(patientId) {
    await api.delete(`/patients/${patientId}`);
  },

  async uploadDicom(patientId, dicomFiles) {
    const formData = new FormData();
    
    if (dicomFiles && dicomFiles.length > 0) {
      dicomFiles.forEach(file => {
        formData.append('dicom_file', file);
      });
    }

    const response = await api.post(`/patients/${patientId}/upload-dicom`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data.result;
  },

  async reSegmentPatient(patientId) {
    const response = await api.post(`/patients/${patientId}/re-segment`);
    return response.data.patient;
  },

  // ===== DOWNLOAD FUNCTIONS =====
  
  async downloadScan(patientId) {
    try {
      const response = await api.get(`/patients/${patientId}/download/scan`, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from headers if available
      const contentDisposition = response.headers['content-disposition'];
      let filename = `scan_${patientId}.nii.gz`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return { success: true };
    } catch (error) {
      console.error('Error downloading scan:', error);
      throw error;
    }
  },

  async downloadMask(patientId) {
    try {
      const response = await api.get(`/patients/${patientId}/download/mask`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const contentDisposition = response.headers['content-disposition'];
      let filename = `segmentation_${patientId}.nii.gz`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return { success: true };
    } catch (error) {
      console.error('Error downloading mask:', error);
      throw error;
    }
  },

  async downloadBoth(patientId) {
    try {
      const response = await api.get(`/patients/${patientId}/download/both`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const contentDisposition = response.headers['content-disposition'];
      let filename = `results_${patientId}.zip`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return { success: true };
    } catch (error) {
      console.error('Error downloading files:', error);
      throw error;
    }
  }
};

export default patientService;