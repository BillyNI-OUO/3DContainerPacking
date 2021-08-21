import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

// 定義一個新的 Vue Store
const store = new Vuex.Store({
    state: {
        container_infos: [],
        box_infos:[],
    },
    mutations: {
        // 將state設定為參數
        MUTATE_CONTAINER_INFO: (state, new_container_infos) => {
            state.container_infos = new_container_infos;
        },
        MUTATE_BOX_INFO:(state, new_box_infos)=>{
            state.box_infos=new_box_infos;
        },
        MUTATE_APPEND_CONTAINER_INFO(state, container_info_to_be_appended){
            state.container_infos=[...state.container_infos, ...container_info_to_be_appended]
        }
    },//end mutation
    actions: {
        loadContainerInfos: (context, container_infos) => {
            context.commit('MUTATE_CONTAINER_INFO', container_infos);
        },//end loadContainerInfos
        loadBoxInfos:(context, box_infos)=>{
            context.commit('MUTATE_BOX_INFO', box_infos);
        },
        appendContainerInfos:(contex, container_info)=>{
            contex.commit("MUTATE_APPEND_CONTAINER_INFO", container_info)
        }
    },//end actions
    getters:{
        getContainerInfos:state=>{
            return state.container_infos
        }
    }
    })//end store
export default store;