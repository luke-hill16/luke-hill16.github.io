import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

console.log('main.js 开始执行')

const app = createApp(App)

console.log('Vue app 创建成功')

app.use(createPinia())
console.log('Pinia 注册成功')

app.use(router)
console.log('Router 注册成功')

app.use(ElementPlus, { locale: zhCn })
console.log('ElementPlus 注册成功')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

console.log('准备挂载 app')

app.mount('#app')

console.log('app 挂载完成')
