<template>
  <div id="app">
    <div id="nav">
      <custom-navbar/>
    </div>
    <transition name="slide" mode="out-in">
    <router-view/>

    </transition>
  </div>
</template>

<script>
import CustomNavbar from './components/CustomNavbar.vue'
export default {
  name: 'App',
  components: {
      CustomNavbar,
  }
}

</script>
<style scoped>
.slide-enter-active,
.slide-leave-active{
transition:opacity 0.7s, transform 0.7s;
}
.slide-enter,
.slide-leave-to{  
  opacity:0;
  transform: translateX(-40%);
}
</style>



