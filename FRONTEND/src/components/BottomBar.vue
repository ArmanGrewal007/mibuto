<!-- BottomBar.vue -->
<template>
  <div>
    <!-- Footer -->
    <br /> <br />
    <footer class="text-center text-lg-start text-white" style="background-color: #3e4551">
      <!-- Grid container -->
      <div class="container p-4">
        <!-- Section: Links -->
        <section class="d-flex justify-content-between align-items-center">
          <!-- saitousphere Icon -->
          <div class="d-flex align-items-center gap-2">
            <router-link to="/home" class="nav-link">
              <img src="/saitousphere.webp" alt="saitousphere" class="logo" title="home" />
            </router-link>
          </div>

          <!-- Social Media Icons -->
          <div>
            <!-- Website -->
            <a class="btn btn-outline-light btn-floating m-1" href="https://armangrewal007.github.io" role="button"
              target="_blank">
              <i class="fas fa-globe"></i>
            </a>
            <!-- Gmail -->
            <a class="btn btn-outline-light btn-floating m-1" href="#!" role="button" target="_blank">
              <i class="fas fa-envelope" aria-hidden="true"></i>
            </a>

            <!-- Instagram -->
            <a class="btn btn-outline-light btn-floating m-1" href="https://www.instagram.com/arman.singh.grewal/"
              role="button" target="_blank">
              <i class="fab fa-instagram"></i>
            </a>

            <!-- LinkedIn -->
            <a class="btn btn-outline-light btn-floating m-1" href="https://www.linkedin.com/in/armangrewal007/"
              role="button" target="_blank">
              <i class="fab fa-linkedin-in"></i>
            </a>

            <!-- Github -->
            <a class="btn btn-outline-light btn-floating m-1" href="https://github.com/ArmanGrewal007/" role="button"
              target="_blank">
              <i class="fab fa-github"></i>
            </a>
          </div>
        </section>
      </div>

      <!-- Copyright -->
      <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2); border-top: 1px solid #6E747D;">
        © 2025 Copyright:
        <a class="link-body-emphasis text-white text-decoration-underline"
          href="https://github.com/ArmanGrewal007/saitousphere/blob/main/LICENSE" target="_blank">ArmanGrewal007</a>
      </div>
      <!-- Copyright -->
    </footer>
    <!-- Footer -->
  </div>
</template>

<script>
export default {
  name: "BottomBar",
};
</script>

<style scoped>
.footer {
  padding: 20px 0;
}

.btn-floating {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.btn-floating:hover {
  transform: scale(1.16);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.logo {
  object-fit: contain;
  filter: brightness(0) saturate(100%);
}
.nav-link:hover .logo {
  filter: invert(1) brightness(0.1);
  opacity: 1;
  transition: filter 0.3s ease, opacity 0.3s ease;
}
</style>