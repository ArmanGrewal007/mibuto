<!-- NavBar.vue -->
<template>
  <div>
    <!-- Modals -->
    <CreateSubjectModal v-if="createSubjectModal" @close="createSubjectModal = false" @submit="handleCreateSubject" />
    <UpdateSubjectModal v-if="updateSubjectModal" @close="updateSubjectModal = false" @update="handleUpdateSubject" />
    <DeleteSubjectModal v-if="deleteSubjectModal" @close="deleteSubjectModal = false" @delete="handleDeleteSubject" />
    <CreateChapterModal v-if="createChapterModal" @close="createChapterModal = false" @submit="handleCreateChapter" />
    <UpdateChapterModal v-if="updateChapterModal" @close="updateChapterModal = false" @update="handleUpdateChapter" />
    <DeleteChapterModal v-if="deleteChapterModal" @close="deleteChapterModal = false" @delete="handleDeleteChapter" />
    <CreateQuizModal v-if="createQuizModal" @close="createQuizModal = false" @submit="handleCreateQuiz" />
    <UpdateQuizModal v-if="updateQuizModal" @close="updateQuizModal = false" @update="handleUpdateQuiz" />
    <DeleteQuizModal v-if="deleteQuizModal" @close="deleteQuizModal = false" @delete="handleDeleteQuiz" />

    <!-- Toast Notifications -->
    <ToastNotification ref="toastComponent" />
    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'sidebar-open': isSidebarOpen }">
      <!-- <div class="sidebar-header">
        <h5 class="mb-0">Menu</h5>
        <button class="btn-close" @click="toggleSidebar"></button>
      </div> -->
      <div class="sidebar-content">
        <div v-if="isLoggedIn">
          <div class="sidebar-header">
            <h5 class="mb-0 text-capitalize">
              Hi {{ username }}!
              <span v-if="isAdmin" class="text-danger">(admin)</span>
            </h5>
            <button class="btn-close" @click="toggleSidebar"></button>
          </div>
          <div class="sidebar-menu">
            <!-- Admin Sections -->
            <div v-if="isAdmin">
              <router-link to="/admin-dashboard" class="sidebar-item" @click="toggleSidebar">
                <i class="fas fa-dashboard"></i> Admin Dashboard
              </router-link>

              <!-- Subject Management Section -->
              <div class="sidebar-section">
                <div class="sidebar-section-title px-3 py-2 bg-light" @click="toggleSubjectManagement">
                  <small class="text-muted text-uppercase fw-bold">Subject Management </small>
                  <i :class="['fas', showSubjectManagement ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  <!-- Toggle icon -->
                </div>
                <div v-if="showSubjectManagement"> <!-- Show buttons only if showSubjectManagement is true -->
                  <a href="#" class="sidebar-item" @click.prevent="openModal('createSubject')">
                    <i class="fas fa-plus-circle"></i> Create Subject
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('updateSubject')">
                    <i class="fas fa-edit"></i> Update Subject
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('deleteSubject')">
                    <i class="fas fa-trash"></i> Delete Subject
                  </a>
                </div>
              </div>

              <!-- Chapter Management Section -->
              <div class="sidebar-section">
                <div class="sidebar-section-title px-3 py-2 bg-light" @click="toggleChapterManagement">
                  <small class="text-muted text-uppercase fw-bold">Chapter Management </small>
                  <i :class="['fas', showChapterManagement ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  <!-- Toggle icon -->
                </div>
                <div v-if="showChapterManagement"> <!-- Chapter buttons only if showChapterManagement is true -->
                  <a href="#" class="sidebar-item" @click.prevent="openModal('createChapter')">
                    <i class="fas fa-plus-circle"></i> Create Chapter
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('updateChapter')">
                    <i class="fas fa-edit"></i> Update Chapter
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('deleteChapter')">
                    <i class="fas fa-trash"></i> Delete Chapter
                  </a>
                </div>
              </div>

              <!-- Quiz Management Section -->
              <div class="sidebar-section">
                <div class="sidebar-section-title px-3 py-2 bg-light" @click="toggleQuizManagement">
                  <small class="text-muted text-uppercase fw-bold">Quiz Management </small>
                  <i :class="['fas', showQuizManagement ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  <!-- Toggle icon -->
                </div>
                <div v-if="showQuizManagement"> <!-- Quiz buttons only if showQuizManagement is true -->
                  <a href="#" class="sidebar-item" @click.prevent="openModal('createQuiz')">
                    <i class="fas fa-plus-circle"></i> Create Quiz
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('updateQuiz')">
                    <i class="fas fa-edit"></i> Update Quiz
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('deleteQuiz')">
                    <i class="fas fa-trash"></i> Delete Quiz
                  </a>
                </div>
              </div>
            </div>

            <a href="/" @click.prevent="logout" class="sidebar-item text-danger mt-3 border-top">
              <i class="fas fa-arrow-right-from-bracket"></i> Logout
            </a>
          </div>
        </div>
        <!-- Not logged in -->
        <div v-else class="sidebar-menu">
          <div class="sidebar-header">
            <h5 class="mb-0">Menu</h5>
            <button class="btn-close" @click="toggleSidebar"></button>
          </div>
          <router-link to="/user-login" class="sidebar-item" @click="toggleSidebar">
            <i class="fas fa-sign-in-alt"></i> Log In
          </router-link>
          <router-link to="/user-signup" class="sidebar-item" @click="toggleSidebar">
            <i class="fas fa-user-plus"></i> Sign Up
          </router-link>
          <router-link to="/admin-login" class="sidebar-item text-danger" @click="toggleSidebar">
            <i class="fas fa-user-shield"></i> Admin
          </router-link>
        </div>
      </div>
    </div>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg sticky-top navbar-blurred">
      <div class="container-fluid">
        <!-- Brand Logo -->
        <div class="navbar-brand d-flex align-items-center">
          <router-link to="/home" class="d-flex align-items-center text-decoration-none nav-link">
            <img src="../../public/mibuto.webp" alt="ticpic logo" style="height: 47px; margin-right: 8px;" />
          </router-link>
        </div>

        <!-- Menu Toggle Button -->
        <button class="btn btn-secondary" @click="toggleSidebar">
          <i class="fas fa-bars"></i>
        </button>
      </div>
    </nav>

    <!-- Overlay -->
    <div class="sidebar-overlay" :class="{ 'overlay-visible': isSidebarOpen }" @click="toggleSidebar">
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import CreateSubjectModal from "@/components/modals/subjects/CreateSubjectModal.vue";
import UpdateSubjectModal from "@/components/modals/subjects/UpdateSubjectModal.vue";
import DeleteSubjectModal from "@/components/modals/subjects/DeleteSubjectModal.vue";
import CreateChapterModal from "@/components/modals/chapters/CreateChapterModal.vue";
import UpdateChapterModal from "@/components/modals/chapters/UpdateChapterModal.vue";
import DeleteChapterModal from "@/components/modals/chapters/DeleteChapterModal.vue";
import CreateQuizModal from "@/components/modals/quizzes/CreateQuizModal.vue";
import UpdateQuizModal from "@/components/modals/quizzes/UpdateQuizModal.vue";
import DeleteQuizModal from "@/components/modals/quizzes/DeleteQuizModal.vue";
import ToastNotification from "@/components/ToastNotification.vue";

