<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  // 自动设置模拟登录
  if (!authStore.is_logined) {
    const mockUser = {
      id: 1,
      email: 'admin@qq.com',
      username: 'admin',
      name: '测试用户',
      role: 'admin'
    }
    const mockToken = 'mock-token-' + Date.now()
    authStore.setUserToken(mockUser, mockToken)
    console.log('App.vue: 自动模拟登录成功')
  }
})
</script>

<template>
  <RouterView />
</template>

<style >
*{
  margin:0;
  padding:0;
}
</style>
