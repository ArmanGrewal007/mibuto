<template>
  <div class="app-container">
    <NavBar />
    <div id="router-view"><router-view /></div>
    <BottomBar />
  </div>
</template>

<script>
// import Vue  from 'vue'
import NavBar from '@/components/NavBar.vue'
import BottomBar from '@/components/BottomBar.vue'


export default {
  name: 'App',
  components: {
    NavBar, BottomBar
  }
}

</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

body {
  background: #526d82;
  font-family: "Roboto Mono", monospace;
  padding-top: 80px;
}

#router-view {
  flex: 1;
}

.btn {
  border: 1px solid #71717188;
  border-width: 3px;
}

.link-secondary,
.link-secondary:hover {
  color: #3D4551 !important;
}
</style>
