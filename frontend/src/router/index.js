import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/About.vue')
  },
  {
    path: '/formsend',
    name: 'formsend',
    component: () => import( '../views/FormSend.vue')
  },
  {
    path: '/render',
    name: 'render',
    component:()=> import ('../views/Render.vue')
  },
  {
    path:'/loading',
    name: 'LoadingPage',
    component:()=>import('../views/LoadingPage.vue')
  },
  {
    path:'/PackingFailPage',
    name:'packingFail',
    component:()=>import('../views/PackingFail.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
