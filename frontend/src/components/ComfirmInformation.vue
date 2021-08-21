<!--reuslt can reference to  https://github.com/A6Hz/3D-bin-packing -->
<template>
  <!--root div-->
  <div>
    <!--show error message if there are empty value-->
    <div v-if="ContainerArrayHaveNoData" class="m-3">
      <a-alert
        message="There are no data settring for Box"
        description="Please go to previous page to create new container"
        type="error"
        closable
        @close="ConAlertOnClose"
      />
    </div>
    <!--end error message -->
    <!-- (box)show error message if there are empty value-->
    <div v-if="BoxArrayHaveNoData" class="m-3">
      <a-alert
        message="There are no data settring for Box"
        description="Please go to previous page to create new box"
        type="error"
        closable
        @close="ConAlertOnClose"
      />
    </div>
    <!--end error message -->
    <!--beggin of container toggle-->
    <div class="container-lg w-100 p-3">
      <b-button
        v-b-toggle
        href="#container-collapse"
        variant="light"
        class="w-100"
        >Containers</b-button
      >
      <b-collapse id="container-collapse" class="mt-2">
        <b-card v-for="(container_info, index) in container_infos" :key="index">
          <span
            class="float-end delete-span"
            @click="deleteContainerInfo(index)"
          >
            X
          </span>
          <!--flex container -->
          <div class="d-flex flex-row ">
          <img
            class="card-img img-thumbnail rounded float-start mr-4 iconImage"
            src="../../imgs/container.png"
          />
          <h1 class="display-6 ml-5">X{{ container_info.Numbers }}</h1>
            <h5 class="showID ">{{container_info.TypeName}}</h5>
             </div> 
             <b-button
            v-b-toggle
            v-bind:href="concateStringToGetContainerIDhref(index)"
            variant="success"
            size="sm"
            block
            class="float-end"
            >Details</b-button
          >    
          <b-collapse
            v-bind:id="concateStringToGetContainerID(index)"
            class="mt-2"
          >
            <!-- container detial-->
            <b-card>
              <table class="table">
                <thead class="thead-light">
                  <tr>
                    <th scope="col">ID</th>
                    <th scope="col">X</th>
                    <th scope="col">Y</th>
                    <th scope="col">Z</th>
                    <th scope="col">Weight limmit</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">{{container_info.ID}}</th>
                    <td>{{container_info.X}}</td>
                    <td>{{container_info.Y}}</td>
                    <td>{{container_info.Z}}</td>
                    <td>{{container_info.Weight_limmit}}</td>
                  </tr>
                </tbody>
              </table>
              <!--end of container detial-->
            </b-card>
          </b-collapse>
        </b-card>
      </b-collapse>
    </div>
    <!--end-of container toggle-->

    <!--beggin of box toggle-->
    <div class="container-lg w-100 p-3">
      <b-button v-b-toggle href="#box-collapse" variant="light" class="w-100"
        >Boxes</b-button
      >
      <b-collapse id="box-collapse" class="mt-2">
        <b-card v-for="(box_info, index) in box_infos" :key="index">
                    <span
            class="float-end delete-span"
            @click="deleteContainerInfo(index)"
          >
            X
          </span>
          <img
            class="card-img img-thumbnail rounded float-start mr-4 iconImage iconImage"
            src="../../imgs/package-box.png"
          />
      <h1 class="display-6 ml-5">X{{ box_info.Numbers }}</h1>
      <h1 class="showID">{{box_info.TypeName}}</h1>
          <b-button
            v-b-toggle
            v-bind:href="concateStringToGetBoxIDhref(index)"
            size="sm"
            class="float-end"
            >Details</b-button
          >
          <b-collapse v-bind:id="concateStringToGetBoxID(index)" class="mt-2">
            <b-card>
              <table class="table">
                <thead class="thead-light">
                  <tr>
                    <th scope="col">ID</th>
                    <th scope="col">X</th>
                    <th scope="col">Y</th>
                    <th scope="col">Z</th>
                    <th scope="col">Weight limmit</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">1</th>
                    <td>{{box_info.X}}</td>
                    <td>{{box_info.Y}}</td>
                    <td>{{box_info.Z}}</td>
                    <td>{{box_info.Weight}}</td>
                  </tr>
                </tbody>
              </table>
              <!--end of container detial-->
            </b-card>
          </b-collapse>
        </b-card>
      </b-collapse>
    </div>

    <!--end of box toggle-->
    <button v-on:click="sendTestMessage">sendtestjson message</button>
    <button v-on:click="sendStoredMessage">
      Send stored json data to remote API
    </button>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  //get the information from store first
  computed: {
    BoxArrayHaveNoData() {
      console.log("box_infos.length" + this.box_infos.length);
      if (this.box_infos.length === 0) {
        return true;
      } else {
        return false;
      }
    },
    ContainerArrayHaveNoData() {
      if (this.container_infos.length === 0) {
        return true;
      } else {
        return false;
      }
    },
    ...mapState({
      container_infos: (state) => state.container_infos,
      box_infos: (state) => state.box_infos,
    }),
  }, //end compute
  methods: {
    ConAlertOnClose(event) {
      console.log(event, "Alert was closed.");
    },

    sendTestMessage() {
      this.axios({
        method: "get",
        baseURL: "http://localhost:4000",
        url: "/api/",
        "Content-Type": "application/json",
      }).then((response) => {
        console.log(response.data);
      });
    },
    concateStringToGetContainerID(index) {
      return "innerbox_container_id" + index;
    },
    concateStringToGetContainerIDhref(index) {
      return "#innerbox_container_id" + index;
    },
    concateStringToGetBoxID(index) {
      return "innerbox_box_id" + index;
    },
    concateStringToGetBoxIDhref(index) {
      return "#innerbox_box_id" + index;
    },
    sendStoredMessage() {
      this.axios({
        method: "post",
        baseURL: "http://localhost:4000",
        url: "/api/ContainerAndBox/info/",
        "Content-Type": "application/json",
        data: {
          containers: this.container_infos,
          boxes: this.box_infos,
        },
      }).then((response) => {
        console.log(response.data);
      });
    },
  }, //end methods,
  data: function () {
    return {
      teststr: "collapse-1-inner",
    };
  },
};
</script>
<style scoped>
.iconImage {
  max-width: 5em;
  max-height: 6em;
}
.showID{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>>