import EventService from '@/services/event_services';

export const subjects = {
  namespaced: true,
  state: {
    subjects: [],
    selectedSubject: null,
  },
  mutations: {
    SET_SUBJECTS(state, subjects) { state.subjects = subjects; },
    SET_SELECTED_SUBJECT(state, subject) { state.selectedSubject = subject; },
    ADD_SUBJECT(state, subject) { state.subjects.push(subject); },
    UPDATE_SUBJECT(state, updatedSubject) {
      const index = state.subjects.findIndex(subject => subject.id === updatedSubject.id);
      if (index !== -1) { state.subjects.splice(index, 1, updatedSubject); }
    },
    DELETE_SUBJECT(state, subjectId) {
      state.subjects = state.subjects.filter(subject => subject.id !== subjectId);
    },
  },
  actions: {
    async fetchSubjects({ commit }) {
      const response = await EventService.getSubjects();
      commit('SET_SUBJECTS', response.data.subjects);
      return response.data;
    },
    async fetchSubjectById({ commit }, subjectId) {
      const response = await EventService.getSubjectsByID(subjectId);
      commit('SET_SELECTED_SUBJECT', response.data.subject);
      return response.data;
    },
    async createSubject({ commit }, subjectData) {
      EventService.addtoken();
      const response = await EventService.createSubject(subjectData);
      commit('ADD_SUBJECT', response.data.subject);
      return response.data;
    },
    async updateSubject({ commit }, { subjectId, updatedData }) {
      EventService.addtoken();
      const response = await EventService.updateSubject(subjectId, updatedData);
      commit('UPDATE_SUBJECT', response.data.subject);
      return response.data;
    },
    async deleteSubject({ commit }, subjectId) {
      EventService.addtoken();
      const response = await EventService.deleteSubject(subjectId);
      commit('DELETE_SUBJECT', subjectId);
      return response.data;
    }
  },
  getters: {
    getSubjects: (state) => [...state.subjects]
      .filter(subject => subject.name)
      .sort((a, b) => a.name.localeCompare(b.name)),
    getSelectedSubject: (state) => state.selectedSubject,
    getSubjectById: (state) => (id) => state.subjects.find(subject => subject.id === id),
  },
};