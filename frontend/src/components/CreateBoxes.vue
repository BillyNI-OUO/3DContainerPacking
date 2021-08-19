     
     <template>
     <!--root div-->
     <div class="mt-2 mr-2">
     <!--card container make element in center-->
  <div class="container container-bg pb-3 mr-3 pr-3 rounded">
          <!--Butoon to create new container-->
      <button 
      class="btn btn-success m-3 float-md-left"
      @click="newBox"
      >
      New Box
      </button>
      <!--End new button-->
    <!--Butoon to create new container-->
      <button 
      class="btn btn-success m-3 float-md-left"
      @click="saveBoxInfo"
      >
      Save changes.
      </button>
      <!--End new button-->
    <div class="card mt-3 " v-for="(box_info, index) in  box_infos" v-bind:key="index">
      <div class="card-body pd-3">

          <!--this span (on right top corner) handle the delete form method-->
        <span 
        class="float-end delete-span" 
        @click="deleteBoxInfo(index)"
        > X 
        </span>

        <h4 class="card-title">Box index number {{index}}</h4>
        <div>
          <!--Modified!, to let user can set the name of the Box. add Name option upon the original first input-->
             <div class="input-group mb-3">

            <input
              type="text"
              class="form-control mb-2"
              placeholder="Name of the box type"
              v-model="box_info.TypeName"
            />
            </div>
          <!--end of Modified-->
          <!--Begin of first input form content-->
          <div class="input-group mb-3">
            <input
              type="number"
              class="form-control mb-2"
              placeholder="Width(X)"
              v-model="box_info.X"
            />
            <div class="input-group-append">
              <span class="input-group-text" id="basic-addon2">cm</span>
            </div>
            <!--End of formating span-->
          </div>
          <!--End of first input form content -->

          <!--Begin of second input form content-->
          <div class="input-group mb-3">
            <input
              type="number"
              class="form-control mb-2"
              placeholder="Heigh(Y)"
              v-model="box_info.Y"
            />
            <div class="input-group-append">
              <span class="input-group-text" id="basic-addon2">cm</span>
            </div>
            <!--End of formating span-->
          </div>
          <!--End of second input form content -->

          <!--Begin of third input form content-->
          <div class="input-group mb-3">
            <input
              type="number"
              class="form-control mb-2"
              placeholder="Deepth(Z)"
              v-model="box_info.Z"
            />
            <div class="input-group-append">
              <span class="input-group-text" id="basic-addon2">cm</span>
            </div>
            <!--End of formating span-->
          </div>
          <!--End of third input form content -->

          <!--Begin of forth input form content-->
          <div class="input-group mb-3">

            <input
              type="number"
              class="form-control mb-2"
              placeholder="Weight "
              v-model="box_info.Weight"
            />
            <div class="input-group-append">
              <span class="input-group-text" id="basic-addon2">KG</span>
            </div>
            <!--End of formating span-->
          </div>

          <!--End of fifth input form content -->
          <!--Begin of forth input form content-->
          <div class="input-group mb-3">
            <input
              type="number"
              class="form-control mb-2"
              placeholder="Number"
              v-model="box_info.Numbers"
            />

            <div class="input-group-append">
              <span class="input-group-text" id="basic-addon2">Number</span>
            </div>
            <!--End of formating span-->
          </div>
          <!--End of fifth input form content -->
      </div>
      <!-- end card body-->
    </div>
    <!-- end card  -->
  </div>
    </div>
  <!--end container-->
  <!--end root div-->
  </div>
</template>
<script>
export default {
  name: "CreateBoxes",
  components: {},
  data:function(){
      return{
      box_infos:[{
          TypeName:'',
           X:'',
           Y:'',
           Z:'',
           Weight:'',
           Numbers:''
        }
      ]
      }//end box_info
  },//end data
  methods:{
      newBox(){
        this.box_infos.push({
            TypeName:'',
            X:'',
            Y:'',
            Z:'',
            Weight:'',
            Numbers:''
        })
      },//end newBox
      deleteBoxInfo(index){
          this.box_infos.splice(index,1);
      },
      saveBoxInfo(){
           this.$store.dispatch('loadBoxInfos', this.box_infos);
      }
  }//end methods
};
</script>
<style scoped>
.container-bg{
  background: #0d4069;
}

.delete-span{
    cursor:pointer;
    color:#a0a1a7;
}

</style>