<template>
  <div>
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

              <!-- Show Management Section -->
              <div class="sidebar-section">
                <div class="sidebar-section-title px-3 py-2 bg-light" @click="toggleShowManagement">
                  <small class="text-muted text-uppercase fw-bold">Show Management </small>
                  <i :class="['fas', showShowManagement ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  <!-- Toggle icon -->
                </div>
                <div v-if="showShowManagement"> <!-- Show buttons only if showShowManagement is true -->
                  <a href="#" class="sidebar-item" @click.prevent="openModal('createShow')">
                    <i class="fas fa-plus-circle"></i> Create Show
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('updateShow')">
                    <i class="fas fa-edit"></i> Update Show
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('deleteShow')">
                    <i class="fas fa-trash"></i> Delete Show
                  </a>
                </div>
              </div>

              <!-- Theater Management Section -->
              <div class="sidebar-section">
                <div class="sidebar-section-title px-3 py-2 bg-light" @click="toggleTheaterManagement">
                  <small class="text-muted text-uppercase fw-bold">Theater Management </small>
                  <i :class="['fas', showTheaterManagement ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  <!-- Toggle icon -->
                </div>
                <div v-if="showTheaterManagement"> <!-- Theater buttons only if showTheaterManagement is true -->
                  <a href="#" class="sidebar-item" @click.prevent="openModal('createTheater')">
                    <i class="fas fa-plus-circle"></i> Create Theater
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('updateTheater')">
                    <i class="fas fa-edit"></i> Update Theater
                  </a>
                  <a href="#" class="sidebar-item" @click.prevent="openModal('deleteTheater')">
                    <i class="fas fa-trash"></i> Delete Theater
                  </a>
                </div>
              </div>

              <!-- Schedule Management Section -->
              <div class="sidebar-section">
                <div class="sidebar-section-title px-3 py-2 bg-light" @click="toggleScheduleManagement">
                  <small class="text-muted text-uppercase fw-bold">Schedule Management </small>
                  <i :class="['fas', showScheduleManagement ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  <!-- Toggle icon -->
                </div>
                <div v-if="showScheduleManagement"> <!-- Schedule buttons only if showScheduleManagement is true -->
                  <a href="#" class="sidebar-item" @click.prevent="openModal('createSchedule')">
                    <i class="fas fa-plus-circle"></i> Create Schedule
                  </a>
                  <a href="#" class="sidebar-item disabled" @click.prevent>
                    <i class="fas fa-edit"></i> Update Schedule
                  </a>
                  <a href="#" class="sidebar-item disabled" @click.prevent>
                    <i class="fas fa-trash"></i> Delete Schedule
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
            <img src="../../public/saitousphere.webp" alt="saitousphere logo" title="home" class="logo"/>
          </router-link>
        </div>

        <!-- Menu Toggle Button -->
        <button class="btn btn-secondary" @click="toggleSidebar">
          <i class="fas fa-bars"></i>
        </button>
      </div>
    </nav>

    <!-- Overlay -->
    <div class="sidebar-overlay" :class="{ 'overlay-visible': isSidebarOpen }" @click="toggleSidebar" />
  </div>
</template>

<script>
import ToastNotification from "@/components/ToastNotification.vue";

export default {
  name: 'NavBar',
  components: {
    ToastNotification
  },
  data() {
    return {
      isSidebarOpen: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
      if (this.isSidebarOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = 'auto';
      }
    },
  }
}
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
  height: 59px; 
  margin-right: 8px;
  filter: brightness(0) saturate(100%);
}
.nav-link:hover .logo {
  filter: invert(1) brightness(0.2);
  transition: filter 0.3s ease, opacity 0.3s ease;
}
</style>