<!-- UpdateChapterModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Update Chapter</h5>
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

              <!-- Chapter Name -->
              <div class="form-floating col-md-12">
                <input id="chapter-name" v-model="formData.name" placeholder="" class="form-control"
                  :disabled="!selectedChapterId" />
                <label for="chapter-name" class="form-label">
                  Name
                  <span class="text-danger">*</span>
                </label>
              </div>

              <!-- Description -->
              <div class="form-floating col-md-12">
                <textarea id="description" v-model="formData.description" placeholder="" class="form-control"
                  :disabled="!selectedChapterId" minlength="10"></textarea>
                <label for="description" class="form-label">
                  Description
                  <span class="text-danger">*</span>
                </label>
              </div>
            </div>
          </form>
          <div class="mt-3 small text-white text-end">
            <em><span class="text-danger">*</span> These fields are required</em>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="randomizeFields" class="btn btn-info" :disabled="!selectedChapterId">
            Randomize Fields
          </button>
          <button type="button" @click="resetToOriginal" class="btn btn-secondary" :disabled="!selectedChapterId">
            Reset
          </button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" @click="handleSubmit" class="btn btn-primary"
            :disabled="!isFormValid || !selectedChapterId">
            Update Chapter
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
  name: 'UpdateChapterModal',
  emits: ['close', 'update'],
  setup(props, { emit }) {
    const store = useStore();
    const selectedSubjectId = ref('');
    const selectedChapterId = ref('');
    const originalData = ref(null);
    const formData = ref({
      name: '',
      description: '',
      subject_id: ''
    });

    // Get subjects from Vuex store
    const subjects = computed(() => store.getters['subjects/getSubjects']);

    // Get chapters for selected subject
    const subjectChapters = computed(() =>
      selectedSubjectId.value
        ? store.getters['chapters/getChaptersBySubjectId'](selectedSubjectId.value)
        : []
    );

    const isFormValid = computed(() => {
      return formData.value.name.trim().length >= 3 &&
        formData.value.description.trim().length >= 5;
    });

    const chapterTypes = [
      'Introduction to', 'Fundamentals of', 'Advanced',
      'Basic Concepts in', 'Applications of', 'Principles of'
    ];

    onMounted(async () => {
      // Load subjects on mount
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleSubjectSelect = async () => {
      selectedChapterId.value = '';
      formData.value = { name: '', description: '', subject_id: '' };
      originalData.value = null;

      if (selectedSubjectId.value) {
        // Load chapters for selected subject
        await store.dispatch(
          'chapters/fetchChaptersBySubject',
          selectedSubjectId.value
        );
      }
    };

    const handleChapterSelect = async () => {
      if (selectedChapterId.value) {
        const response = await store.dispatch(
          'chapters/fetchChapterById',
          selectedChapterId.value
        );
        originalData.value = { ...response.data };
        formData.value = { ...response.data };
      } else {
        formData.value = { name: '', description: '', subject_id: '' };
        originalData.value = null;
      }
    };

    const randomizeFields = () => {
      formData.value = {
        ...formData.value,
        name: faker.helpers.arrayElement(chapterTypes) + ' ' +
          faker.science.chemicalElement().name,
        description: `This chapter covers ${faker.science.unit().name} and its ` +
          `relationship with ${faker.science.unit().symbol}.`
      };
    };

    const resetToOriginal = () => {
      if (originalData.value) {
        formData.value = { ...originalData.value };
      }
    };

    const handleSubmit = () => {
      if (selectedChapterId.value) {
        emit('update', {
          chapterId: selectedChapterId.value,
          updatedData: {
            name: formData.value.name,
            description: formData.value.description,
            subject_id: selectedSubjectId.value
          }
        });
      }
    };

    return {
      subjects,
      subjectChapters,
      selectedSubjectId,
      selectedChapterId,
      formData,
      randomizeFields,
      resetToOriginal,
      handleSubmit,
      isFormValid,
      handleSubjectSelect,
      handleChapterSelect
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>