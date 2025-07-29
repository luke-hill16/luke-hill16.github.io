<script setup name='login'>
import login_img from '@/assets/image/login.png'
import {reactive, onMounted, ref} from 'vue'
import {useAuthStore} from '@/stores/auth'
import {useRouter} from 'vue-router'
import authHttp from "@/api/authHttp"
import {ElMessage} from "element-plus"
import axios from 'axios'

const authStore=useAuthStore()
const router=useRouter()

// 默认测试账号
const defaultCredentials = {
  email: 'admin@qq.com',
  password: '123456'
}

// 是否使用模拟登录
const useMockLogin = ref(true)

let form =reactive({
    email: defaultCredentials.email,
    password: defaultCredentials.password
})

// 开发模式标志
const isDevMode = import.meta.env.DEV || import.meta.env.VITE_DEV_MODE === 'true'

// 模拟登录函数
const mockLogin = async (email, password) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        token: 'mock-token-' + Date.now(),
        user: {
          id: 1,
          email: email,
          username: email.split('@')[0],
          name: '测试用户',
          role: 'admin'
        }
      })
    }, 1000) // 模拟网络延迟
  })
}

// 切换登录模式
const toggleLoginMode = () => {
  useMockLogin.value = !useMockLogin.value
  if (useMockLogin.value) {
    // 切换到模拟登录时，自动填入默认账号
    form.email = defaultCredentials.email
    form.password = defaultCredentials.password
    ElMessage.info('已切换到模拟登录模式')
  } else {
    // 切换到真实登录时，清空表单
    form.email = ''
    form.password = ''
    ElMessage.info('已切换到真实后端登录模式')
  }
}

const onSubmit=async ()=>{
    let pwdRgx=/^[0-9a-zA-Z_-]{6,20}/
    let emailRgx=/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9])+/
    if(!(emailRgx.test(form.email))){
        ElMessage.info('邮箱格式不满足!')
        return;}
    if(!(pwdRgx.test(form.password))){
        ElMessage.info('密码格式不满足!')
        return;}
    
    try{
      let data
      
      // 根据模式选择登录方式
      if (useMockLogin.value && isDevMode) {
        console.log('使用模拟登录')
        data = await mockLogin(form.email, form.password)
        ElMessage.success('模拟登录成功！')
      } else {
        console.log('使用真实后端登录')
        data = await authHttp.login(form.email, form.password)
        ElMessage.success('登录成功！')
      }
      
      let token = data.token;
      let user = data.user;
      authStore.setUserToken(user, token)
      router.push({name:"frame"})
    }catch(err){
      if (useMockLogin.value && isDevMode) {
        ElMessage.error('模拟登录失败')
      } else {
        ElMessage.error('用户名或密码错误')
      }
    }
}

// 快速填入测试账号
const fillTestCredentials = () => {
  form.email = defaultCredentials.email
  form.password = defaultCredentials.password
  ElMessage.info('已填入测试账号')
}

// 组件挂载时设置默认值
onMounted(() => {
  if (isDevMode) {
    console.log('开发模式：已设置默认测试账号')
  }
})
</script>
<template>
  <div class="dowebok">
    <div class="container-login100">
      <div class="wrap-login100">
        <div class="login100-pic js-tilt" data-tilt>
          <img :src="login_img" alt="IMG" />
        </div>

        <div class="login100-from validate-form">
          <span class="login100-form-title">员工登录的</span>
          
          <!-- 开发模式提示和切换按钮 -->
          <div v-if="isDevMode" class="dev-mode-notice" style="
            background: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 15px; 
            margin-bottom: 20px;
            border-radius: 4px;
            font-size: 14px;
            color: #856404;
          ">
            <strong>🧪 开发模式</strong><br/>
            <div style="margin: 10px 0;">
              <button 
                @click="toggleLoginMode"
                :style="{
                  background: useMockLogin ? '#28a745' : '#dc3545',
                  color: 'white',
                  border: 'none',
                  padding: '5px 10px',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  marginRight: '10px'
                }"
              >
                {{ useMockLogin ? '✅ 模拟登录' : '🔗 真实登录' }}
              </button>
              <button 
                v-if="useMockLogin"
                @click="fillTestCredentials"
                style="
                  background: #007bff;
                  color: white;
                  border: none;
                  padding: '5px 10px';
                  border-radius: 3px;
                  cursor: pointer;
                "
              >
                📝 填入测试账号
              </button>
            </div>
            <div v-if="useMockLogin">
              测试账号：{{ defaultCredentials.email }}<br/>
              测试密码：{{ defaultCredentials.password }}
            </div>
            <div v-else>
              请输入真实的后端账号密码
            </div>
          </div>
          
          <div class="wrap-input100 validate-input">
            <input
              class="input100"
              type="text"
              name="email"
              placeholder="邮箱"
              v-model='form.email'
            />
            <span class="focus-input100"></span>
            <span class="symbol-input100">
              <i class="iconfont icon-fa-envelope" aria-hidden="true"></i>
            </span>
          </div>
          <div class="wrap-input100 validate-input">
            <input
              class="input100"
              type="password"
              name="password"
              placeholder="密码"
              v-model='form.password'
            />
            <span class="focus-input100"></span>
            <span class="symbol-input100">
              <i class="iconfont icon-fa-envelope" aria-hidden="true"></i>
            </span>
          </div>
          <div class="container-login100-form-btn">
            <button class="login100-form-btn" @click='onSubmit'>
              {{ useMockLogin && isDevMode ? '模拟登录' : '登录' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scope src ='@/assets/css/login.css'></style>
<style scope src ='@/assets/iconfont/iconfont.css'></style>