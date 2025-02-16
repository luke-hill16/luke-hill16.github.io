import { createRouter, createWebHashHistory } from 'vue-router'
import login from '@/views/login/login.vue'
import frame from '@/views/main/frame.vue'
import myabsent from"@/views/abhosentt/my.vue"
import subabsent from "@/views/abhosentt/sub.vue"
import { useAuthStore }from "@/stores/auth";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'frame',
      component: frame,
      children:[
        {path:'/abhosentt/my',name:'myabsent',component:myabsent},
        {path:'/abhosentt/sub',name:'subabsent',component:subabsent}
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
  ]
})
//导航守卫
router.beforeEach((to,from)=>{
 //判断用户是否登录，如果还没有登录，并且访问的页面不是登录页面， 那么就要跳转到登录页面
 const authStore =useAuthStore()
 if (!authStore.is_logined && to.name != 'login'){
  return {name:'login'}
 }
})

export default router
