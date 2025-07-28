<template>
  <div class="language-container">
    <div class="page-header">
      <h2>语言规范管理工作总结</h2>
      <div class="header-actions">
        <el-button type="primary" @click="exportReport">
          <el-icon><Download /></el-icon>
          导出报告
        </el-button>
        <el-button type="success" @click="showAddWorkDialog">
          <el-icon><Plus /></el-icon>
          添加工作记录
        </el-button>
      </div>
    </div>

    <!-- 工作概览 -->
    <div class="overview-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon success">
                <el-icon><Check /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">普通话达标率</div>
                <div class="card-value">90%+</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card" @click="goToEmployee" style="cursor:pointer;">
            <div class="card-content">
              <div class="card-icon primary">
                <el-icon><Document /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">规范制度</div>
                <div class="card-value">15项</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon warning">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">待整改问题</div>
                <div class="card-value">8项</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon info">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">文明程度提升</div>
                <div class="card-value">显著</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 主要工作内容 -->
        <el-tab-pane label="主要工作内容" name="work">
          <div class="work-content">
            <el-timeline>
              <el-timeline-item
                v-for="(work, index) in workItems"
                :key="index"
                :timestamp="work.timestamp"
                :type="work.type"
                :color="work.color"
              >
                <el-card>
                  <template #header>
                    <div class="card-header">
                      <span class="work-title">{{ work.title }}</span>
                      <el-tag :type="work.status" size="small">{{ work.statusText }}</el-tag>
                    </div>
                  </template>
                  <div class="work-description">{{ work.description }}</div>
                  <div class="work-details" v-if="work.details">
                    <div v-for="(detail, idx) in work.details" :key="idx" class="detail-item">
                      <el-icon><CircleCheck /></el-icon>
                      <span>{{ detail }}</span>
                    </div>
                  </div>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-tab-pane>

        <!-- 实施成效 -->
        <el-tab-pane label="实施成效" name="results">
          <div class="results-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card class="result-card">
                  <template #header>
                    <div class="card-header">
                      <span>教职工普通话达标情况</span>
                    </div>
                  </template>
                  <div class="result-item">
                    <div class="result-label">普通话等级证书获得率</div>
                    <el-progress :percentage="90" :color="customColors" />
                    <div class="result-desc">90%以上教职工取得普通话等级证书</div>
                  </div>
                  <div class="result-item">
                    <div class="result-label">教学检查评分标准</div>
                    <el-progress :percentage="85" :color="customColors" />
                    <div class="result-desc">语言规范作为重要评分标准</div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card class="result-card">
                  <template #header>
                    <div class="card-header">
                      <span>网络语言文明程度</span>
                    </div>
                  </template>
                  <div class="result-item">
                    <div class="result-label">不规范用语现象减少</div>
                    <el-progress :percentage="75" :color="customColors" />
                    <div class="result-desc">公共场所不规范用语现象显著减少</div>
                  </div>
                  <div class="result-item">
                    <div class="result-label">校园普通话使用率</div>
                    <el-progress :percentage="95" :color="customColors" />
                    <div class="result-desc">教学、会议、活动全流程使用普通话</div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <!-- 存在问题 -->
        <el-tab-pane label="存在问题" name="problems">
          <div class="problems-content">
            <el-alert
              v-for="(problem, index) in problems"
              :key="index"
              :title="problem.title"
              :description="problem.description"
              :type="problem.type"
              :closable="false"
              show-icon
              class="problem-alert"
            />
          </div>
        </el-tab-pane>

        <!-- 未来计划 -->
        <el-tab-pane label="未来计划" name="plans">
          <div class="plans-content">
            <el-steps :active="2" direction="vertical" finish-status="success">
              <el-step
                v-for="(plan, index) in futurePlans"
                :key="index"
                :title="plan.title"
                :description="plan.description"
              />
            </el-steps>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 添加工作记录对话框 -->
    <el-dialog
      v-model="workDialogVisible"
      title="添加工作记录"
      width="600px"
      @close="resetWorkForm"
    >
      <el-form :model="workForm" :rules="workRules" ref="workFormRef" label-width="100px">
        <el-form-item label="工作标题" prop="title">
          <el-input v-model="workForm.title" placeholder="请输入工作标题" />
        </el-form-item>
        <el-form-item label="工作类型" prop="type">
          <el-select v-model="workForm.type" placeholder="请选择工作类型" style="width: 100%">
            <el-option label="组织机构建设" value="organization" />
            <el-option label="宣传教育" value="education" />
            <el-option label="专项整治" value="special" />
            <el-option label="制度建设" value="system" />
          </el-select>
        </el-form-item>
        <el-form-item label="工作描述" prop="description">
          <el-input
            v-model="workForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入工作描述"
          />
        </el-form-item>
        <el-form-item label="完成状态" prop="status">
          <el-select v-model="workForm.status" placeholder="请选择完成状态" style="width: 100%">
            <el-option label="已完成" value="success" />
            <el-option label="进行中" value="warning" />
            <el-option label="待开始" value="info" />
          </el-select>
        </el-form-item>
        <el-form-item label="完成时间" prop="completionTime">
          <el-date-picker
            v-model="workForm.completionTime"
            type="date"
            placeholder="选择完成时间"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="workDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitWorkForm" :loading="submitting">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Check, Document, Warning, TrendCharts, CircleCheck } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