export default {
  name: "NavBar",
  components: {
    CreateSubjectModal, UpdateSubjectModal, DeleteSubjectModal,
    CreateChapterModal, UpdateChapterModal, DeleteChapterModal,
    CreateQuizModal, UpdateQuizModal, DeleteQuizModal,
    ToastNotification
  },
  data() {
    return {
      isSidebarOpen: false,
      showSubjectManagement: false, createSubjectModal: false, updateSubjectModal: false, deleteSubjectModal: false,
      showChapterManagement: false, createChapterModal: false, updateChapterModal: false, deleteChapterModal: false,
      showQuizManagement: false, createQuizModal: false, updateQuizModal: false, deleteQuizModal: false,
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: "user_auth/isLoggedIn",
      username: "user_auth/username",
      isAdmin: "user_auth/isAdmin",
    }),
  },
  methods: {
    ...mapActions({ clearSession: "user_auth/logout" }),
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
      if (this.isSidebarOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = 'auto';
      }
    },
    toggleSubjectManagement() { this.showSubjectManagement = !this.showSubjectManagement; },
    toggleChapterManagement() { this.showChapterManagement = !this.showChapterManagement; },
    toggleQuizManagement() { this.showQuizManagement = !this.showQuizManagement; },
    logout() { this.clearSession(); this.toggleSidebar(); },
    openModal(type) {
      switch (type) {
        case 'createSubject': this.createSubjectModal = true; break;
        case 'updateSubject': this.updateSubjectModal = true; break;
        case 'deleteSubject': this.deleteSubjectModal = true; break;
        case 'createChapter': this.createChapterModal = true; break;
        case 'updateChapter': this.updateChapterModal = true; break;
        case 'deleteChapter': this.deleteChapterModal = true; break;
        case 'createQuiz': this.createQuizModal = true; break;
        case 'updateQuiz': this.updateQuizModal = true; break;
        case 'deleteQuiz': this.deleteQuizModal = true; break;
      }
      this.toggleSidebar();
    },
    async handleAction(actionType, data, modalRef) {
      try {
        // Extract the action and entity 
        const [, action, entity] = actionType.match(/^([a-z]+)([A-Z].*)$/) || ["", ""];
        let lowerEntity = entity.toLowerCase() + `s`;
        if (lowerEntity === "quizs") lowerEntity = "quizzes";
        const response = await this.$store.dispatch(`${lowerEntity}/${actionType}`, data);
        this[modalRef] = false;
        const message = response?.msg || response?.message || `${entity} ${action} was successful!`;
        this.$refs.toastComponent?.addToast("success", message);
      } catch (error) {
        const message = error.response?.data?.msg || error.response?.data?.message || "Something went wrong. Please try again.";
        this.$refs.toastComponent?.addToast("error", message);
      }
    },

    // Subject handlers
    handleCreateSubject(data) { this.handleAction("createSubject", data, "createSubjectModal"); },
    handleUpdateSubject(data) { this.handleAction("updateSubject", data, "updateSubjectModal"); },
    handleDeleteSubject(subjectId) { this.handleAction("deleteSubject", subjectId, "deleteSubjectModal"); },
    // Chapter handlers
    handleCreateChapter(data) { this.handleAction("createChapter", data, "createChapterModal"); },
    handleUpdateChapter(data) { this.handleAction("updateChapter", data, "updateChapterModal"); },
    handleDeleteChapter(chapterId) { this.handleAction("deleteChapter", chapterId, "deleteChapterModal"); },
    // Quiz handlers
    handleCreateQuiz(data) { this.handleAction("createQuiz", data, "createQuizModal"); },
    handleUpdateQuiz(data) { this.handleAction("updateQuiz", data, "updateQuizModal"); },
    handleDeleteQuiz(quizId) { this.handleAction("deleteQuiz", quizId, "deleteQuizModal"); },
  },
};
</script>

