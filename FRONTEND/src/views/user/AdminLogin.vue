<!-- AdminLogin.vue -->
<template>
  <!-- cmd+K cmd+4 -->
  <div class="container custom-container">
    <div class="text-center">
      <h3>Admin Login</h3>
    </div>

    <!-- Toast Notifications -->
    <ToastNotification ref="toastComponent" />

    <!-- Login Form -->
    <form @submit.prevent="submitForm">
      <!-- Username input -->
      <div class="form-floating mb-4 mt-2">
        <input type="text" id="loginName" class="form-control" v-model="username" ref="usernameInput" placeholder=""
          required />
        <label class="form-label" for="loginName">Username</label>
      </div>

      <!-- Password input -->
      <div class="form-floating mb-4 mt-2">
        <input type="password" id="loginPassword" class="form-control" v-model="password" placeholder="" required />
        <label class="form-label" for="loginPassword">Password</label>
      </div>

      <!-- Login button -->
      <div class="d-flex justify-content-center pb-3">
        <button type="submit" class="btn btn-primary btn-block mx-2">
          Log In
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import ToastNotification from "@/components/ToastNotification.vue";

export default {
  name: "AdminLogin",
  components: {
    ToastNotification,
  },
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    submitForm() {
      const user = {
        username: this.username.trim(),
        password: this.password.trim(),
      };

      this.$store
        .dispatch("user_auth/admin_login", user)
        .then(() => {
          this.$refs.toastComponent.addToast("success", "Welcome admin!");
          setTimeout(() => {
            this.$router.push({ name: "home" });
          }, 1000);
        })
        .catch((error) => {
          const message = error.response?.data?.msg || error.response?.data?.message || "Something went wrong. Please try again.";
          this.$refs.toastComponent.addToast("error", message);
        });
    },
  },
  mounted() {
    this.$refs.usernameInput.focus();
  },
};
</script>

<style src="./User.css" scoped></style>