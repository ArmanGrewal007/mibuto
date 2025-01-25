<!-- UserSignUp.vue -->
<template>
  <!-- cmd+K cmd+4 -->
  <div class="container custom-container">
    <div class="text-center">
      <h3>User Sign-Up</h3>
    </div>

    <!-- Toast Notifications -->
    <ToastNotification ref="toastComponent" />

    <!-- Signup Form -->
    <form @submit.prevent="submitForm">
      <!-- Username input -->
      <div class="form-floating mb-4 mt-2">
        <input type="text" id="username" class="form-control" v-model="username" ref="usernameInput" placeholder=""
          required />
        <label class="form-label" for="signupName">Username</label>
      </div>

      <!-- Email input -->
      <div class="form-floating mb-4 mt-2">
        <input type="email" id="email" class="form-control" v-model="email" @input="validateEmail" :class="{
          'email-valid': isEmailValid && email,
          'email-invalid': !isEmailValid && email,
        }" placeholder="" required />
        <label class="form-label" for="signupName">
          <small class="text-danger" v-if="!isEmailValid && email">
            Email address invalid
          </small>
          <span v-else>Email</span>
        </label>
      </div>

      <!-- Password input -->
      <div class="form-floating mb-4 mt-2">
        <input type="password" id="signupPassword" class="form-control" v-model="password" @input="validatePasswords"
          placeholder="" required />
        <label class="form-label" for="signupPassword">Password</label>
      </div>

      <!-- Confirm Password input -->
      <div class="form-floating mb-4 mt-2">
        <input type="password" id="confirmPassword" class="form-control" v-model="confirmPassword"
          @input="validatePasswords" :class="{
            'passwords-match': passwordsMatch && confirmPassword,
            'passwords-mismatch': !passwordsMatch && confirmPassword,
          }" placeholder="" required />
        <label class="form-label" for="confirmPassword">
          <small class="text-danger" v-if="!passwordsMatch && confirmPassword">
            Passwords do not match
          </small>
          <span v-else>Confirm Password</span>
        </label>

      </div>

      <!-- Sign up button -->
      <div class="d-flex justify-content-center pb-3">
        <button type="submit" class="btn btn-primary btn-block mx-2" :disabled="!isFormValid">
          Sign Up
        </button>
      </div>

      <!-- Router link -->
      <div class="pb-2 text-center">
        <router-link to="/user-login"
          class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-75-hover">
          (Click here to Login)
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import ToastNotification from '@/components/ToastNotification.vue';

export default {
  name: "UserSignup",
  components: {
    ToastNotification,
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      passwordsMatch: false,
      isEmailValid: false,
    };
  },
  computed: {
    isFormValid() {
      return (
        this.username &&
        this.email &&
        this.isEmailValid &&
        this.password &&
        this.confirmPassword &&
        this.passwordsMatch
      );
    },
  },
  methods: {
    validateEmail() {
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      this.isEmailValid = emailPattern.test(this.email);
    },
    validatePasswords() {
      this.passwordsMatch = this.password === this.confirmPassword;
    },
    submitForm() {
      if (!this.isFormValid) return;

      const user = {
        username: this.username.trim(),
        email: this.email.trim(),
        password: this.password.trim(),
      };

      this.$store
        .dispatch("user_auth/signup", user)
        .then(() => {
          this.$refs.toastComponent.addToast('success', 'Signup Successful!<br>&nbsp;Redirecting to login page');
          setTimeout(() => {
            this.$router.push({ name: "user-login" });
          }, 1000);
        })
        .catch((error) => {
          const message = error.response?.data?.msg || error.response?.data?.message || "Something went wrong. Please try again.";
          this.$refs.toastComponent.addToast('error', message);
        });
    },
  },
  mounted() {
    this.$refs.usernameInput.focus();
  },
};
</script>

<style src="./User.css" scoped></style>