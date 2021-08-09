<template>
  <div id="app">
    <div id="nav">
      <custom-navbar/>
    </div>
    <router-view/>
  </div>
</template>

<script>
import CustomNavbar from './components/CustomNavbar.vue'
export default {
  name: 'App',
  components: {
      CustomNavbar
  }
}

</script>