// 响应式数据
const submitting = ref(false)
const workDialogVisible = ref(false)
const workFormRef = ref()
const activeTab = ref('work')

// 工作表单
const workForm = reactive({
  title: '',
  type: '',
  description: '',
  status: 'success',
  completionTime: ''
})

// 表单验证规则
const workRules = {
  title: [
    { required: true, message: '请输入工作标题', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择工作类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入工作描述', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择完成状态', trigger: 'change' }
  ]
}

// 进度条颜色
const customColors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 }
]

// 主要工作内容
const workItems = ref([
  {
    title: '组织机构建设',
    description: '成立语言规范整治工作领导小组，明确职责分工，确保工作有序开展。',
    timestamp: '2024年1月',
    type: 'primary',
    color: '#409eff',
    status: 'success',
    statusText: '已完成',
    details: [
      '成立专项工作领导小组',
      '制定详细的工作计划',
      '明确各部门职责分工',
      '建立工作协调机制'
    ]
  },
  {
    title: '宣传教育',
    description: '通过广播、电视、网络等渠道普及语言规范知识，增强公众意识。',
    timestamp: '2024年2月',
    type: 'success',
    color: '#67c23a',
    status: 'success',
    statusText: '已完成',
    details: [
      '制作语言规范宣传材料',
      '开展线上线下宣传活动',
      '组织语言规范知识讲座',
      '建立宣传教育长效机制'
    ]
  },
  {
    title: '专项整治',
    description: '针对网络用语、广告宣传、商品包装等领域开展不规范用语用字整治行动。',
    timestamp: '2024年3月',
    type: 'warning',
    color: '#e6a23c',
    status: 'warning',
    statusText: '进行中',
    details: [
      '网络用语规范整治',
      '广告宣传用语检查',
      '商品包装文字审核',
      '公共场所标识规范'
    ]
  },
  {
    title: '制度建设',
    description: '将语言规范纳入考核体系，例如教师职称评定与普通话水平挂钩，学生日常行为规范中也包含语言规范要求。',
    timestamp: '2024年4月',
    type: 'info',
    color: '#909399',
    status: 'info',
    statusText: '待开始',
    details: [
      '制定语言规范考核标准',
      '建立教师普通话等级要求',
      '完善学生行为规范制度',
      '建立监督检查机制'
    ]
  }
])

// 存在问题
const problems = ref([
  {
    title: '地区发展不均衡',
    description: '部分地区和单位对语言规范重视不足，推进速度不均衡。需要加强统筹协调，确保工作全面推进。',
    type: 'warning'
  },
  {
    title: '应用能力待提升',
    description: '从业人员语言应用能力仍需提升，尤其在审计等特定领域存在应用不规范问题。需要加强培训和实践。',
    type: 'error'
  },
  {
    title: '长效机制待完善',
    description: '语言规范工作的长效机制需要进一步完善，确保工作的持续性和有效性。',
    type: 'info'
  }
])

