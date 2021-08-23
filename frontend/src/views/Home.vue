<template>
  <div class="home">
   <!-- <img alt="Vue logo" src="../assets/logo.png">-->
    <slide-bar/>
  </div>
</template>

<script>
import SlideBar from '../components/SlideBar.vue';
export default {
  name: 'Home',
  components: {
    SlideBar
  }
}
</script>
