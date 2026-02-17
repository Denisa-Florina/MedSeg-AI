import api from './api';

export const authService = {
  async login(email, password) {
    const response = await api.post('/auth/login', { email, password });

    localStorage.setItem('doctor', JSON.stringify(response.data.doctor));

    return response.data.doctor;
  },

  async logout() {
    await api.post('/auth/logout');
    localStorage.removeItem('doctor');
  },

  async getCurrentDoctor() {
    const doctor = localStorage.getItem('doctor');
    if (doctor) return JSON.parse(doctor);
    return null;
  }
};

export default authService;
