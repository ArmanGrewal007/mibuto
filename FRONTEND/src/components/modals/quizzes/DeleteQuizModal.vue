<!-- DeleteQuizModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Delete Quiz</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <!-- Subject Dropdown -->
          <div class="form-floating mb-4">
            <select id="subject" v-model="selectedSubjectId" class="form-select" @change="handleSubjectChange">
              <option value="">Select Subject</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
            <label for="subject" class="form-label">
              Select Subject<span class="text-danger">*</span>
            </label>
          </div>

          <!-- Chapter Dropdown -->
          <div class="form-floating mb-4" v-if="selectedSubjectId">
            <select id="chapter" v-model="selectedChapterId" class="form-select" @change="handleChapterChange">
              <option value="">Select Chapter</option>
              <option v-for="chapter in subjectChapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
            <label for="chapter" class="form-label">
              Select Chapter<span class="text-danger">*</span>
            </label>
          </div>

          <!-- Quiz Dropdown -->
          <div class="form-floating mb-4" v-if="selectedChapterId">
            <select id="quiz" v-model="selectedQuizId" class="form-select">
              <option value="">Select Quiz</option>
              <option v-for="quiz in chapterQuizzes" :key="quiz.id" :value="quiz.id">
                {{ quiz.title }}
              </option>
            </select>
            <label for="quiz" class="form-label">
              Select Quiz<span class="text-danger">*</span>
            </label>
          </div>

          <!-- Warning Messages -->
          <div v-if="selectedQuiz" class="alert alert-warning" role="alert">
            <p class="mb-1">
              Are you sure you want to delete the quiz:
              <strong><u>{{ selectedQuiz.title }}</u></strong>?
            </p>
            <p class="mb-1">
              From chapter:
              <strong><u>{{ selectedChapter?.name }}</u></strong>
            </p>
            <p class="mb-1">
              In subject:
              <strong><u>{{ selectedSubject?.name }}</u></strong>
            </p>
            <p class="mb-1">
              Scheduled for:
              <strong><u>{{ formatDateTime(selectedQuiz.date_of_quiz) }}</u></strong>
            </p>
            <p class="mb-0 text-danger">
              <strong>This action is irreversible and will delete all quiz questions and student responses.</strong>
            </p>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button v-if="selectedQuizId" type="button" @click="handleDelete" class="btn btn-danger"
            :disabled="isProcessing">
            {{ isProcessing ? 'Deleting...' : 'Delete Quiz' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop show"></div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'DeleteQuizModal',
  emits: ['close', 'delete'],
  setup(props, { emit }) {
    const store = useStore();
    const selectedSubjectId = ref('');
    const selectedChapterId = ref('');
    const selectedQuizId = ref('');
    const isProcessing = ref(false);

    // Get subjects from store
    const subjects = computed(() => store.getters['subjects/getSubjects']);

    // Get chapters for selected subject
    const subjectChapters = computed(() =>
      selectedSubjectId.value
        ? store.getters['chapters/getChaptersBySubjectId'](selectedSubjectId.value)
        : []
    );

    // Get quizzes for selected chapter
    const chapterQuizzes = computed(() =>
      selectedChapterId.value
        ? store.getters['quizzes/getQuizzesByChapterId'](selectedChapterId.value)
        : []
    );

    // Find the selected entities
    const selectedSubject = computed(() =>
      subjects.value.find(subject => subject.id === selectedSubjectId.value)
    );

    const selectedChapter = computed(() =>
      subjectChapters.value.find(chapter => chapter.id === selectedChapterId.value)
    );

    const selectedQuiz = computed(() =>
      chapterQuizzes.value.find(quiz => quiz.id === selectedQuizId.value)
    );

    onMounted(async () => {
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleSubjectChange = async () => {
      selectedChapterId.value = '';
      selectedQuizId.value = '';
      if (selectedSubjectId.value) {
        await store.dispatch(
          'chapters/fetchChaptersBySubject',
          selectedSubjectId.value
        );
      }
    };

    const handleChapterChange = async () => {
      selectedQuizId.value = '';
      if (selectedChapterId.value) {
        await store.dispatch(
          'quizzes/fetchQuizzesByChapter',
          selectedChapterId.value
        );
      }
    };

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleString('en-US', {
        dateStyle: 'full',
        timeStyle: 'short'
      });
    };

    const handleDelete = async () => {
      if (selectedQuizId.value) {
        isProcessing.value = true;
        try {
          emit('delete', {
            quizId: selectedQuizId.value,
            chapterId: selectedChapterId.value,
            subjectId: selectedSubjectId.value
          });
        } finally {
          isProcessing.value = false;
        }
      }
    };

    return {
      subjects,
      subjectChapters,
      chapterQuizzes,
      selectedSubjectId,
      selectedChapterId,
      selectedQuizId,
      selectedSubject,
      selectedChapter,
      selectedQuiz,
      isProcessing,
      handleSubjectChange,
      handleChapterChange,
      handleDelete,
      formatDateTime
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>