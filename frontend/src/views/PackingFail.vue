<template>
  <div class="box">
      <div>
      <h1>Packing fail, not event sigle box can be packed.      </h1>
    <h2>
    <small class="text-muted">Will redirect to home page in 10sec</small>  
    </h2>
    </div>
      </div>
</template>

<script>
export default{
   name: 'PackingFail',
  components: {
  },
    created(){
        console.log("packing fail page")
        setTimeout(
            ()=>{
            this.$router.push("/")
            },10000
        )
    },
}
</script>
<style scoped>
.box {
    margin: 0 auto;
    text-align: left;
    width: 800px;
}
</style>