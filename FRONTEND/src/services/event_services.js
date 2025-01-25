// event_services.js is a service file that contains all the API calls 
// related to the event module.
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  withCredentials: false,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
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
}