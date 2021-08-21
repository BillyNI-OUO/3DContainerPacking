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


      <!--Tab 2 shows new create box-->
      <a-tab-pane key="2" tab="Create boxes">
        <create-boxes/>
      </a-tab-pane>
      <!--end of tap pane 2-->
      <!--Tap 3 shows the comfirmation table and send the result to backedn-->
      <a-tab-pane key="3" tab="Comfirm the informaiton">
      <comfirm-information/>
      </a-tab-pane>
    </a-tabs>
          <!--end of tap pane 3-->
  </div>
  <!--end root element -->
</template>

<script>
import ComfirmInformation from '../components/ComfirmInformation.vue';
import CreateBoxes from '../components/CreateBoxes.vue';
import CreateContainer from '../components/CreateContainer.vue';

export default {
  components:{
    CreateContainer,
    CreateBoxes,
    ComfirmInformation
  },
  data() {
    return {};
  },
};
</script>

