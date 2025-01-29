<!-- CreateChapterModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Create New Chapter</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row g-3">
              <!-- Subject Selection -->
              <div class="form-floating col-md-12">
                <select  id="subject-select"  v-model="formData.subject_id"  class="form-select"
                  :class="{ 'is-invalid': !formData.subject_id && showValidation }">
                  <option value="">Select a subject</option>
                  <option  v-for="subject in subjects"  :key="subject.id"  :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
                <label for="subject-select" class="form-label">Subject <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!formData.subject_id && showValidation">
                  Please select a subject
                </div>
              </div>

              <!-- Chapter Name -->
              <div class="form-floating col-md-12">
                <input id="chapter-name" v-model="formData.name" placeholder="" class="form-control"
                  :class="{ 'is-invalid': !formData.name && showValidation }"/>
                <label for="chapter-name" class="form-label">Name <span class="text-danger">*</span></label>
                <div class="invalid-feedback" v-if="!formData.name && showValidation">
                  Chapter name is required
                </div>
              </div>

              <!-- Description -->
              <div class="form-floating col-md-12">
                <textarea id="description" v-model="formData.description" placeholder="" class="form-control" style="height: 100px"></textarea>
                <label for="description" class="form-label">Description</label>
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
            Create Chapter
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
  name: 'CreateChapterModal',
  emits: ['close', 'submit'],
  setup(props, { emit }) {
    const store = useStore();
    const showValidation = ref(false);

    const formData = ref({
      name: '',
      description: '',
      subject_id: ''
    });

    // Get subjects from Vuex store
    const subjects = computed(() => store.getters['subjects/getSubjects']);

    // Fetch subjects when component mounts
    onMounted(async () => {
      if (subjects.value.length === 0) {
        await store.dispatch('subjects/fetchSubjects');
      }
    });

    const chapterTypes = [
      'Introduction to', 'Fundamentals of', 'Advanced', 
      'Basic Concepts in', 'Applications of', 'Principles of'
    ];

    const isFormValid = computed(() => {
      return formData.value.name.trim().length >= 3 && 
              formData.value.subject_id !== '';
    });

    const randomizeFields = () => {
      if (subjects.value.length > 0) {
        const randomSubject = faker.helpers.arrayElement(subjects.value);
        formData.value = {
          subject_id: randomSubject.id,
          name: faker.helpers.arrayElement(chapterTypes) + ' ' + 
                faker.science.chemicalElement().name,
          description: `This chapter covers ${faker.science.unit().name} and its ` +
                      `relationship with ${faker.science.unit().symbol}.`
        };
      }
    };

    const clearFields = () => {
      formData.value = { 
        name: '', 
        description: '', 
        subject_id: '' 
      };
      showValidation.value = false;
    };

    const handleSubmit = () => {
      showValidation.value = true;
      if (isFormValid.value) {
        emit('submit', { ...formData.value });
      }
    };

    return {
      formData,
      subjects,
      randomizeFields,
      clearFields,
      handleSubmit,
      isFormValid,
      showValidation
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>