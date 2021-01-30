<template>
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Quicksand&display=swap" rel="stylesheet">
  <Navbar/>
  <router-view/>
</template>

<script>

import Navbar from '@/components/Navbar.vue'

export default {
  components: {
    Navbar
  },
  computed: {
    darkMode () {
      return this.$store.getters.darkMode
    }
  },
  watch: {
    darkMode (newState, _) {
      document.body.classList.toggle('dark-theme')
    }
  }
}
</script>

<style lang="scss">

body {
  transition: ease 1s;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  * {
    font-family: 'Quicksand', sans-serif;
    outline: none;
  }

  #app {
    text-align: center;
  }

  .hidden{
    display: none;
  }
}

body {
  background: rgb(250, 250, 250);

  p, button, h3, input, textarea {
    color: rgb(50,50,50);
    border-color: none;
  }
}

body.dark-theme{
  background: rgb(30, 30, 30);

  p, button, h3, input, textarea {
    color: rgb(200,200,200);
    border-color: none;
  }
}
</style>
