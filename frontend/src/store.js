import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

<<<<<<< refs/remotes/origin/Home
// 定義一個新的 Vue Store
const store = new Vuex.Store({
    state: {
        container_infos: [],
    },
    mutations: {
        // 將state設定為參數
        MUTATE_CONTAINER_INFO: (state, new_container_infos) => {
            state.container_infos = new_container_infos;
        }
    },//end mutation
    actions: {
        loadContainerInfos: (context, container_infos) => {
            context.commit('MUTATE_CONTAINER_INFO', container_infos);
        }
    }
    })//end store
=======
// define new Vue Store
const store = new Vuex.Store({
    state: {
      isLoading: false,
    },
    mutations: {
      // setting state as parameters
      Loaded(state) {
        //isLoading have two state true/false 
        state.isLoading = !state.isLoading
      }
    }

})
>>>>>>> add save container changes and boxes changes
export default store;