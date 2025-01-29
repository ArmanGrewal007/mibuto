import EventService from '@/services/event_services';

export const chapters = {
  namespaced: true,
  state: {
    chapters: [],
    selectedChapter: null,
    chaptersBySubject: {},  // Organize chapters by subject_id for efficient lookup
  },
  mutations: {
    SET_CHAPTERS(state, chapters) {  state.chapters = chapters; },
    SET_SELECTED_CHAPTER(state, chapter) {  state.selectedChapter = chapter;},
    SET_CHAPTERS_BY_SUBJECT(state, { subjectId, chapters }) {
      state.chaptersBySubject = {
        ...state.chaptersBySubject,
        [subjectId]: chapters
      };
    },
    ADD_CHAPTER(state, chapter) { 
      state.chapters.push(chapter);
      // Update chapters by subject
      const subjectChapters = state.chaptersBySubject[chapter.subject_id] || [];
      state.chaptersBySubject[chapter.subject_id] = [...subjectChapters, chapter];
    },
    UPDATE_CHAPTER(state, updatedChapter) {
      // Update in main chapters array
      const index = state.chapters.findIndex(chapter => chapter.id === updatedChapter.id);
      if (index !== -1) { 
        state.chapters.splice(index, 1, updatedChapter); 
      }
      
      // Update in chaptersBySubject
      if (state.chaptersBySubject[updatedChapter.subject_id]) {
        const subjectIndex = state.chaptersBySubject[updatedChapter.subject_id]
          .findIndex(chapter => chapter.id === updatedChapter.id);
        if (subjectIndex !== -1) {
          state.chaptersBySubject[updatedChapter.subject_id].splice(subjectIndex, 1, updatedChapter);
        }
      }
    },
    DELETE_CHAPTER(state, { chapterId, subjectId }) {
      // Remove from main chapters array
      state.chapters = state.chapters.filter(chapter => chapter.id !== chapterId);
      
      // Remove from chaptersBySubject
      if (state.chaptersBySubject[subjectId]) {
        state.chaptersBySubject[subjectId] = state.chaptersBySubject[subjectId]
          .filter(chapter => chapter.id !== chapterId);
      }
      
      // Clear selectedChapter if it was deleted
      if (state.selectedChapter && state.selectedChapter.id === chapterId) {
        state.selectedChapter = null;
      }
    },
  },
  actions: {
    async fetchChapters({ commit }) {
      const response = await EventService.getChapters();
      commit('SET_CHAPTERS', response.data.data);
      return response.data;
    },
    async fetchChapterById({ commit }, chapterId) {
      const response = await EventService.getChapterByID(chapterId);
      commit('SET_SELECTED_CHAPTER', response.data.data);
      return response.data;
    },
    async fetchChaptersBySubject({ commit }, subjectId) {
      const response = await EventService.getChaptersBySubject(subjectId);
      commit('SET_CHAPTERS_BY_SUBJECT', { 
        subjectId, 
        chapters: response.data.data 
      });
      return response.data;
    },
    async createChapter({ commit }, chapterData) {
      EventService.addtoken();
      const response = await EventService.createChapter(chapterData);
      commit('ADD_CHAPTER', response.data.data);
      return response.data;
    },
    async updateChapter({ commit }, { chapterId, updatedData }) {
      EventService.addtoken();
      const response = await EventService.updateChapter(chapterId, updatedData);
      commit('UPDATE_CHAPTER', response.data.data);
      return response.data;
    },
    async deleteChapter({ commit }, { chapterId, subjectId }) {
      EventService.addtoken();
      const response = await EventService.deleteChapter(chapterId);
      commit('DELETE_CHAPTER', { chapterId, subjectId });
      return response.data;
    }
  },
  getters: {
    getChapters: (state) => [...state.chapters]
      .filter(chapter => chapter.name)
      .sort((a, b) => a.name.localeCompare(b.name)),
    getSelectedChapter: (state) => state.selectedChapter,
    getChapterById: (state) => (id) => state.chapters.find(chapter => chapter.id === id),
    getChaptersBySubjectId: (state) => (subjectId) => 
      state.chaptersBySubject[subjectId] 
        ? [...state.chaptersBySubject[subjectId]].sort((a, b) => a.name.localeCompare(b.name))
        : [],
    getChapterCount: (state) => (subjectId) => state.chaptersBySubject[subjectId]?.length || 0,
  },
};