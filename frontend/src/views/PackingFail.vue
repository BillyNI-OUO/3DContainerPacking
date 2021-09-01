<template>
  <div class="box">
      <div>
      <h1>Packing fail, not event sigle box can be packed.      </h1>
      <img src="../../imgs/sad.png" height="100" width="100">
    <h2>
    <small class="text-muted">Will redirect to home page in {{ countDown }} sec</small>  
    </h2>
    </div>
      </div>
</template>

<script>
export default{
   name: 'PackingFail',
   data(){
      return{
         countDown : 10
      }
   },
  methods: {
         countDownTimer(){
                if(this.countDown > 0) {
                    setTimeout(() => {
                        this.countDown -= 1
                        this.countDownTimer()
                    }, 1000)
                }
         }  
  },
    created(){
        this.countDownTimer()
        console.log("packing fail page")
        setTimeout(
            ()=>{
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