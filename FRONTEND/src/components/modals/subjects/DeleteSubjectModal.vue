<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Delete Subject</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <!-- Subject Dropdown -->
          <div class="form-floating mb-4">
            <select id="subject" v-model="selectedSubjectId" class="form-select">
              <option value="">...</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
            <label for="subject" class="form-label">Select Subject<span class="text-danger">*</span></label>
          </div>

          <div v-if="selectedSubjectId" class="alert alert-warning" role="alert">
            Are you sure you want to delete the subject: <strong><u>{{ selectedSubject?.name }}</u></strong>?<br>
            This action is irreversible and will delete all associated chapters, and any quizzes contained within those
            chapters.
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button v-if="selectedSubjectId" type="button" @click="handleDelete" class="btn btn-danger">
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

    // Find the selected subject object
    const selectedSubject = computed(() =>
      subjects.value.find(subject => subject.id === selectedSubjectId.value)
    );

    onMounted(async () => {
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleDelete = () => {
      if (selectedSubjectId.value) {
        emit('delete', selectedSubjectId.value);
      }
    };

    return {
      subjects,
      selectedSubjectId,
      selectedSubject,
      handleDelete
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>