<style>
.navbar-blurred {
  position: fixed;
  width: 100%;
  background: #9db2bf84;
  backdrop-filter: blur(4px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1030;
}

/* Sidebar styles */
.sidebar {
  position: fixed;
  top: 0;
  right: -300px;
  width: 300px;
  height: 100vh;
  background-color: white;
  transition: right 0.3s ease;
  z-index: 1040;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar-open {
  right: 0;
}

.sidebar-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dee2e6;
}

.sidebar-content {
  overflow-y: auto;
  height: calc(100% - 60px);
}

.sidebar-menu {
  padding: 1rem 0;
}

.sidebar-section {
  margin-top: 1rem;
}

.sidebar-section-title {
  border-bottom: 1px solid #dee2e6;
  border-top: 1px solid #dee2e6;
}

.sidebar-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: inherit;
  text-decoration: none;
  transition: background-color 0.2s;
  gap: 0.5rem;
}

.sidebar-item:hover:not(.disabled) {
  background-color: #f8f9fa;
  text-decoration: none;
  cursor: pointer;
}

.sidebar-item.disabled {
  color: #6c757d;
  cursor: not-allowed;
  opacity: 0.5;
}

.sidebar-item i {
  width: 20px;
}

/* Overlay */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1035;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease;
}

.overlay-visible {
  opacity: 1;
  visibility: visible;
}

/* User info section */
.user-info {
  background-color: #f8f9fa;
}

.logo {
  height: 47px;
  margin-right: 8px;
}

.nav-link:hover .logo {
  filter: invert(1) brightness(2);
  transition: filter 0.3s ease, opacity 0.3s ease;
}
</style>