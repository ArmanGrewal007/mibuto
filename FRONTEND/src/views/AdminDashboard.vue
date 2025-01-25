<!-- AdminDashboard.vue -->
<template>
  <div class="container mt-4">
    <!-- Toast Notifications -->
    <ToastNotification ref="toastComponent" />

    <div v-if="!isLoggedIn">
      <p>Please log in as admin to view this page.</p>
      <div class="btn btn-primary" @click="$router.push('/home')">Go to Home</div>
    </div>

    <div v-else-if="isLoggedIn && !isAdmin">
      <p>You are not authorized to use this page.</p>
    </div>

    <div v-else>
      <div class="mb-4">
        Hi {{ username }}, isLoggedIn: {{ isLoggedIn }}, isAdmin: {{ isAdmin }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import ToastNotification from "@/components/ToastNotification.vue";

export default {
  name: "AdminDashboard",
  components: {
    ToastNotification
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters({
      username: 'user_auth/username',
      isLoggedIn: 'user_auth/isLoggedIn',
      isAdmin: 'user_auth/isAdmin'
    })
  }
};
</script>