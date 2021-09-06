<template>
  <div>
    <!--root div -->
    <!--Begin of ant tap-->
    <a-tabs default-active-key="1" tab-position="left" size="large" >
    <!--Tap 1 shows the upload page, let able user to upload the excel file to create box and container-->
      <a-tab-pane key="1" tab="Upload the setting files">
        <upload-setting-file/>
      </a-tab-pane>
       <!--end of tap pane 1-->

        <!--Tap 2 shows new create container-->
      <a-tab-pane key="2" tab="Create containers" >
        <create-container/>
      </a-tab-pane>
       <!--end tap pane 2-->


      <!--Tap 3 shows new pallets-->
      <a-tab-pane key="3" tab="Select palletes">
        <create-pallet/>
      </a-tab-pane>
      <!--end of tap pane 3-->


      <!--Tab 4 shows new create box-->
      <a-tab-pane key="4" tab="Create boxes">
        <create-boxes/>
      </a-tab-pane>
      <!--end of tap pane 3-->
      <!--Tap 4 shows the comfirmation table and send the result to backedn-->
      <a-tab-pane key="5" tab="Comfirm the informaiton">
      <comfirm-information/>
      </a-tab-pane>
       <!--end of tap pane 4-->

    </a-tabs>
         
  </div>
  <!--end root element -->
</template>

<script>
import ComfirmInformation from '../components/ComfirmInformation.vue';
import CreateBoxes from '../components/CreateBoxes.vue';
import CreateContainer from '../components/CreateContainer.vue';
import UploadSettingFile from '../components/UploadSettingFile.vue';
import CreatePallet from '../components/CreatePallet.vue'

export default {
  components:{
    CreateContainer,
    CreateBoxes,
    ComfirmInformation,
    UploadSettingFile,
    CreatePallet
  },
  data() {
    return {};
  },
};
</script>

