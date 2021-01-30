<template>
  <div class="content-box">
      <p>{{msg}}</p>
      <div :class="{active: isActive, 'slide-button': true}" @click="slide">
          <div ref="slider"></div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'SlideButton',
  props: {
    msg: String,
    fun: Function
  },
  data () {
    return {
      isActive: false
    }
  },
  methods: {
    slide () {
      this.isActive = !this.isActive
      this.fun(this.isActive)
    }
  }
}
</script>

<style lang="scss" scoped>

.content-box {
  display: flex;
  flex-direction: column;
  align-items: center;

  p {
    margin: 0px;
    padding: 0px;
  }

  .slide-button {
    height: 0.25rem;
    width: 3rem;
    border-radius: 999px;
    display: flex;
    align-items: center;
    margin-top: 0.2rem;

    div {
      width: 1.2rem;
      height: 1.2rem;
      border-radius: 999px;
      transition: ease 0.5s;
      transform: translateX(-0.3rem);
    }

    &.active div{
      transition: ease 0.5s;
      transform: translateX(2.1rem);
    }
  }

}

body {
  .slide-button {
    background: rgb(220, 220, 220);
    div {
      background: radial-gradient(rgba(140,140,140,1), rgba(255,255,255,0));
    }
  }
}

body.dark-theme {
  .slide-button {
    background: rgb(70, 70, 70);
    div {
      background: radial-gradient(rgba(140,140,140,1), rgba(25,25,25,0));;
    }
  }
}
</style>
