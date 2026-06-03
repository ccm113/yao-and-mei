import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'
import Story from '@/views/Story.vue'
import Game from '@/views/Game.vue'
import QnA from '@/views/QnA.vue'
import WishList from '@/views/WishList.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/', name: 'Home', component: Home },
  { path: '/story', name: 'Story', component: Story },
  { path: '/game', name: 'Game', component: Game },
  { path: '/qna', name: 'QnA', component: QnA },
  { path: '/wishlist', name: 'WishList', component: WishList },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const isLoggedIn = localStorage.getItem('user')
  if (to.path !== '/login' && to.path !== '/register' && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
