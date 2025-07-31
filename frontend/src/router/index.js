import { createRouter, createWebHistory } from 'vue-router'
import SpotPriceQuery from '../views/SpotPriceQuery.vue'

const routes = [
  {
    path: '/',
    name: 'SpotPriceQuery',
    component: SpotPriceQuery
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 