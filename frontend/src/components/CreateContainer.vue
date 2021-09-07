     
     <template>
  <!--root div-->
  <div class="mt-2 mr-2">
    <!--card container make element in center-->
    <div class="container container-bg pb-3 mr-3 pr-3 rounded">
      <!--Butoon to commit changes to store-->
      <a-popconfirm title="If the number is too big, it may crash the frontend system, are you sure you want to continue?" 
      ok-text="continue" 
      cancel-text="cancel" 
      @confirm="confirm"
      :visible="visible"
      @visibleChange="handleVisibleChange"
      >
        <button class="btn btn-success m-3">
          Save changes
        </button>
      </a-popconfirm>
      <!--End new button-->
      <div class="card mt-3">
        <div class="card-body pd-3">
          <!--this span (on right top corner) handle the delete form method-->
          <span class="float-end delete-span" @click="deleteContainerInfo()">
            X
          </span>

          <h4 class="card-title">Container Index number</h4>
          <div>
            <!--modified add a input from for typename-->
            <div class="input-group mb-3">
              <input
                type="text"
                class="form-control mb-2"
                placeholder="Type name of the container"
                v-model="container_info.TypeName"
              />
            </div>

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
    <button v-on:click="updateWithFakeData">Update with fake data</button>
    <!--end root div-->
  </div>
</template>
<script>
import Swal from "sweetalert2";
import { v4 as uuidv4 } from "uuid";
export default {
  name: "CreateContainer",
  components: {},
  data: function () {
    return {
      container_infos: [],
      container_info: {
        ID: uuidv4(),
        TypeName: "",
        X: "",
        Y: "",
        Z: "",
        Weight_limmit: "",
        Numbers: "",
      },
      visible: false,
    }; //end container_info
  }, //end data
  computed:{
    checkNumberIsTooBig(){
      if(this.container_info.Numbers>10){
        return true;
      }else{
        return false;
      }
    }
  },//end computed
  methods: {
    confirm(){
      this.saveChanges();
    },
    doNothing(){
    },
    deleteContainerInfo() {
      this.container_info = {
        ID: [uuidv4()],
        TypeName: "",
        X: "",
        Y: "",
        Z: "",
        Weight_limmit: "",
        Numbers: "",
      };
      this.container_infos = [];
    }, //end deleteContainerInfo
    saveChanges() {
    //  console.log(this.container_info);
      Swal.fire({
        icon: "success",
        title: "Your work has been saved",
        showConfirmButton: false,
        timer: 1500,
      });
      this.container_infos.push(this.container_info);
      this.$store.dispatch("appendContainerInfos", this.container_infos);
      this.container_infos = [];
      this.container_info = { ID: uuidv4() };
    },
    updateWithFakeData() {
      let test_box = [
        {
          ID: uuidv4(),
          TypeName: "helloContainer",
          X: "227",
          Y: "225",
          Z: "580",
          Weight_limmit: "20000",
          Numbers: "1",
        },
      ];
      this.$store.dispatch("appendContainerInfos", test_box);
    },
    
      handleVisibleChange(visible) {
      if (!visible) {
        this.visible = false;
        return;
      }
      // Determining condition before show the popconfirm.
      if (this.checkNumberIsTooBig) {
        this.visible = true;
      } else {
        this.confirm(); // next step
      }
      }
  }, //end methods
};
</script>
<style scoped>
.container-bg {
  background: #0d4069;
}

.delete-span {
  cursor: pointer;
  color: #a0a1a7;
}
</style>