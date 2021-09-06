    <template>
  <!--root div-->
  <div class="mt-2 mr-2">
    <!--card container make element in center-->
    <div class="container container-bg pb-3 mr-3 pr-3 rounded">
      <!--Butoon to create new container-->
      <button class="btn btn-success m-3 float-md-left" @click="savePalletInfo">
        Save changes.
      </button>
      <!--End new button-->
      <div
        class="card mt-3"
      >
        <div class="card-body pd-3">
          <!--this span (on right top corner) handle the delete form method-->
          <span class="float-end delete-span" >
            X
          </span>

          <h4 class="card-title">Box index number</h4>
          <div>
            <!--Modified!, to let user can select pallect he/her want, add a select model here-->
            <div class="input-group mb-3">
                <select v-model="pallet_info.TypeName" class="form-select font-black" @change="selectOnChange($event)">
                <option v-for="(typename, index) in pallet_types" :key="index" >{{typename}}</option>
                </select>
            </div>




            <!--Modified!, to let user can set the name of the Box. add Name option upon the original first input-->
            <div class="input-group mb-3">
              <input
                type="text"
                class="form-control mb-2" 
                placeholder="Name of the box type"
                v-model="pallet_info.TypeName"
              />
            </div>
            <!--end of Modified-->
            <!--Begin of first input form content-->
            <div class="input-group mb-3">
              <input
                type="number"
                class="form-control mb-2"
                placeholder="Width(X)"
                v-model="pallet_info.X"
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
                v-model="pallet_info.Y"
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
                v-model="pallet_info.Z"
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
                v-model="pallet_info.Weight"
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
                v-model="pallet_info.Numbers"
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
import { v4 as uuidv4 } from "uuid";
import Swal from "sweetalert2";
export default {
data(){
    return{
      pallet_types:["140X102","122X102","122X90", "110X75", "138X89"],
      pallet_info: {
        ID: uuidv4(),
        TypeName: "",
        X: "",
        Y: "",
        Z: "",
        Weight: "",
        Numbers: "",
      },
      pallet_infos:[]
    }
},//end data
methods:{
  selectOnChange(envt){
          switch(envt.target.value){ 
        case "140X102":
          this.pallet_info.TypeName="140X102"
          this.pallet_info.X=140
          this.pallet_info.Z=102
          this.pallet_info.Y=12
          this.pallet_info.Weight=25
          this.pallet_info.Numbers=1
          break;
        case "122X102":
          this.pallet_info.TypeName="122X102"
          this.pallet_info.X=122
          this.pallet_info.Z=102
          this.pallet_info.Y=12
          this.pallet_info.Weight=22
          this.pallet_info.Numbers=1
          break;
        case "122X90":
          this.pallet_info.TypeName="122x90"
          this.pallet_info.X=122
          this.pallet_info.Z=90
          this.pallet_info.Y=12
          this.pallet_info.Weight=20
          this.pallet_info.Numbers=1
          break;
        case "110X75":
          this.pallet_info.TypeName="110X75"
          this.pallet_info.X=110
          this.pallet_info.Z=75
          this.pallet_info.Y=12
          this.pallet_info.Weight=12
          this.pallet_info.Numbers=1
          break;
        case "138X89":
          this.pallet_info.TypeName="138X89"
          this.pallet_info.X=138
          this.pallet_info.Z=89
          this.pallet_info.Y=12
          this.pallet_info.Weight=18
          this.pallet_info.Numbers=1
          break;
        default:
          console.log("default, not a recognizable item")
      }//end switch
  },//end selectOnChange
  savePalletInfo() {
      //show messsage
      Swal.fire({
        icon: "success",
        title: "Your work has been saved",
        showConfirmButton: false,
        timer: 1500,
      });
      this.pallet_infos.push(this.pallet_info)
      this.$store.dispatch("appendPalletInfos", this.pallet_infos);
      this.pallet_infos=[];
      this.pallet_info={ID:uuidv4()};
    },//end showBoxInfo
},
}
</script>
<style scoped>
.container-bg {
  background: #0d4069;
}

.delete-span {
  cursor: pointer;
  color: #a0a1a7;
}

.font-black{
    color:black;
}
</style>