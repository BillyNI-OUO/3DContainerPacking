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

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
// Ant Design
Vue.use(Antd);

new Vue({
  el:'#app',
  components:{App},
  template: 'App/',
  router,
  render: h => h(App)
}).$mount('#app')
