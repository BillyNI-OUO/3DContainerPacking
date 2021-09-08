<template>
  <a-carousel :after-change="onChange">
    <div>
        <div class="box">
  <h5 class="card-header">First step</h5>
  <div class="card-body">
    <h5 class="card-title">Go to formsend page and create the container infomation</h5>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
    </div>
    <div></div>
    <div><h3>
      3
      Check the information and edit the setting.
      </h3></div>
    <div><h3>
        Send the request and rendering.
      </h3></div>
  </a-carousel>
</template>
<script>
export default {
  methods: {
    onChange(a, b, c) {
      console.log(a, b, c);
    },
  },
};
</script>
<style scoped>
/* For demo */
.ant-carousel >>> .slick-slide {
  text-align: center;
  height: 500px;
  line-height: 160px;
  background: #ffffff;
  overflow: hidden;
}

.ant-carousel >>> .slick-slide h3 {
  color: rgb(2, 1, 1);
}

.box{
height:30%;
}


</style>