<template>
  <div>
    <p>Loading: {{ifLoading}}</p>
    <button @click="reverseLoad()">Reverse</button>
  </div>
</template>
<script>
export default {
  name: "ComfirmInfo",
  computed: {
    ifLoading() {
      return this.$store.state.isLoading;
    }
  },
  methods: {
    reverseLoad() {
      this.$store.commit("Loaded");
    }
  }
};
</script>