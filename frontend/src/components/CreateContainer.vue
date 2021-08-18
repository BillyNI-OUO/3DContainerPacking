     
     <template>
        <!--root div-->
     <div class="mt-2 mr-2">
     <!--card container make element in center-->
  <div class="container container-bg pb-3 mr-3 pr-3 rounded">
    <!--Butoon to create new container-->

      <button 
      class="btn btn-success m-3  "
      @click="newContainer"
      >
      New container
      </button>
      <!--End new button-->
      <!--Butoon to commit changes to store-->

      <button 
      class="btn btn-success m-3  "
      @click="saveChanges"
      >
      Save changes
      </button>
      <!--End new button-->
    <div class="card  mt-3 " v-for="(container_info, index) in  container_infos" v-bind:key="index">
      <div class="card-body pd-3">

          <!--this span (on right top corner) handle the delete form method-->
        <span 
        class="float-end delete-span" 
        @click="deleteContainerInfo(index)"
        > X 
        </span>

        <h4 class="card-title">Container ID {{index}}</h4>
        <div>
          <!--Begin of first input form content-->
          <div class="input-group mb-3">
            <input
              type="number"
              class="form-control mb-2"
              placeholder="Width(X)"
              v-model="container_info.X"
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
              v-model="container_info.Y"
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
              v-model="container_info.Z"
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
              placeholder="Weight limitation"
              v-model="container_info.Weight_limmit"
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
              v-model="container_info.Numbers"
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
    <!--end root container-->
    </div>
    <!--end root div-->
    </div>

</template>
<script>
export default {
  name: "CreateContainer",
  components: {},
  data:function(){
      return{
      container_infos:[{
          ID:'',
           X:'',
           Y:'',
           Z:'',
           Weight_limmit:'',
           Numbers:''
        }
      ]
      }//end container_info
  },//end data
  methods:{
      newContainer(){
        this.container_infos.push({
            ID:'',
            X:'',
            Y:'',
            Z:'',
            Weight_limmit:'',
            Numbers:''
        })
      },//end newContainer
      deleteContainerInfo(index){
          this.container_infos.splice(index,1);
      },//end deleteContainerInfo
      saveChanges(){
        this.$store.dispatch('loadContainerInfos', this.container_infos);
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