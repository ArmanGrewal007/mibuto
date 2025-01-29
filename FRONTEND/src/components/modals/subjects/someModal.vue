<!-- DeleteSubjectModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Delete Subject</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="handleDelete">
            <div class="row g-3">
              <!-- Subject Selection -->
              <div class="form-floating col-md-12">
                <select id="subject-select" v-model="selectedSubjectId" class="form-select">
                  <option value="">Select a subject to delete</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
                <label for="subject-select" class="form-label">Select Subject
                  <span class="text-danger">*</span>
                </label>
              </div>
            </div>
          </form>
          <div class="mt-3 text-white">
            <em class="text-danger">
              Warning: Deleting a subject is permanent and cannot be undone.
            </em>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" @click="handleDelete" class="btn btn-danger" :disabled="!selectedSubjectId">
            Delete Subject
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
  name: 'DeleteSubject',
  emits: ['close', 'delete'],
  setup(props, { emit }) {
    const store = useStore();
    const selectedSubjectId = ref('');
    const subjects = computed(() => store.getters['subjects/getSubjects']);

    onMounted(async () => {
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleDelete = () => {
      if (selectedSubjectId.value) {
        emit('delete', { subjectId: selectedSubjectId.value });
      }
    };

    return {
      subjects,
      selectedSubjectId,
      handleDelete
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>
