import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore }from "@/stores/auth";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'frame',
      component: () => import('@/views/main/frame.vue'), // 懒加载
      children:[
        {
          path: '',  // 默认首页
          name: 'home',
          component: () => import('@/views/main/home.vue')
        },
        {path:'/abhosentt/my',name:'myabsent',component:() => import('@/views/abhosentt/my.vue')},
        {path:'/abhosentt/sub',name:'subabsent',component:() => import('@/views/abhosentt/sub.vue')},
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
      component: () => import('@/views/login/login.vue') // 懒加载
    }
  ]
})

// 简化的导航守卫 - 完全跳过登录验证
router.beforeEach((to, from) => {
  // 直接允许访问所有页面，不进行登录验证
  return true
})

export default router
