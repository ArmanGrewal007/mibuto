<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Create New Quiz</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row g-3">
              <!-- Subject Selection -->
              <div class="form-floating col-md-12">
                <select id="subject-select" v-model="selectedSubject" class="form-select"
                  :class="{ 'is-invalid': !selectedSubject && showValidation }" @change="handleSubjectChange">
                  <option value="">Select a subject</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
                <label for="subject-select" class="form-label">Subject <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!selectedSubject && showValidation">
                  Please select a subject
                </div>
              </div>

              <!-- Chapter Selection -->
              <div class="form-floating col-md-12">
                <select id="chapter-select" v-model="formData.chapter_id" class="form-select"
                  :class="{ 'is-invalid': !formData.chapter_id && showValidation }" :disabled="!selectedSubject">
                  <option value="">Select a chapter</option>
                  <option v-for="chapter in chaptersForSubject" :key="chapter.id" :value="chapter.id">
                    {{ chapter.name }}
                  </option>
                </select>
                <label for="chapter-select" class="form-label">Chapter <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!formData.chapter_id && showValidation">
                  Please select a chapter
                </div>
              </div>

              <!-- Quiz Title -->
              <div class="form-floating col-md-12">
                <input id="quiz-title" v-model="formData.title" placeholder="" class="form-control"
                  :class="{ 'is-invalid': !formData.title && showValidation }" />
                <label for="quiz-title" class="form-label">Title <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!formData.title && showValidation">
                  Quiz title is required
                </div>
              </div>

              <!-- Quiz Date -->
              <div class="form-floating col-md-6">
                <input type="datetime-local" id="quiz-date" v-model="formData.date_of_quiz" class="form-control"
                  :class="{ 'is-invalid': !formData.date_of_quiz && showValidation }" />
                <label for="quiz-date" class="form-label">Date & Time <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!formData.date_of_quiz && showValidation">
                  Quiz date and time is required
                </div>
              </div>

              <!-- Duration -->
              <div class="form-floating col-md-6">
                <input type="number" id="duration" v-model="formData.time_duration" class="form-control"
                  :class="{ 'is-invalid': !formData.time_duration && showValidation }" min="1" />
                <label for="duration" class="form-label">Duration (minutes) <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!formData.time_duration && showValidation">
                  Quiz duration is required
                </div>
              </div>

              <!-- Remarks -->
              <div class="form-floating col-md-12">
                <textarea id="remarks" v-model="formData.remarks" placeholder="" class="form-control"
                  style="height: 100px"></textarea>
                <label for="remarks" class="form-label">Remarks</label>
              </div>
            </div>
          </form>
          <div class="mt-3 small text-white text-end">
            <em><span class="text-danger">*</span> These fields are required</em>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="randomizeFields" class="btn btn-info">
            Randomize Fields
          </button>
          <button type="button" @click="clearFields" class="btn btn-secondary">
            Clear
          </button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" @click="handleSubmit" class="btn btn-success" :disabled="!isFormValid">
            Create Quiz
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
  name: 'CreateQuizModal',
  emits: ['close', 'submit'],
  setup(props, { emit }) {
    const store = useStore();
    const showValidation = ref(false);
    const selectedSubject = ref('');

    const formData = ref({
      title: '',
      chapter_id: '',
      date_of_quiz: '',
      time_duration: '',
      remarks: ''
    });

    // Get subjects and chapters from Vuex store
    const subjects = computed(() => store.getters['subjects/getSubjects']);
    const chaptersForSubject = computed(() =>
      store.getters['chapters/getChaptersBySubjectId'](selectedSubject.value) || []
    );

    // Fetch subjects when component mounts
    onMounted(async () => {
      if (subjects.value.length === 0) {
        await store.dispatch('subjects/fetchSubjects');
      }
    });

    // Watch for subject change to fetch chapters
    const handleSubjectChange = async () => {
      if (selectedSubject.value) {
        await store.dispatch('chapters/fetchChaptersBySubject', selectedSubject.value);
        formData.value.chapter_id = ''; // Reset chapter selection
      }
    };

    const quizTypes = [
      'Mid-term Quiz', 'Final Assessment', 'Chapter Test',
      'Practice Quiz', 'Review Test', 'Evaluation'
    ];

    const isFormValid = computed(() => {
      return formData.value.title.trim().length > 0 &&
        formData.value.chapter_id !== '' &&
        formData.value.date_of_quiz !== '' &&
        formData.value.time_duration > 0;
    });

    const randomizeFields = () => {
      if (subjects.value.length > 0) {
        // Set random subject
        selectedSubject.value = faker.helpers.arrayElement(subjects.value).id;

        // Wait for chapters to load then set random chapter
        handleSubjectChange().then(() => {
          if (chaptersForSubject.value.length > 0) {
            const randomChapter = faker.helpers.arrayElement(chaptersForSubject.value);

            // Set form data with random values
            formData.value = {
              chapter_id: randomChapter.id,
              title: faker.helpers.arrayElement(quizTypes) + ' - ' + randomChapter.name,
              date_of_quiz: new Date(Date.now() + faker.number.int({ min: 86400000, max: 604800000 }))
                .toISOString().slice(0, 16),
              time_duration: faker.number.int({ min: 15, max: 120 }),
              remarks: `This quiz covers ${faker.lorem.sentence()}`
            };
          }
        });
      }
    };

    const clearFields = () => {
      selectedSubject.value = '';
      formData.value = {
        title: '',
        chapter_id: '',
        date_of_quiz: '',
        time_duration: '',
        remarks: ''
      };
      showValidation.value = false;
    };

    const handleSubmit = () => {
      showValidation.value = true;
      if (isFormValid.value) {
        // Convert time_duration from minutes to seconds
        const submitData = {
          ...formData.value,
          time_duration: parseInt(formData.value.time_duration) * 60
        };
        emit('submit', submitData);
      }
    };

    return {
      formData,
      subjects,
      selectedSubject,
      chaptersForSubject,
      randomizeFields,
      clearFields,
      handleSubmit,
      handleSubjectChange,
      isFormValid,
      showValidation
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>