<!-- CreateSubjectModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Create New Subject</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row g-3">
              <!-- Subject Name -->
              <div class="form-floating col-md-12">
                <input id="subject-name" v-model="formData.name" placeholder="" class="form-control" />
                <label for="subject-name" class="form-label">Name
                  <span class="text-danger">*</span>
                </label>
              </div>
              <!-- Description -->
              <div class="form-floating col-md-12">
                <textarea id="description" v-model="formData.description" placeholder=""
                  class="form-control"></textarea>
                <label for="description" class="form-label">Description
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
            Create Subject
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop show"></div>
</template>

<script>
import { ref, computed } from 'vue';
import { faker } from '@faker-js/faker';

export default {
  name: 'CreateSubjectModal',
  emits: ['close', 'submit'],
  setup(props, { emit }) {
    const formData = ref({
      name: '',
      description: ''
    });

    // More realistic subject generator
    const academicSubjects = [
      'Mathematics', 'Physics', 'Chemistry',
      'Biology', 'Computer Science', 'Literature',
      'History', 'Art', 'Economics'
    ];

    const isFormValid = computed(() => {
      return formData.value.name.trim().length >= 3 &&
        formData.value.description.trim().length >= 20;
    });

    const randomizeFields = () => {
      formData.value = {
        name: faker.helpers.arrayElement(academicSubjects) + '-' +
          faker.number.int({ min: 100, max: 400 }),
        description: `Study of ${faker.science.chemicalElement().name} and ` +
                      `${faker.science.unit().name}. `
      };
    };

    const clearFields = () => {
      formData.value = { name: '', description: '' };
    };

    const handleSubmit = () => {
      emit('submit', { ...formData.value });
    };

    return {
      formData,
      randomizeFields,
      clearFields,
      handleSubmit,
      isFormValid
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>