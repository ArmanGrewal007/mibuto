<!-- ToastNotification.vue -->
<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1000">
    <TransitionGroup name="toast">
      <div v-for="toast in toasts" :key="toast.id" class="toast align-items-center text-white border-0" :class="{
        'bg-success': toast.type === 'success',
        'bg-danger': toast.type === 'error',
      }" role="alert" aria-live="assertive" aria-atomic="true" style="display: block">
        <div class="d-flex">
          <div class="toast-body">
            <i :class="toast.type === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'"
              class="me-2"></i>
            {{ toast.message }}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="removeToast(toast.id)"></button>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script>
export default {
  name: 'ToastNotification',
  data() {
    return {
      toasts: [],
    };
  },
  methods: {
    addToast(type, message) {
      const toast = { id: Date.now(), type, message };
      this.toasts.push(toast);
      setTimeout(() => this.removeToast(toast.id), 2000);
    },
    removeToast(id) {
      this.toasts = this.toasts.filter((toast) => toast.id !== id);
    },
  },
};
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>