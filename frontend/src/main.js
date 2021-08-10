import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


//Import Ant Design
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

<<<<<<< refs/remotes/origin/Home
//vuex
import Vuex from 'vuex'
import store from './store.js'

=======
//Vuex for state management
import Vuex from 'vuex'
//import store.js
import store from './store'
>>>>>>> add save container changes and boxes changes

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
// Ant Design
Vue.use(Antd);
//load Vuex
Vue.use(Vuex);




//load vuex
Vue.use(Vuex);


new Vue({
  el:'#app',
  components:{App},
  template: 'App/',
  router,
  store,
  render: h => h(App)
}).$mount('#app')
