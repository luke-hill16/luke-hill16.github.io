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
        {
          path: '',  // 添加这个空路径作为默认首页
          name: 'home',
          component: () => import('@/views/main/home.vue')  // 懒加载首页组件
        },
        {path:'/abhosentt/my',name:'myabsent',component:myabsent},
        {path:'/abhosentt/sub',name:'subabsent',component:subabsent},
        {path:'/employee',name:'employee',component:() => import('@/views/main/employee.vue')},
        {path:'/video-monitor',name:'video-monitor',component:() => import('@/views/main/video-monitor.vue')},
        {path:'/exam',name:'exam',component:() => import('@/views/main/exam.vue')},
        {path:'/notification',name:'notification',component:() => import('@/views/main/notification.vue')},
        {path:'/expense-rd',name:'expense-rd',component:() => import('@/views/main/expense-rd.vue')},
        {path:'/expense-rd2',name:'expense-rd2',component:() => import('@/views/main/expense-rd2.vue')},
        {path:'/filemanage',name:'filemanage',component:() => import('@/views/main/filemanage.vue')},
        {path:'/agriculture',name:'agriculture',component:() => import('@/views/main/agriculture.vue')},
        {path:'/building',name:'building',component:() => import('@/views/main/building.vue')},
        {path:'/language',name:'language',component:() => import('@/views/main/language.vue')},
        {path:'/district',name:'district',component:() => import('@/views/main/dihestrict.vue')},
        {path:'/traffic',name:'traffic',component:() => import('@/views/main/traffic.vue')},
        {path:'/industry',name:'industry',component:() => import('@/views/main/industry.vue')},
        {path:'/education',name:'education',component:() => import('@/views/main/education.vue')},
        {path:'/enterprise',name:'enterprise',component:() => import('@/views/main/enterprise.vue')},
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
