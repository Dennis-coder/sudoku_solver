<template>
    <div class="nav">
        <SlideButton
          :msg="'Dark Mode'"
          :fun="toggleDarkMode"
        />
    </div>
</template>

<script>
import SlideButton from '@/components/SlideButton.vue'

export default {
  name: 'Navbar',
  components: {
    SlideButton
  },
  methods: {
    toggleDarkMode (isActive) {
      this.$store.dispatch('toggleDarkMode')
    }
  }
}
</script>

<style lang="scss" scoped>
.nav {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>