// 未来计划
const futurePlans = ref([
  {
    title: '建立长效机制',
    description: '强化制度执行，确保语言规范工作持续有效开展。'
  },
  {
    title: '持续专项整治',
    description: '针对重点领域和突出问题，持续开展专项整治行动。'
  },
  {
    title: '纳入年度考核',
    description: '将语言规范工作纳入年度考核体系，确保工作落实到位。'
  },
  {
    title: '加强培训教育',
    description: '定期开展语言规范培训，提升从业人员应用能力。'
  }
])

// 方法
const showAddWorkDialog = () => {
  workDialogVisible.value = true
}

const submitWorkForm = async () => {
  if (!workFormRef.value) return
  
  try {
    await workFormRef.value.validate()
    submitting.value = true
    
    // 模拟提交操作
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newWork = {
      title: workForm.title,
      description: workForm.description,
      timestamp: new Date().toLocaleDateString(),
      type: 'primary',
      color: '#409eff',
      status: workForm.status,
      statusText: getStatusText(workForm.status)
    }
    
    workItems.value.push(newWork)
    ElMessage.success('工作记录添加成功')
    
    workDialogVisible.value = false
    resetWorkForm()
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    submitting.value = false
  }
}

const resetWorkForm = () => {
  if (workFormRef.value) {
    workFormRef.value.resetFields()
  }
  Object.assign(workForm, {
    title: '',
    type: '',
    description: '',
    status: 'success',
    completionTime: ''
  })
}

const getStatusText = (status) => {
  const statusMap = {
    success: '已完成',
    warning: '进行中',
    info: '待开始'
  }
  return statusMap[status] || '未知'
}

const exportReport = () => {
  // 模拟导出报告功能
  ElMessage.success('语言规范管理工作总结报告导出成功')
}

const router = useRouter()

function goToEmployee() {
  router.push('/filemanage')
}

// 生命周期
onMounted(() => {
  // 初始化数据
})
</script>

<style scoped>
.language-container {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.page-header h2 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.overview-section {
  margin-bottom: 30px;
}

.overview-card {
  height: 120px;
  transition: all 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.card-icon.success {
  background: linear-gradient(135deg, #67c23a, #85ce61);
}

.card-icon.primary {
  background: linear-gradient(135deg, #409eff, #66b1ff);
}

.card-icon.warning {
  background: linear-gradient(135deg, #e6a23c, #ebb563);
}

.card-icon.info {
  background: linear-gradient(135deg, #909399, #a6a9ad);
}

.card-info {
  flex: 1;
}

.card-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.content-section {
  margin-top: 30px;
}

.work-content {
  padding: 20px 0;
}

.work-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.work-description {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
}

.work-details {
  margin-top: 15px;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  color: #606266;
}

.detail-item .el-icon {
  color: #67c23a;
  margin-right: 8px;
  font-size: 14px;
}

.results-content {
  padding: 20px 0;
}

.result-card {
  margin-bottom: 20px;
}

.result-item {
  margin-bottom: 25px;
}

.result-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.result-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.problems-content {
  padding: 20px 0;
}

.problem-alert {
  margin-bottom: 15px;
}

.plans-content {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-timeline-item__node) {
  background-color: #409eff;
}

:deep(.el-timeline-item__tail) {
  border-left-color: #e4e7ed;
}

:deep(.el-card__header) {
  background-color: #f8f9fa;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
}

:deep(.el-progress-bar__outer) {
  background-color: #f0f2f5;
}

:deep(.el-steps) {
  padding: 20px 0;
}

:deep(.el-step__title) {
  font-size: 16px;
  font-weight: 500;
}

:deep(.el-step__description) {
  color: #606266;
  line-height: 1.6;
}
</style> 