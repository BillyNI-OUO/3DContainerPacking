<template>
  <!--root div-->
    <div>
        <h1>Items ({{ container_infos.length }})</h1>
        <table>
            <tbody>
                <tr v-for="(container_info,index) in container_infos" :key="index">
                    <td>{{ inex }}</td>
                    <td>{{ container_info.X}}</td>
                    <td>{{ container_info.Y}}</td>
                    <td>{{ container_info.Z}}</td>
                    <td>{{ container_info.Weight_limmit}}</td>
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
  }),
};
</script>
