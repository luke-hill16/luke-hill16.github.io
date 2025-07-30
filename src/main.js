import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
const app = createApp(App)

// 添加全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.log('Vue Error:', err);
  console.log('Error Info:', info);
  // 忽略连接相关错误
  if (err.message && err.message.includes('connection')) {
    return;
  }
};

// 添加全局警告处理
app.config.warnHandler = (msg, vm, trace) => {
  console.log('Vue Warning:', msg);
  console.log('Warning Trace:', trace);
};

app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
    locale: zhCn,});
//icon
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.mount('#app')
