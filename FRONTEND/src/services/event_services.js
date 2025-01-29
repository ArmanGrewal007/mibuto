// event_services.js is a service file that contains all the API calls 
// related to the event module.
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5001',
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  timeout: 10000
})

export default {
  // add JWT token to the header
  addtoken() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      console.log('apiclient header token added', apiClient.defaults.headers.common['Authorization']);
    }
  },
  postUserSignup(credentials) { return apiClient.post('/user-signup', credentials) },
  postUserLogin(credentials) { return apiClient.post('/user-login', credentials) },
  postAdminLogin(credentials) { return apiClient.post('/admin-login', credentials) },
  // Subject APIs
  createSubject(data) { return apiClient.post('/create-subject', data) },
  getSubjects() { return apiClient.get('/get-subject'); },
  getSubjectByID(subjectID) { return apiClient.get(`/get-subject?subject_id=${subjectID}`); },
  updateSubject(subjectID, data) { return apiClient.patch(`/update-subject/${subjectID}`, { ...data }); },
  deleteSubject(subjectID) { return apiClient.delete(`/delete-subject/${subjectID}`); },
  // Chapter APIs
  createChapter(data) { return apiClient.post('/create-chapter', data) },
  getChapters() { return apiClient.get('/get-chapter') },
  getChapterByID(chapterID) { return apiClient.get(`/get-chapter?chapter_id=${chapterID}`) },
  getChaptersBySubject(subjectID) { return apiClient.get(`/get-chapter?subject_id=${subjectID}`) },
  updateChapter(chapterID, data) { return apiClient.patch(`/update-chapter/${chapterID}`, { ...data }) },
  deleteChapter(chapterID) { return apiClient.delete(`/delete-chapter/${chapterID}`) },
}