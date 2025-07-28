<template>
  <el-container class="container">
    <el-aside class="aside" width="250px">
      <router-link to="/" class="brand">益客管理系统</router-link>
      <el-menu
        :router="true"
        :default-active="$route.name"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item :index="'home'" :route="{ name: 'home' }">
          <template #title>
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </template>
        </el-menu-item>
        <el-sub-menu index="2">
          <template #title>
            <el-icon><Calendar /></el-icon>
            <span>考勤管理</span>
          </template>
          <el-menu-item :index="'myabsent'" :route="{ name: 'myabsent' }"><el-icon><Avatar /></el-icon>个人管理</el-menu-item>
          <el-menu-item :index="'subabsent'" :route="{ name: 'subabsent' }"><el-icon><UserFilled /></el-icon>下属考勤</el-menu-item>
          <el-menu-item :index="'expense-rd'" :route="{ name: 'expense-rd' }"><el-icon><Money /></el-icon>研发费用管理</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="3">
          <template #title>
            <el-icon><Files /></el-icon>
            <span>通知管理</span>
          </template>
          <el-menu-item :index="'notification'" :route="{ name: 'notification' }"><el-icon><Tools /></el-icon>发布通的知</el-menu-item>
          <el-menu-item :index="'video-monitor'" :route="{ name: 'video-monitor' }"><el-icon><Comment /></el-icon>通知列的表</el-menu-item>
          <el-menu-item :index="'expense-rd2'" :route="{ name: 'expense-rd2' }"><el-icon><Money /></el-icon>研发费用管理2</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="5">
          <template #title>
            <el-icon><User /></el-icon>
            <span>员工管理</span>
          </template>
          <el-menu-item :index="'exam'" :route="{ name: 'exam' }"><el-icon><BellFilled /></el-icon>员工通的知</el-menu-item>
          <el-menu-item :index="'employee'" :route="{ name: 'employee' }"><el-icon><Briefcase /></el-icon>员工列的表</el-menu-item>
          <el-menu-item :index="'filemanage'" :route="{ name: 'filemanage' }"><el-icon><Files /></el-icon>员工管的理</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="6">
          <template #title>
            <el-icon><User /></el-icon>
            <span>智慧农业</span>
          </template>
          <el-menu-item :index="'agriculture'" :route="{ name: 'agriculture' }"><el-icon><Monitor /></el-icon>农业管理</el-menu-item>
          <el-menu-item :index="'building'" :route="{ name: 'building' }"><el-icon><Monitor /></el-icon>建筑管理</el-menu-item>
          <el-menu-item :index="'language'" :route="{ name: 'language' }"><el-icon><Monitor /></el-icon>语言管理</el-menu-item>
          <el-menu-item :index="'district'" :route="{ name: 'district' }"><el-icon><Location /></el-icon>区县管理</el-menu-item>
          <el-menu-item :index="'traffic'" :route="{ name: 'traffic' }"><el-icon><Location /></el-icon>交通管理</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="16">
          <template #title>
            <el-icon><User /></el-icon>
            <span>智慧工信</span>
          </template>
          <el-menu-item :index="'industry'" :route="{ name: 'industry' }"><el-icon><Monitor /></el-icon>工信管理</el-menu-item>
          <el-menu-item :index="'education'" :route="{ name: 'education' }"><el-icon><School /></el-icon>教育管理</el-menu-item>
          <el-menu-item :index="'enterprise'" :route="{ name: 'enterprise' }"><el-icon><House /></el-icon>企业管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="left-header">
          <el-button
            ><el-icon><Expand /></el-icon
          ></el-button>
        </div>
        <el-button
          v-show="isCollapse"
          :icon="Expand"
          @click="onCollapseAside"
        />
        <div class="right-header">
          <!-- 添加AI图标 -->
          <el-button 
            class="ai-button" 
            type="primary" 
            size="small" 
            @click="showAIChat"
            style="margin-right: 15px;"
          >
            <el-icon><ChatDotRound /></el-icon>
            AI助手
          </el-button>
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-avatar :size="30" icon="UserFilled" /><span
                style="margin-left: 10px"
                >({{ authStore.user.department.name }}){{
                  authStore.user.realname
                }}</span
              >
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="onControlResetPwdDialog">修改密码</el-dropdown-item>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item divided @click="onExit"
                  >退出登录</el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main"><RouterView></RouterView></el-main>
    </el-container>
  </el-container>
  <el-dialog v-model="dialogVisible" title="修改密码" width="500">
    <el-form :model="resetpwdform" :rules="rules" ref='formTag'>
      <el-form-item label="旧密码" :label-width="formLabelWidth" prop="oldpwd">
        <el-input v-model="resetpwdform.oldpwd" autocomplete="off"  type="password"/>
      </el-form-item>

      <el-form-item label="新密码" :label-width="formLabelWidth" prop="pwd1">
        <el-input v-model="resetpwdform.pwd1" autocomplete="off" type="password" />
      </el-form-item>

      <el-form-item label="确认密码" :label-width="formLabelWidth" prop="pwd2">
        <el-input v-model="resetpwdform.pwd2" autocomplete="off" type="password" />
      </el-form-item>
      
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
  <!-- AI对话窗口 -->
  <el-dialog 
      v-model="aiChatVisible" 
      title="AI智能助手" 
      width="800px" 
      :before-close="handleAIChatClose"
      class="ai-chat-dialog"
      draggable
    >
      <div class="chat-container">
        <!-- 左侧功能列表 -->
        <div class="chat-sidebar">
          <div class="sidebar-menu">
            <div class="menu-item" @click="selectFunction('policy')">
              <el-icon><Document /></el-icon>
              <span>政策库</span>
            </div>
            <div class="menu-item" @click="selectFunction('enterprise')">
              <el-icon><OfficeBuilding /></el-icon>
              <span>企业库</span>
            </div>
            <div class="menu-item" @click="selectFunction('regulation')">
              <el-icon><Reading /></el-icon>
              <span>法规库</span>
            </div>
            <div class="menu-item" @click="selectFunction('standard')">
              <el-icon><Collection /></el-icon>
              <span>标准库</span>
            </div>
            <div class="menu-item" @click="selectFunction('case')">
              <el-icon><Files /></el-icon>
              <span>案例库</span>
            </div>
            <div class="menu-item" @click="selectFunction('help')">
              <el-icon><QuestionFilled /></el-icon>
              <span>帮助中心</span>
            </div>
          </div>
        </div>
        
        <!-- 右侧聊天区域 -->
        <div class="chat-main">
          <!-- 聊天消息展示区域 -->
          <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="(message, index) in chatMessages" 
            :key="index" 
            :class="['message-item', message.type]"
          >
            <!-- 用户消息 -->
            <div v-if="message.type === 'user'" class="message user-message">
              <div class="message-content">
                <div class="message-text">{{ message.content }}</div>
                <div class="message-time">{{ formatTime(message.timestamp) }}</div>
              </div>
              <div class="message-avatar">
                <el-avatar :size="40" :src="userAvatar">
                  <el-icon><UserFilled /></el-icon>
                </el-avatar>
              </div>
            </div>
            <!-- AI消息 -->
            <div v-else class="message ai-message">
              <div class="message-avatar">
                <el-avatar :size="40" class="ai-avatar">
                  <el-icon><Service /></el-icon>
                </el-avatar>
              </div>
              <div class="message-content">
                <div class="message-text">{{ message.content }}</div>
                <div class="message-time">{{ formatTime(message.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="chat-input-area">
          <div class="input-container">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              placeholder="请输入您的问题..."
              @keydown.enter="sendMessage"
              resize="none"
            />
            <div class="input-actions">
              <span class="input-tip">Enter 发送</span>
              <el-button 
                type="primary" 
                @click="sendMessage"
                :loading="sending"
                :disabled="!inputMessage.trim()"
              >
                发送
              </el-button>
            </div>
          </div>
        </div>
        </div>
      </div>
    </el-dialog>
  
</template>

<script setup name="frame">
import { ref, computed, reactive, nextTick } from "vue";
import { 
  Expand, 
  Fold, 
  HomeFilled, 
  Calendar, 
  Avatar, 
  UserFilled, 
  Files, 
  Tools, 
  Comment, 
  User, 
  BellFilled, 
  Briefcase,
  ChatDotRound,
  Service,
  ArrowDown,
  Document,
  OfficeBuilding,
  Reading,
  Collection,
  QuestionFilled,
  Money,
  Monitor,
  Location,
  School,
  House
} from "@element-plus/icons-vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import authHttp from "@/api/authHttp"
import chatHttp from "@/api/chatHttp"
import { ElMessage } from "element-plus"
import Agriculture from "./agriculture.vue";

let formLabelWidth = '140px'
//ref divided
let dialogVisible = ref(false)
let resetpwdform = reactive({
  oldpwd: '',
  pwd1: '',
  pwd2: '',
})
let formTag = ref()
let rules = reactive({
  oldpwd: [
    { required: true, message: '旧密码', trigger: 'blur' },
    { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' },
  ],
  pwd1: [
    { required: true, message: '新密码', trigger: 'blur' },
    { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' },
  ],
  pwd2: [
    { required: true, message: '确认密码', trigger: 'blur' },
    { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' },
  ]
})

const authStore = useAuthStore();
const router = useRouter();

// AI对话相关
const aiChatVisible = ref(false)
const inputMessage = ref('')
const sending = ref(false)
const messagesContainer = ref(null)
const userAvatar = ref('') // 用户头像URL

// 聊天消息
const chatMessages = reactive([
  {
    type: 'ai',
    content: '您好！我是AI智能助手，有什么可以帮助您的吗？',
    timestamp: new Date()
  }
])

// 显示AI对话窗口
const showAIChat = () => {
  aiChatVisible.value = true
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

// 关闭AI对话窗口
const handleAIChatClose = () => {
  aiChatVisible.value = false
  inputMessage.value = ''
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || sending.value) return
  
  const userMessage = inputMessage.value.trim()
  
  // 添加用户消息
  chatMessages.push({
    type: 'user',
    content: userMessage,
    timestamp: new Date()
  })
  
  inputMessage.value = ''
  sending.value = true
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  try {
    // 调用真实的AI接口
    const response = await chatHttp.chatWithAI(userMessage)
    chatMessages.push({
      type: 'ai',
      content: response.reply,
      timestamp: new Date()
    })
  } catch (error) {
    console.error('AI接口调用失败:', error)
    chatMessages.push({
      type: 'ai',
      content: '抱歉，AI服务暂时不可用，请稍后再试。',
      timestamp: new Date()
    })
  } finally {
    sending.value = false
    
    // 滚动到底部
    nextTick(() => {
      scrollToBottom()
    })
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (date.toDateString() === now.toDateString()) { // 今天
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else {
    return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }
}

// 选择功能
const selectFunction = async (type) => {
  const functionNames = {
    policy: '政策库',
    enterprise: '企业库',
    regulation: '法规库',
    standard: '标准库',
    case: '案例库',
    help: '帮助中心'
  }
  
  const functionName = functionNames[type] || '未知功能'
  const userMessage = `我想查看${functionName}`
  
  // 添加用户选择消息
  chatMessages.push({
    type: 'user',
    content: userMessage,
    timestamp: new Date()
  })
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
  
  try {
    // 调用真实的AI接口
    const response = await chatHttp.chatWithAI(userMessage)
    chatMessages.push({
      type: 'ai',
      content: response.reply,
      timestamp: new Date()
    })
  } catch (error) {
    console.error('AI接口调用失败:', error)
    chatMessages.push({
      type: 'ai',
      content: `好的，我来为您打开${functionName}。这里是${functionName}的相关信息，您可以根据需要进行查询和浏览。`,
      timestamp: new Date()
    })
  }
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

// 原有方法
const onExit = () => {
  authStore.clearUserToken();
  router.push({ name: "login" });
};

const onControlResetPwdDialog = () => {
  resetpwdform.oldpwd = ''
  resetpwdform.pwd1 = ''
  resetpwdform.pwd2 = ''
  dialogVisible.value = true
}

const onSubmit = () => {
  formTag.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        await authHttp.resetPwd(resetpwdform.oldpwd, resetpwdform.pwd1, resetpwdform.pwd2)
        ElMessage.success("密码修改成功")
        dialogVisible.value = false
      } catch (detail) {
        ElMessage.error(detail)
      }
    } else {
      ElMessage.info('字段校验失败!')
      console.log('字段校验失败!');
    }
    console.log(fields)
  })
  dialogVisible.value = false
}

// 菜单相关方法
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}

const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}

const isCollapse = ref(false)
const onCollapseAside = () => {
  isCollapse.value = !isCollapse.value
}
</script>

<style scoped>
.aside {
  background-color: #e0e0e0;
}
.container {
  height: 100vh;
  background-color: #f5f6f9;
}
.aside .brand {
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid#3c3c3c;
  background-color: #5f6fd5;
  display: flex;
  height: 60px;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}
.header {
  background-color: #fff;
  border-bottom: 1px solid#e6e6e6;
  height: 60px;
  display: flex;
  justify-content: space-between;
}
.el-menu {
  border-right: none;
}
.left-header {
  display: flex;
  align-items: center;
}
.right-header {
  display: flex;
  align-items: center;
}
.el-dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.main {
  padding: 20px;
}

/* AI对话窗口样式 */
.ai-chat-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.chat-container {
  height: 600px;
  display: flex;
  flex-direction: row;
}

.chat-sidebar {
  width: 130px;
  background: #f8f9fa;
  border-right: 0px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  background: #fff;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.sidebar-menu {
  flex: 1;
  padding: 10px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  gap: 10px;
}

.menu-item:hover {
  background: #e3f2fd;
}

.menu-item .el-icon {
  font-size: 18px;
  color: #666;
}

.menu-item span {
  font-size: 14px;
  color: #333;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f8f9fa;
  border-radius: 8px 8px 0 0;
  max-height: 450px;
}

.message-item {
  margin-bottom: 20px;
  display: flex;
  width: 100%;
}

.message-item.user {
  justify-content: flex-end;
}

.message-item.ai {
  justify-content: flex-start;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
}

.user-message {
  flex-direction: row !important;
  justify-content: flex-end;
  margin-left: auto;
}

.ai-message {
  flex-direction: row;
  justify-content: flex-start;
  margin-right: auto;
}

.message-avatar {
  flex-shrink: 0;
}

.ai-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-content {
  max-width: 85%;
  display: flex;
  flex-direction: column;
}

.user-message .message-content {
  align-items: flex-end;
  text-align: right;
}

.ai-message .message-content {
  align-items: flex-start;
  text-align: left;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  word-wrap: break-word;
  line-height: 1.5;
}

.user-message .message-text {
  background: #007bff;
  color: white;
  border-radius: 12px 12px 4px 12px;
  margin-left: auto;
}

.ai-message .message-text {
  background: white;
  color: #333;
  border: 1px solid #e0e0e0;
  border-radius: 12px 12px 12px 4px;
  margin-right: auto;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  text-align: right;
}

.ai-message .message-time {
  text-align: left;
}

.chat-input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid #e0e0e0;
  border-radius: 0 0 8px 8px;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-tip {
  font-size: 12px;
  color: #999;
}

/* AI按钮样式 */
.ai-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.ai-button:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}
</style>