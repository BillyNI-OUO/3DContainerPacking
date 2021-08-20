<template>
  <div>
    <flickity ref="flickity" :options="flickityOptions">
      <div class="carousel-cell">1</div>
      <div class="carousel-cell">2</div>
      <div class="carousel-cell">3</div>
      <div class="carousel-cell">4</div>
      <div class="carousel-cell">5</div>
    </flickity>
  </div>
</template>

<script>
import Flickity from './Flickity.vue';

export default {
  name: "test",
  components: {
    Flickity
  },
  data() {
    return {
      flickityOptions: {
        initialIndex: 0,
        // prevNextButtons: true,
        // pageDots: true,
        // wrapAround: false
      }
    }
  },
  mounted() {
    this.resize();
  },
  methods: {
    resize() {
      this.$refs.flickity.resize();
    }
  }
};
</script>

<style>
.carousel-cell {
  align-items: center;
  background-color: lightgray;
  display: flex;
  font-size: 32px;
  height: 300px;
  justify-content: center;
  width: 500px;
}
</style>