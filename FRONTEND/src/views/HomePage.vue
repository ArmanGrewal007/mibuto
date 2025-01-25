<template>
  <div>
    <div class="mb-4">
      Hi {{ username }}, isLoggedIn: {{ isLoggedIn }}, isAdmin: {{ isAdmin }}
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'HomePage',
  computed: {
    ...mapGetters({
      username: 'user_auth/username',
      isLoggedIn: 'user_auth/isLoggedIn',
      isAdmin: 'user_auth/isAdmin'
    })
  }
}
</script>

<style lang="scss" scoped></style>