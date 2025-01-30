import EventService from '@/services/event_services';

export const quizzes = {
  namespaced: true,
  state: {
    quizzes: [],
    selectedQuiz: null,
    quizzesByChapter: {},  // Organize quizzes by chapter_id for efficient lookup
  },
  mutations: {
    SET_QUIZZES(state, quizzes) {state.quizzes = quizzes;},
    SET_SELECTED_QUIZ(state, quiz) {state.selectedQuiz = quiz;},
    SET_QUIZZES_BY_CHAPTER(state, { chapterId, quizzes }) {
      state.quizzesByChapter = {
        ...state.quizzesByChapter,
        [chapterId]: quizzes
      };
    },
    ADD_QUIZ(state, quiz) {
      state.quizzes.push(quiz);
      // Update quizzes by chapter
      const chapterQuizzes = state.quizzesByChapter[quiz.chapter_id] || [];
      state.quizzesByChapter[quiz.chapter_id] = [...chapterQuizzes, quiz];
    },
    UPDATE_QUIZ(state, updatedQuiz) {
      // Update in main quizzes array
      const index = state.quizzes.findIndex(quiz => quiz.id === updatedQuiz.id);
      if (index !== -1) {
        state.quizzes.splice(index, 1, updatedQuiz);
      }

      // Update in quizzesByChapter
      if (state.quizzesByChapter[updatedQuiz.chapter_id]) {
        const chapterIndex = state.quizzesByChapter[updatedQuiz.chapter_id]
          .findIndex(quiz => quiz.id === updatedQuiz.id);
        if (chapterIndex !== -1) {
          state.quizzesByChapter[updatedQuiz.chapter_id].splice(chapterIndex, 1, updatedQuiz);
        }
      }
    },
    DELETE_QUIZ(state, { quizId, chapterId }) {
      // Remove from main quizzes array
      state.quizzes = state.quizzes.filter(quiz => quiz.id !== quizId);

      // Remove from quizzesByChapter
      if (state.quizzesByChapter[chapterId]) {
        state.quizzesByChapter[chapterId] = state.quizzesByChapter[chapterId]
          .filter(quiz => quiz.id !== quizId);
      }

      // Clear selectedQuiz if it was deleted
      if (state.selectedQuiz && state.selectedQuiz.id === quizId) {
        state.selectedQuiz = null;
      }
    },
  },
  actions: {
    async fetchQuizzes({ commit }) {
      const response = await EventService.getQuizzes();
      commit('SET_QUIZZES', response.data.data);
      return response.data;
    },
    async fetchQuizById({ commit }, quizId) {
      const response = await EventService.getQuizByID(quizId);
      commit('SET_SELECTED_QUIZ', response.data.data);
      return response.data;
    },
    async fetchQuizzesByChapter({ commit }, chapterId) {
      const response = await EventService.getQuizzesByChapter(chapterId);
      commit('SET_QUIZZES_BY_CHAPTER', {chapterId, quizzes: response.data.data});
      return response.data;
    },
    async createQuiz({ commit }, quizData) {
      EventService.addtoken();
      const response = await EventService.createQuiz(quizData);
      commit('ADD_QUIZ', response.data.data);
      return response.data;
    },
    async updateQuiz({ commit }, updatedData) {
      EventService.addtoken();
      const response = await EventService.updateQuiz(updatedData);
      commit('UPDATE_QUIZ', response.data.data);
      return response.data;
    },
    async deleteQuiz({ commit }, { quizId, chapterId }) {
      EventService.addtoken();
      const response = await EventService.deleteQuiz(quizId);
      commit('DELETE_QUIZ', { quizId, chapterId });
      return response.data;
    }
  },
  getters: {
    getQuizzes: (state) => [...state.quizzes]
      .filter(quiz => quiz.title)
      .sort((a, b) => a.title.localeCompare(b.title)),
    getSelectedQuiz: (state) => state.selectedQuiz,
    getQuizById: (state) => (id) => state.quizzes.find(quiz => quiz.id === id),
    getQuizzesByChapterId: (state) => (chapterId) =>
      state.quizzesByChapter[chapterId]
        ? [...state.quizzesByChapter[chapterId]].sort((a, b) => a.title.localeCompare(b.title))
        : [],
    getQuizCount: (state) => (chapterId) => state.quizzesByChapter[chapterId]?.length || 0,
  }
};