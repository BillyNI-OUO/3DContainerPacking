<!--reuslt can reference to  https://github.com/A6Hz/3D-bin-packing -->
<template>
  <!--root div-->
  <div>
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
          <p class="card-text">ID {{ container_info.ID }}</p>
          <b-button
            v-b-toggle
            v-bind:href="concateStringToGetContainerIDhref(index)"
            size="sm"
            >Details</b-button
          >
          <b-collapse
            v-bind:id="concateStringToGetContainerID(index)"
            class="mt-2"
          >
            <b-card>Hello!</b-card>
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
          <p class="card-text">ID {{ box_info.ID }}</p>
          <b-button
            v-b-toggle
            v-bind:href="concateStringToGetBoxIDhref(index)"
            size="sm"
            >Details</b-button
          >
          <b-collapse v-bind:id="concateStringToGetBoxID(index)" class="mt-2">
            <b-card>Hello!</b-card>
          </b-collapse>
        </b-card>
      </b-collapse>
    </div>

    <!--end of box toggle-->
    <button v-on:click="sendTestMessage">sendtestjson message</button>
    <button v-on:click="sendStoredMessage"> Send stored json data to remote API</button>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  //get the information from store first
  computed: mapState({
    container_infos: (state) => state.container_infos,
    box_infos: (state) => state.box_infos,
  }), //end compute
  methods: {
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
        data:{
          "containers":this.container_infos,
          "boxes":this.box_infos
        }
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
