<!-- UpdateQuizModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Update Quiz</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row g-3">
              <!-- Subject Selection -->
              <div class="form-floating col-md-12">
                <select id="subject-select" v-model="selectedSubjectId" class="form-select"
                  @change="handleSubjectSelect">
                  <option value="">Select Subject</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
                <label for="subject-select" class="form-label">
                  Select Subject<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Chapter Selection -->
              <div class="form-floating col-md-12">
                <select id="chapter-select" v-model="selectedChapterId" class="form-select"
                  :disabled="!selectedSubjectId" @change="handleChapterSelect">
                  <option value="">Select Chapter</option>
                  <option v-for="chapter in subjectChapters" :key="chapter.id" :value="chapter.id">
                    {{ chapter.name }}
                  </option>
                </select>
                <label for="chapter-select" class="form-label">
                  Select Chapter<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Quiz Selection -->
              <div class="form-floating col-md-12">
                <select id="quiz-select" v-model="selectedQuizId" class="form-select" :disabled="!selectedChapterId"
                  @change="handleQuizSelect">
                  <option value="">Select Quiz</option>
                  <option v-for="quiz in chapterQuizzes" :key="quiz.id" :value="quiz.id">
                    {{ quiz.title }}
                  </option>
                </select>
                <label for="quiz-select" class="form-label">
                  Select Quiz<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Quiz Title -->
              <div class="form-floating col-md-12">
                <input id="quiz-title" v-model="formData.title" placeholder="" class="form-control"
                  :disabled="!selectedQuizId" />
                <label for="quiz-title" class="form-label">
                  New Title<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Time Duration -->
              <div class="form-floating col-md-6">
                <input type="number" id="time-duration" v-model="formData.time_duration" placeholder=""
                  class="form-control" :disabled="!selectedQuizId" min="1" />
                <label for="time-duration" class="form-label">
                  Time Duration (minutes)<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Date of Quiz -->
              <div class="form-floating col-md-6">
                <input type="datetime-local" id="date-of-quiz" v-model="formData.date_of_quiz" placeholder=""
                  class="form-control" :disabled="!selectedQuizId" />
                <label for="date-of-quiz" class="form-label">
                  Date of Quiz<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Remarks -->
              <div class="form-floating col-md-12">
                <textarea id="remarks" v-model="formData.remarks" placeholder="" class="form-control"
                  :disabled="!selectedQuizId" minlength="5"></textarea>
                <label for="remarks" class="form-label">
                  New Remarks<span class="text-danger">*</span>
                </label>
              </div>
            </div>
          </form>
          <div class="mt-3 small text-white text-end">
            <em><span class="text-danger">*</span> These fields are required</em>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="randomizeFields" class="btn btn-info" :disabled="!selectedQuizId">
            Randomize Fields
          </button>
          <button type="button" @click="resetToOriginal" class="btn btn-secondary" :disabled="!selectedQuizId">
            Reset
          </button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" @click="handleSubmit" class="btn btn-primary"
            :disabled="!isFormValid || !selectedQuizId">
            Update Quiz
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
import { faker } from '@faker-js/faker';

export default {
  name: 'UpdateQuizModal',
  emits: ['close', 'update'],
  setup(props, { emit }) {
    const store = useStore();
    const selectedSubjectId = ref('');
    const selectedChapterId = ref('');
    const selectedQuizId = ref('');
    const originalData = ref(null);
    const formData = ref({
      title: '',
      time_duration: '',
      date_of_quiz: '',
      remarks: '',
      chapter_id: ''
    });

    // Get subjects from Vuex store
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

    const isFormValid = computed(() => {
      return formData?.value?.title?.trim()?.length >= 3 &&
        formData?.value?.time_duration > 0 &&
        formData?.value?.date_of_quiz &&
        formData?.value?.remarks?.trim()?.length >= 5;
    });

    const quizTitles = [
      'Weekly Assessment', 'Chapter Test', 'Pop Quiz',
      'Final Exam', 'Practice Test', 'Review Quiz'
    ];

    onMounted(async () => {
      // Load subjects on mount
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleSubjectSelect = async () => {
      selectedChapterId.value = '';
      selectedQuizId.value = '';
      formData.value = { title: '', time_duration: '', date_of_quiz: '', remarks: '', chapter_id: '' };
      originalData.value = null;

      if (selectedSubjectId.value) {
        await store.dispatch('chapters/fetchChaptersBySubject', selectedSubjectId.value);
      }
    };

    const handleChapterSelect = async () => {
      selectedQuizId.value = '';
      formData.value = { title: '', time_duration: '', date_of_quiz: '', remarks: '', chapter_id: '' };
      originalData.value = null;

      if (selectedChapterId.value) {
        await store.dispatch('quizzes/fetchQuizzesByChapter', selectedChapterId.value);
      }
    };

    const handleQuizSelect = async () => {
      if (selectedQuizId.value) {
        const response = await store.dispatch('quizzes/fetchQuizById', selectedQuizId.value);
        originalData.value = { ...response.data };
        formData.value = { ...response.data };
      } else {
        formData.value = { title: '', time_duration: '', date_of_quiz: '', remarks: '', chapter_id: '' };
        originalData.value = null;
      }
    };

    const randomizeFields = () => {
      const futureDate = new Date();
      futureDate.setDate(futureDate.getDate() + Math.floor(Math.random() * 30));

      formData.value = {
        ...formData.value,
        title: faker.helpers.arrayElement(quizTitles),
        time_duration: Math.floor(Math.random() * 90) + 30,
        date_of_quiz: futureDate.toISOString().slice(0, 16),
        remarks: `This quiz covers ${faker.science.unit().name} and tests understanding of ${faker.science.unit().symbol}.`
      };
    };

    const resetToOriginal = () => {
      if (originalData.value) {
        formData.value = { ...originalData.value };
      }
    };

    const handleSubmit = () => {
      if (selectedQuizId.value) {
        emit('update', {
          id: selectedQuizId.value,
          updatedData: {
            title: formData.value.title,
            time_duration: formData.value.time_duration,
            date_of_quiz: formData.value.date_of_quiz,
            remarks: formData.value.remarks,
            chapter_id: selectedChapterId.value
          }
        });
      }
    };

    return {
      subjects,
      subjectChapters,
      chapterQuizzes,
      selectedSubjectId,
      selectedChapterId,
      selectedQuizId,
      formData,
      randomizeFields,
      resetToOriginal,
      handleSubmit,
      isFormValid,
      handleSubjectSelect,
      handleChapterSelect,
      handleQuizSelect
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>