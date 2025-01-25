import EventService from "@/services/event_services";

export const user_auth = {
  namespaced: true,
  
  state: {
    user: null,
    username: '',
    user_email: '',
    isAdmin: false
  },

  mutations: {
    LOGIN_DATA(state, userData) {
      state.user = userData.user;
      const loggedInAsAdmin = userData.loggedInAsAdmin || false;
      state.isAdmin = loggedInAsAdmin && userData.user?.roles.includes('Admin');
      
      localStorage.setItem('username', JSON.stringify(userData.user?.username));
      localStorage.setItem('user_email', JSON.stringify(userData.user?.email));
      localStorage.setItem('isAdmin', JSON.stringify(state.isAdmin));
      localStorage.setItem('token', userData.token);
      EventService.addtoken();
    },
    
    CLEAR_USER_DATA(state) {
      state.user = null;
      state.isAdmin = false;
      state.username = '';
      state.user_email = '';
      
      localStorage.removeItem('username');
      localStorage.removeItem('user_email');
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
    userEmail: state => state.user?.email || ''
  }
};