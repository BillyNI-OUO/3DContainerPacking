<!--reuslt can reference to  https://github.com/A6Hz/3D-bin-packing -->
<template>
  <!--root div-->
  <div>
<div>
  <b-button v-b-toggle.collapse-1 variant="primary">Toggle Collapse</b-button>
  <b-collapse id="collapse-1" class="mt-2">
    <b-card>
      <p class="card-text">Collapse contents Here</p>
      <b-button v-b-toggle.collapse-1-inner size="sm">Toggle Inner Collapse</b-button>
      <b-collapse id="collapse-1-inner" class="mt-2">
        <b-card>Hello!</b-card>
      </b-collapse>
    </b-card>
  </b-collapse>
</div>

    <h1>Items ({{ container_infos.length }})</h1>
    <table>
      <tbody>
        <tr v-for="(container_info, index) in container_infos" :key="index">
          <td>container</td>
          <td>{{ index }}</td>
          <td>{{ container_info.X }}</td>
          <td>{{ container_info.Y }}</td>
          <td>{{ container_info.Z }}</td>
          <td>{{ container_info.Weight_limmit }}</td>
          <td>{{ container_info.Numbers }}</td>
        </tr>
        <tr v-for="(box_info, index) in box_infos" :key="index">
          <td>box</td>
          <td>{{ index }}</td>
          <td>{{ box_info.X }}</td>
          <td>{{ box_info.Y }}</td>
          <td>{{ box_info.Z }}</td>
          <td>{{ box_info.Weight }}</td>
          <td>{{ box_info.Numbers }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: mapState({
    container_infos: (state) => state.container_infos,
    box_infos: (state) => state.box_infos,
  }),

};
</script>
