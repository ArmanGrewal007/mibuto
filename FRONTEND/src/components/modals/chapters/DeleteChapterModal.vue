<!-- DeleteChapterModal.vue -->
<template>
  <div class="modal show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content modal-custom">
        <div class="text-center modal-header">
          <h5 class="modal-title">Delete Chapter</h5>
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
            <select id="chapter" v-model="selectedChapterId" class="form-select">
              <option value="">Select Chapter</option>
              <option v-for="chapter in subjectChapters" :key="chapter.id" :value="chapter.id">
                {{ chapter.name }}
              </option>
            </select>
            <label for="chapter" class="form-label">
              Select Chapter<span class="text-danger">*</span>
            </label>
          </div>

          <!-- Warning Message -->
          <div v-if="selectedChapter" class="alert alert-warning" role="alert">
            <p class="mb-1">
              Are you sure you want to delete the chapter: 
              <strong><u>{{ selectedChapter.name }}</u></strong>?
            </p>
            <p class="mb-1">
              From subject: 
              <strong><u>{{ selectedSubject?.name }}</u></strong>
            </p>
            <p class="mb-0">
              This action is irreversible and will delete all associated quizzes.
            </p>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">
            Cancel
          </button>
          <button v-if="selectedChapterId" type="button" @click="handleDelete" class="btn btn-danger">
            Delete Chapter
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
  name: 'DeleteChapterModal',
  emits: ['close', 'delete'],
  setup(props, { emit }) {
    const store = useStore();
    const selectedSubjectId = ref('');
    const selectedChapterId = ref('');

    // Get subjects from store
    const subjects = computed(() => store.getters['subjects/getSubjects']);
    
    // Get chapters for selected subject
    const subjectChapters = computed(() => 
      selectedSubjectId.value 
        ? store.getters['chapters/getChaptersBySubjectId'](selectedSubjectId.value)
        : []
    );

    // Find the selected subject object
    const selectedSubject = computed(() => 
      subjects.value.find(subject => subject.id === selectedSubjectId.value)
    );

    // Find the selected chapter object
    const selectedChapter = computed(() => 
      subjectChapters.value.find(chapter => chapter.id === selectedChapterId.value)
    );

    onMounted(async () => {
      await store.dispatch('subjects/fetchSubjects');
    });

    const handleSubjectChange = async () => {
      selectedChapterId.value = '';
      if (selectedSubjectId.value) {
        await store.dispatch(
          'chapters/fetchChaptersBySubject', 
          selectedSubjectId.value
        );
      }
    };

    const handleDelete = () => {
      if (selectedChapterId.value) {
        emit('delete', {
          chapterId: selectedChapterId.value,
          subjectId: selectedSubjectId.value
        });
      }
    };

    return {
      subjects,
      subjectChapters,
      selectedSubjectId,
      selectedChapterId,
      selectedSubject,
      selectedChapter,
      handleSubjectChange,
      handleDelete
    };
  }
};
</script>

<style src="@/components/modals/modalStyle.css" scoped></style>