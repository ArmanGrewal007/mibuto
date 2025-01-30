<!-- UpdateSubjectModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Update Subject</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row g-3">
              <!-- Subject Selection -->
              <div class="form-floating col-md-12">
                <select id="subject-select" v-model="selectedSubjectId" class="form-select"
                  @change="handleSubjectSelect">
                  <option value="">...</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
                <label for="subject-select" class="form-label">Select Subject
                  <span class="text-danger">*</span>
                </label>
              </div>

              <!-- Subject Name -->
              <div class="form-floating col-md-12">
                <input id="subject-name" v-model="formData.name" placeholder="" class="form-control"
                  :disabled="!selectedSubjectId" pattern="^.+-\d+$" />
                <label for="subject-name" class="form-label">
                  New Name (format: text-number)<span class="text-danger">*</span>
                </label>
              </div>

              <!-- Description -->
              <div class="form-floating col-md-12">
                <textarea id="description" v-model="formData.description" placeholder="" class="form-control"
                  :disabled="!selectedSubjectId" minlength="10"></textarea>
                <label for="description" class="form-label">
                  New Description<span class="text-danger">*</span>
                </label>
              </div>
            </div>
          </form>
          <div class="mt-3 small text-white text-end">
            <em><span class="text-danger">*</span> These fields are required</em>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="randomizeFields" class="btn btn-info" :disabled="!selectedSubjectId">
            Randomize Fields
          </button>
          <button type="button" @click="resetToOriginal" class="btn btn-secondary" :disabled="!selectedSubjectId">
            Clear
          </button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" @click="handleSubmit" class="btn btn-primary"
            :disabled="!isFormValid || !selectedSubjectId">
            Update Subject
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
  name: 'UpdateSubjectModal',
  emits: ['close', 'update'],
  setup(props, { emit }) {
    const store = useStore();
    const selectedSubjectId = ref('');
    const originalData = ref(null);
    const formData = ref({
      name: '',
      description: ''
    });

    const subjects = computed(() => store.getters['subjects/getSubjects']);

    const isFormValid = computed(() => {
      return formData?.value?.name?.trim().length >= 3 &&
        formData?.value?.description?.trim().length >= 5;
    });

    const academicSubjects = [
      'Mathematics', 'Physics', 'Chemistry',
      'Biology', 'Computer Science', 'Literature',
      'History', 'Art', 'Economics'
    ];

    onMounted(async () => {
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleSubjectSelect = async () => {
      if (selectedSubjectId.value) {
        const subject = await store.dispatch(
          'subjects/fetchSubjectById',
          selectedSubjectId.value
        );
        originalData.value = { ...subject.subject };
        formData.value = { ...subject.subject };
      } else {
        formData.value = { name: '', description: '' };
        originalData.value = null;
      }
    };

    const randomizeFields = () => {
      formData.value = {
        ...formData.value,
        name: faker.helpers.arrayElement(academicSubjects) + '-' +
          faker.number.int({ min: 100, max: 400 }),
        description: `Study of ${faker.science.chemicalElement().name} and ` +
          `${faker.science.unit().name}. `
      };
    };

    const resetToOriginal = () => {
      if (originalData.value) {
        formData.value = { ...originalData.value };
      }
    };

    const handleSubmit = () => {
      if (selectedSubjectId.value) {
        emit('update', {
          subjectId: selectedSubjectId.value,
          updatedData: {
            name: formData.value.name,
            description: formData.value.description
          }
        });
      }
    };

    return {
      subjects,
      selectedSubjectId,
      formData,
      randomizeFields,
      resetToOriginal,
      handleSubmit,
      isFormValid,
      handleSubjectSelect
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>