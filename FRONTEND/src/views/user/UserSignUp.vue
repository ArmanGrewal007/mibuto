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
        <label class="form-label" for="username">Username</label>
      </div>

      <!-- Full Name input -->
      <div class="form-floating mb-4 mt-2">
        <input type="text" id="fullName" class="form-control" v-model="fullName" placeholder="" required />
        <label class="form-label" for="fullName">Full Name</label>
      </div>

      <!-- Qualification Dropdown -->
      <div class="form-floating mb-4 mt-2">
        <select id="qualification" class="form-select" v-model="qualification" required>
          <option value="" disabled>Select Qualification</option>
          <option value="High School">High School</option>
          <option value="Bachelor's Degree">Bachelor's Degree</option>
          <option value="Master's Degree">Master's Degree</option>
          <option value="PhD">PhD</option>
          <option value="Professional Certification">Professional Certification</option>
          <option value="Other">Other</option>
        </select>
        <label for="qualification">Qualification</label>
      </div>

      <!-- Date of Birth input -->
      <div class="form-floating mb-4 mt-2">
        <input type="date" id="dob" class="form-control" v-model="dob" :max="maxDate" @blur="validateDOB" placeholder=""
          required />
        <label class="form-label" for="dob">Date of Birth</label>
        <small v-if="dobError" class="text-danger">{{ dobError }}</small>
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
      fullName: "",
      qualification: "",
      dob: "",
      dobError: "",
      password: "",
      confirmPassword: "",
      passwordsMatch: false,
    };
  },
  computed: {
    maxDate() {
      // Set max date to 16 years ago
      const date = new Date();
      date.setFullYear(date.getFullYear() - 16);
      return date.toISOString().split('T')[0];
    },
    isFormValid() {
      return (
        this.username &&
        this.fullName &&
        this.qualification &&
        this.dob &&
        !this.dobError &&
        this.password &&
        this.confirmPassword &&
        this.passwordsMatch
      );
    },
  },
  methods: {
    validateDOB() {
      if (!this.dob) {
        this.dobError = "Date of Birth is required";
        return;
      }

      const selectedDate = new Date(this.dob);
      const sixteenYearsAgo = new Date();
      sixteenYearsAgo.setFullYear(sixteenYearsAgo.getFullYear() - 16);

      if (selectedDate > sixteenYearsAgo) {
        this.dobError = "You must be at least 16 years old";
      } else {
        this.dobError = "";
      }
    },
    validatePasswords() {
      this.passwordsMatch = this.password === this.confirmPassword;
    },
    submitForm() {
      if (!this.isFormValid) return;

      const user = {
        username: this.username.trim(),
        full_name: this.fullName.trim(),
        qualification: this.qualification.trim(),
        dob: this.dob,
        password: this.password.trim(),
      };

      this.$store
        .dispatch("user_auth/signup", user)
        .then(() => {
          this.$refs.toastComponent.addToast('success', 'Signup Successful! Redirecting to login page');
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