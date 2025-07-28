<template>
  <div class="notification-container">
    <el-card>
      <div class="header">
        <span>通知管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="createNotification" size="small">发布通知</el-button>
          <el-button type="success" @click="refreshNotifications" size="small">刷新</el-button>
        </div>
      </div>
      
      <!-- 通知列表 -->
      <el-table :data="notifications" style="width: 100%; margin-top: 20px;" fit="true">
        <el-table-column prop="title" label="通知标题" min-width="200">
          <template #default="scope">
            <span class="clickable-title" @click="viewNotificationDetail(scope.row)">{{ scope.row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="通知类别" min-width="120"/>
        <el-table-column prop="priority" label="优先级" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.priority === '高'" type="danger">{{ scope.row.priority }}</el-tag>
            <el-tag v-else-if="scope.row.priority === '中'" type="warning">{{ scope.row.priority }}</el-tag>
            <el-tag v-else type="info">{{ scope.row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === '已发布'" type="success">{{ scope.row.status }}</el-tag>
            <el-tag v-else-if="scope.row.status === '草稿'" type="info">{{ scope.row.status }}</el-tag>
            <el-tag v-else type="warning">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publisher" label="发布人" min-width="120"/>
        <el-table-column prop="publishTime" label="发布时间" min-width="150"/>
        <el-table-column prop="readCount" label="已读人数" min-width="100"/>
        <el-table-column label="操作" min-width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="editNotification(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="viewReadStatus(scope.row)">查看已读</el-button>
            <el-button size="small" type="danger" @click="deleteNotification(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 通知详情弹窗 -->
    <el-dialog v-model="notificationDetailVisible" title="通知详情" width="900px" :before-close="handleClose">
      <div class="notification-detail" v-if="currentNotification">
        <!-- 通知基本信息 -->
        <el-card class="info-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>通知信息</span>
              <el-button type="primary" size="small" @click="editNotification(currentNotification)">编辑通知</el-button>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>通知标题：</label>
                <span>{{ currentNotification.title }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>通知类别：</label>
                <span>{{ currentNotification.category }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>优先级：</label>
                <el-tag v-if="currentNotification.priority === '高'" type="danger">{{ currentNotification.priority }}</el-tag>
                <el-tag v-else-if="currentNotification.priority === '中'" type="warning">{{ currentNotification.priority }}</el-tag>
                <el-tag v-else type="info">{{ currentNotification.priority }}</el-tag>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>状态：</label>
                <el-tag v-if="currentNotification.status === '已发布'" type="success">{{ currentNotification.status }}</el-tag>
                <el-tag v-else-if="currentNotification.status === '草稿'" type="info">{{ currentNotification.status }}</el-tag>
                <el-tag v-else type="warning">{{ currentNotification.status }}</el-tag>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>发布人：</label>
                <span>{{ currentNotification.publisher }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>发布时间：</label>
                <span>{{ currentNotification.publishTime }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="detail-item">
                <label>通知内容：</label>
                <div class="content-text">{{ currentNotification.content }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <!-- 已读状态列表 -->
        <el-card class="read-status-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>已读状态</span>
              <div class="header-actions">
                <el-button type="primary" size="small" @click="refreshReadStatus">刷新</el-button>
              </div>
            </div>
          </template>
          
          <el-table :data="readStatusList" style="width: 100%" stripe>
            <el-table-column prop="realname" label="姓名" width="120"/>
            <el-table-column prop="department" label="部门" width="120"/>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag v-if="scope.row.status === '已读'" type="success">{{ scope.row.status }}</el-tag>
                <el-tag v-else type="warning">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="readTime" label="阅读时间" min-width="150"/>
            <el-table-column prop="ipAddress" label="IP地址" width="120"/>
          </el-table>
        </el-card>
      </div>
    </el-dialog>

    <!-- 发布/编辑通知弹窗 -->
    <el-dialog v-model="notificationFormVisible" :title="notificationFormTitle" width="800px" :before-close="handleFormClose">
      <el-form :model="notificationForm" :rules="notificationRules" ref="notificationFormRef" label-width="120px">
        <el-form-item label="通知标题" prop="title">
          <el-input v-model="notificationForm.title" placeholder="请输入通知标题"/>
        </el-form-item>
        <el-form-item label="通知类别" prop="category">
          <el-select v-model="notificationForm.category" placeholder="请选择通知类别" style="width: 100%">
            <el-option label="公司公告" value="公司公告"/>
            <el-option label="部门通知" value="部门通知"/>
            <el-option label="系统通知" value="系统通知"/>
            <el-option label="活动通知" value="活动通知"/>
            <el-option label="其他" value="其他"/>
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-radio-group v-model="notificationForm.priority">
            <el-radio label="低">低</el-radio>
            <el-radio label="中">中</el-radio>
            <el-radio label="高">高</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="接收部门" prop="targetDepartments">
          <el-select v-model="notificationForm.targetDepartments" multiple placeholder="请选择接收部门" style="width: 100%">
            <el-option label="技术部" value="技术部"/>
            <el-option label="人事部" value="人事部"/>
            <el-option label="财务部" value="财务部"/>
            <el-option label="市场部" value="市场部"/>
            <el-option label="行政部" value="行政部"/>
          </el-select>
        </el-form-item>
        <el-form-item label="通知内容" prop="content">
          <el-input
            v-model="notificationForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入通知内容"
          />
        </el-form-item>
        <el-form-item label="附件">
          <el-upload
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            multiple
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持jpg/png/pdf/doc/docx文件，且不超过10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="发布设置">
          <el-checkbox v-model="notificationForm.urgent">紧急通知</el-checkbox>
          <el-checkbox v-model="notificationForm.requireConfirm">需要确认</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="saveAsDraft">保存草稿</el-button>
          <el-button @click="notificationFormVisible = false">取消</el-button>
          <el-button type="primary" @click="submitNotificationForm">发布通知</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 已读状态弹窗 -->
    <el-dialog v-model="readStatusVisible" title="已读状态详情" width="800px" :before-close="handleReadStatusClose">
      <div class="read-status-detail" v-if="currentReadStatusNotification">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="通知标题">{{ currentReadStatusNotification.title }}</el-descriptions-item>
          <el-descriptions-item label="发布人">{{ currentReadStatusNotification.publisher }}</el-descriptions-item>
          <el-descriptions-item label="发布时间">{{ currentReadStatusNotification.publishTime }}</el-descriptions-item>
          <el-descriptions-item label="总人数">{{ currentReadStatusNotification.totalCount }}</el-descriptions-item>
          <el-descriptions-item label="已读人数">{{ currentReadStatusNotification.readCount }}</el-descriptions-item>
          <el-descriptions-item label="未读人数">{{ currentReadStatusNotification.unreadCount }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="status-summary">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="status-card">
                <div class="status-number">{{ currentReadStatusNotification.readCount }}</div>
                <div class="status-label">已读</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="status-card">
                <div class="status-number">{{ currentReadStatusNotification.unreadCount }}</div>
                <div class="status-label">未读</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="status-card">
                <div class="status-number">{{ currentReadStatusNotification.readRate }}%</div>
                <div class="status-label">已读率</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const notifications = ref([])
const notificationDetailVisible = ref(false)
const currentNotification = ref(null)
const notificationFormVisible = ref(false)
const notificationFormTitle = ref('发布通知')
const notificationFormRef = ref(null)
const readStatusVisible = ref(false)
const currentReadStatusNotification = ref(null)
const fileList = ref([])

// 模拟通知数据
const mockNotifications = [
  {
    id: 'notif001',
    title: '关于公司年度会议的通知',
    category: '公司公告',
    priority: '高',
    status: '已发布',
    publisher: '张经理',
    publishTime: '2024-01-15 09:00:00',
    readCount: 45,
    content: '各位同事，公司将于本周五下午2点在大会议室召开年度总结会议，请各部门负责人准时参加。会议将讨论公司年度业绩、来年规划等重要事项。'
  },
  {
    id: 'notif002',
    title: '系统维护通知',
    category: '系统通知',
    priority: '中',
    status: '已发布',
    publisher: '技术部',
    publishTime: '2024-01-14 18:00:00',
    readCount: 38,
    content: '为了提升系统性能，我们将在今晚22:00-24:00进行系统维护，期间可能影响部分功能的使用，请提前做好准备。'
  },
  {
    id: 'notif003',
    title: '员工福利活动通知',
    category: '活动通知',
    priority: '低',
    status: '草稿',
    publisher: '人事部',
    publishTime: '2024-01-13 10:30:00',
    readCount: 0,
    content: '为增进员工之间的交流，公司将于下周三组织团建活动，活动地点和时间另行通知，请大家踊跃报名参加。'
  }
]

// 模拟已读状态数据
const readStatusList = ref([
  {
    id: 'rs001',
    realname: '张三',
    department: '技术部',
    status: '已读',
    readTime: '2025-01-15 09:15:00',
    ipAddress: '192.168.1.100'
  },
  {
    id: 'rs002',
    realname: '李四',
    department: '人事部',
    status: '已读',
    readTime: '2025-01-15 09:20:00',
    ipAddress: '192.168.1.101'
  },
  {
    id: 'rs003',
    realname: '王五',
    department: '财务部',
    status: '已读',
    readTime: '2025-01-15 09:20:00',
    ipAddress: '192.168.1.101'
  }
])

// 通知表单数据
const notificationForm = ref({
  title: '',
  category: '',
  priority: '中',
  targetDepartments: [],
  content: '',
  urgent: false,
  requireConfirm: false
})

// 表单验证规则
const notificationRules = {
  title: [
    { required: true, message: '请输入通知标题', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择通知类别', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ],
  targetDepartments: [
    { required: true, message: '请选择接收部门', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入通知内容', trigger: 'blur' }
  ]
}

// 方法
const fetchNotifications = async () => {
  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    notifications.value = mockNotifications
    ElMessage.success('通知列表加载成功')
  } catch (e) {
    ElMessage.error('获取通知列表失败')
  }
}

const refreshNotifications = () => {
  fetchNotifications()
}

const createNotification = () => {
  notificationFormTitle.value = '发布通知'
  notificationForm.value = {
    title: '',
    category: '',
    priority: '中',
    targetDepartments: [],
    content: '',
    urgent: false,
    requireConfirm: false
  }
  fileList.value = []
  notificationFormVisible.value = true
}

const editNotification = (notification) => {
  notificationFormTitle.value = '编辑通知'
  notificationForm.value = { ...notification }
  notificationFormVisible.value = true
}

const submitNotificationForm = async () => {
  try {
    await notificationFormRef.value.validate()
    // 模拟提交
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success(notificationFormTitle.value === '发布通知' ? '通知发布成功' : '通知更新成功')
    notificationFormVisible.value = false
    fetchNotifications()
  } catch (error) {
    ElMessage.error('表单验证失败')
  }
}

const saveAsDraft = async () => {
  try {
    await notificationFormRef.value.validate()
    // 模拟保存草稿
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('草稿保存成功')
    notificationFormVisible.value = false
    fetchNotifications()
  } catch (error) {
    ElMessage.error('表单验证失败')
  }
}

const deleteNotification = async (notification) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除通知"${notification.title}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 模拟删除操作
    notifications.value = notifications.value.filter(n => n.id !== notification.id)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}

const viewNotificationDetail = (notification) => {
  currentNotification.value = notification
  notificationDetailVisible.value = true
  loadReadStatus(notification.id)
}

const viewReadStatus = (notification) => {
  currentReadStatusNotification.value = {
    ...notification,
    totalCount: 50,
    unreadCount: 50 - notification.readCount,
    readRate: Math.round((notification.readCount / 50) * 100)
  }
  readStatusVisible.value = true
}

const loadReadStatus = (notificationId) => {
  // 模拟加载已读状态
  readStatusList.value = [
    {
      id: 'rs001',
      realname: '张三',
      department: '技术部',
      status: '已读',
      readTime: '2025-01-15 09:15:00',
      ipAddress: '192.168.1.100'
    },
    {
      id: 'rs002',
      realname: '李四',
      department: '人事部',
      status: '已读',
      readTime: '2025-01-15 09:20:00',
      ipAddress: '192.168.1.101'
    },
    {
      id: 'rs003',
      realname: '王五',
      department: '财务部',
      status: '已读',
      readTime: '2025-01-15 09:20:00',
      ipAddress: '192.168.1.101'
    }
  ]
}

const refreshReadStatus = () => {
  if (currentNotification.value) {
    loadReadStatus(currentNotification.value.id)
    ElMessage.success('已读状态已刷新')
  }
}

const handleFileChange = (file, fileList) => {
  console.log('文件变化:', file, fileList)
}

const handleClose = () => {
  notificationDetailVisible.value = false
  currentNotification.value = null
  readStatusList.value = []
}

const handleFormClose = () => {
  notificationFormVisible.value = false
  notificationFormRef.value?.resetFields()
  fileList.value = []
}

const handleReadStatusClose = () => {
  readStatusVisible.value = false
  currentReadStatusNotification.value = null
}

onMounted(fetchNotifications)
</script>

<style scoped>
.notification-container {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  height: calc(100vh - 160px);
  overflow: auto;
}

.header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.clickable-title {
  color: #409eff;
  cursor: pointer;
}

.clickable-title:hover {
  text-decoration: underline;
}

.notification-detail {
  padding: 20px;
}

.info-card,
.read-status-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.detail-item {
  margin-bottom: 15px;
  display: flex;
  align-items: flex-start;
}

.detail-item label {
  font-weight: bold;
  width: 100px;
  color: #606266;
  flex-shrink: 0;
}

.detail-item span {
  color: #303133;
}

.content-text {
  color: #303133;
  line-height: 1.6;
  white-space: pre-wrap;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-top: 5px;
}

.status-summary {
  margin-top: 20px;
}

.status-card {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.status-number {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.status-label {
  color: #606266;
  font-size: 14px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .notification-container {
    padding: 10px;
  }
  
  .header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
