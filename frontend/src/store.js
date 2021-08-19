import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

// 定義一個新的 Vue Store
const store = new Vuex.Store({
    state: {
        container_infos: [{
            ID:'',
            X:'',
            Y:'',
            Z:'',
            Weight_limmit:'',
            Numbers:''
        },],
        box_infos:[{
            TypeName:'',
            X:'',
            Y:'',
            Z:'',
            Weight:'',
            Numbers:''
        }],
    },
    mutations: {
        // 將state設定為參數
        MUTATE_CONTAINER_INFO: (state, new_container_infos) => {
            state.container_infos = new_container_infos;
        },
        MUTATE_BOX_INFO:(state, new_box_infos)=>{
            state.box_infos=new_box_infos;
        }
    },//end mutation
    actions: {
        loadContainerInfos: (context, container_infos) => {
            context.commit('MUTATE_CONTAINER_INFO', container_infos);
        },//end loadContainerInfos
        loadBoxInfos:(context, box_infos)=>{
            context.commit('MUTATE_BOX_INFO', box_infos);
        },
    },//end actions
    getters:{
        getContainerInfos:state=>{
            return state.container_infos
        }
    }
    })//end store
export default store;