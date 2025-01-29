import EventService from "@/services/event_services";

export const user_auth = {
  namespaced: true,

  state: {
    user: JSON.parse(localStorage.getItem('user')) || null,
    username: localStorage.getItem('username') ? JSON.parse(localStorage.getItem('username')) : '',
    isAdmin: localStorage.getItem('isAdmin') ? JSON.parse(localStorage.getItem('isAdmin')) : false
  },

  mutations: {
    LOGIN_DATA(state, userData) {
      state.user = userData.user;
      const loggedInAsAdmin = userData.loggedInAsAdmin || false;
      state.isAdmin = loggedInAsAdmin && userData.user?.roles.includes('Admin');

      localStorage.setItem('user', JSON.stringify(userData.user));
      localStorage.setItem('username', JSON.stringify(userData.user?.username));
      localStorage.setItem('full_name', JSON.stringify(userData.user?.full_name));
      localStorage.setItem('qualification', JSON.stringify(userData.user?.qualification));
      localStorage.setItem('isAdmin', JSON.stringify(state.isAdmin));
      localStorage.setItem('token', userData.token);
      EventService.addtoken();
    },

    CLEAR_USER_DATA(state) {
      state.user = null;
      state.isAdmin = false;
      state.username = '';

      localStorage.removeItem('user');
      localStorage.removeItem('username');
      localStorage.removeItem('full_name');
      localStorage.removeItem('qualification');
      localStorage.removeItem('user');
      localStorage.removeItem('token');
      localStorage.removeItem('isAdmin');
    },

    SET_USER(state, userData) {
      state.user = userData;
    }
  },

  actions: {
    async login({ commit }, credentials) {
      const response = await EventService.postUserLogin(credentials);
      if (response.status < 400) {
        commit('LOGIN_DATA', response.data);
        return response;
      }
    },

    async signup({ commit }, credentials) {
      const response = await EventService.postUserSignup(credentials);
      if (response.status < 400) {
        commit('LOGIN_DATA', response.data);
        return response;
      }
    },

    async admin_login({ commit }, credentials) {
      const response = await EventService.postAdminLogin(credentials);
      if (response.status < 400) {
        commit('LOGIN_DATA', { ...response.data, loggedInAsAdmin: true });
        return response;
      }
    },

    logout({ commit }) {
      commit('CLEAR_USER_DATA');
    },

    async fetchUser({ commit }, { id }) {
      const response = await EventService.getUser(id);
      if (response.status < 400) {
        commit('SET_USER', response.data);
        return response;
      }
    }
  },

  getters: {
    isLoggedIn: state => !!state.user || state.isAdmin,
    isAdmin: state => state.isAdmin,
    username: state => state.user?.username || '',
    fullName: state => state.user?.full_name || '',
    qualification: state => state.user?.qualification || ''
  }
};