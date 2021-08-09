<template>
  <div>
    <!--root div -->
    <!--Begin of ant tap-->
    <a-tabs default-active-key="1" tab-position="left" size="large" >
      <a-tab-pane key="1" tab="Create containers" >
        <!--Tap 1 shows new create container-->
        <create-container/>
       </a-tab-pane>
       <!--end tap pane 1-->
      <!--Tap 2 shows new create box-->
      <a-tab-pane key="2" tab="Create boxes">
        <create-boxes/>
      </a-tab-pane>
      <!--end of tap pane 2-->
      <a-tab-pane key="3" tab="Comfirm the informaiton"> Confirminformation</a-tab-pane>
    </a-tabs>
  </div>
  <!--end root element -->
</template>

<script>
import CreateBoxes from '../components/CreateBoxes.vue';
import CreateContainer from '../components/CreateContainer.vue';

export default {
  components:{
    CreateContainer,
    CreateBoxes
  },
  data() {
    return {};
  },
};
</script>

