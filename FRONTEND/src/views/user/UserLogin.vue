<!-- UserLogin.vue -->
<template>
  <!-- cmd+K cmd+4 -->
  <div class="container custom-container">
    <div class="text-center">
      <h3>User Login</h3>
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

      <!-- Router link -->
      <div class="pb-2 text-center">
        <router-link to="/user-signup"
          class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-75-hover">
          (Click here to Sign-Up)
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import ToastNotification from '@/components/ToastNotification.vue';

export default {
  name: "UserLogin",
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
        .dispatch("user_auth/login", user)
        .then(() => {
          this.$refs.toastComponent.addToast("success", "Login Successful!");
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