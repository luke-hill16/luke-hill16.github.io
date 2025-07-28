<template>
  <div class="exam-container">
    <el-card>
      <div class="header">
        <span>员工考试管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="createExam" size="small">创建考试</el-button>
          <el-button type="success" @click="refreshExams" size="small">刷新</el-button>
        </div>
      </div>
      
      <!-- 考试列表 -->
      <el-table :data="exams" style="width: 100%; margin-top: 20px;" fit="true">
        <el-table-column prop="title" label="考试标题" min-width="200">
          <template #default="scope">
            <span class="clickable-title" @click="viewExamDetail(scope.row)">{{ scope.row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="考试类别" min-width="120"/>
        <el-table-column prop="duration" label="考试时长" min-width="100">
          <template #default="scope">
            <span>{{ scope.row.duration }}分钟</span>
          </template>
        </el-table-column>
        <el-table-column prop="totalScore" label="总分" min-width="80"/>
        <el-table-column prop="passScore" label="及格分" min-width="80"/>
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === '进行中'" type="success">{{ scope.row.status }}</el-tag>
            <el-tag v-else-if="scope.row.status === '已结束'" type="info">{{ scope.row.status }}</el-tag>
            <el-tag v-else type="warning">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="startTime" label="开始时间" min-width="150"/>
        <el-table-column prop="endTime" label="结束时间" min-width="150"/>
        <el-table-column label="操作" min-width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="editExam(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="viewResults(scope.row)">查看成绩</el-button>
            <el-button size="small" type="danger" @click="deleteExam(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 考试详情弹窗 -->
    <el-dialog v-model="examDetailVisible" title="考试详情" width="1000px" :before-close="handleClose">
      <div class="exam-detail" v-if="currentExam">
        <!-- 考试基本信息 -->
        <el-card class="info-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>考试信息</span>
              <el-button type="primary" size="small" @click="editExam(currentExam)">编辑考试</el-button>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="detail-item">
                <label>考试标题：</label>
                <span>{{ currentExam.title }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <label>考试类别：</label>
                <span>{{ currentExam.category }}</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <label>考试时长：</label>
                <span>{{ currentExam.duration }}分钟</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="detail-item">
                <label>总分：</label>
                <span>{{ currentExam.totalScore }}分</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <label>及格分：</label>
                <span>{{ currentExam.passScore }}分</span>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="detail-item">
                <label>状态：</label>
                <el-tag v-if="currentExam.status === '进行中'" type="success">{{ currentExam.status }}</el-tag>
                <el-tag v-else-if="currentExam.status === '已结束'" type="info">{{ currentExam.status }}</el-tag>
                <el-tag v-else type="warning">{{ currentExam.status }}</el-tag>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>开始时间：</label>
                <span>{{ currentExam.startTime }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>结束时间：</label>
                <span>{{ currentExam.endTime }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="detail-item">
                <label>考试说明：</label>
                <span>{{ currentExam.description }}</span>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <!-- 题目列表 -->
        <el-card class="questions-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>题目列表</span>
              <div class="header-actions">
                <el-button type="success" size="small" @click="addQuestion">添加题目</el-button>
                <el-button type="primary" size="small" @click="refreshQuestions">刷新</el-button>
              </div>
            </div>
          </template>
          
          <el-table :data="questions" style="width: 100%" stripe>
            <el-table-column prop="order" label="序号" width="80"/>
            <el-table-column prop="type" label="题型" width="100">
              <template #default="scope">
                <el-tag v-if="scope.row.type === '单选题'" type="primary">{{ scope.row.type }}</el-tag>
                <el-tag v-else-if="scope.row.type === '多选题'" type="success">{{ scope.row.type }}</el-tag>
                <el-tag v-else-if="scope.row.type === '判断题'" type="warning">{{ scope.row.type }}</el-tag>
                <el-tag v-else type="info">{{ scope.row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="题目内容" min-width="300"/>
            <el-table-column prop="score" label="分值" width="80"/>
            <el-table-column prop="difficulty" label="难度" width="100">
              <template #default="scope">
                <el-tag v-if="scope.row.difficulty === '简单'" type="success">{{ scope.row.difficulty }}</el-tag>
                <el-tag v-else-if="scope.row.difficulty === '中等'" type="warning">{{ scope.row.difficulty }}</el-tag>
                <el-tag v-else type="danger">{{ scope.row.difficulty }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" @click="editQuestion(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteQuestion(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 参与人员 -->
        <el-card class="participants-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>参与人员</span>
              <div class="header-actions">
                <el-button type="success" size="small" @click="addParticipant">添加人员</el-button>
                <el-button type="primary" size="small" @click="refreshParticipants">刷新</el-button>
              </div>
            </div>
          </template>
          
          <el-table :data="participants" style="width: 100%" stripe>
            <el-table-column prop="realname" label="姓名" width="120"/>
            <el-table-column prop="department" label="部门" width="120"/>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag v-if="scope.row.status === '已完成'" type="success">{{ scope.row.status }}</el-tag>
                <el-tag v-else-if="scope.row.status === '进行中'" type="warning">{{ scope.row.status }}</el-tag>
                <el-tag v-else type="info">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="score" label="得分" width="100"/>
            <el-table-column prop="startTime" label="开始时间" min-width="150"/>
            <el-table-column prop="endTime" label="结束时间" min-width="150"/>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" @click="viewParticipantDetail(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-dialog>

    <!-- 创建/编辑考试弹窗 -->
    <el-dialog v-model="examFormVisible" :title="examFormTitle" width="800px" :before-close="handleFormClose">
      <el-form :model="examForm" :rules="examRules" ref="examFormRef" label-width="120px">
        <el-form-item label="考试标题" prop="title">
          <el-input v-model="examForm.title" placeholder="请输入考试标题"/>
        </el-form-item>
        <el-form-item label="考试类别" prop="category">
          <el-select v-model="examForm.category" placeholder="请选择考试类别" style="width: 100%">
            <el-option label="安全培训" value="安全培训"/>
            <el-option label="技能考核" value="技能考核"/>
            <el-option label="制度学习" value="制度学习"/>
            <el-option label="岗位培训" value="岗位培训"/>
            <el-option label="其他" value="其他"/>
          </el-select>
        </el-form-item>
        <el-form-item label="考试时长" prop="duration">
          <el-input-number v-model="examForm.duration" :min="1" :max="300" placeholder="分钟"/>
        </el-form-item>
        <el-form-item label="总分" prop="totalScore">
          <el-input-number v-model="examForm.totalScore" :min="1" :max="100" placeholder="分"/>
        </el-form-item>
        <el-form-item label="及格分" prop="passScore">
          <el-input-number v-model="examForm.passScore" :min="1" :max="examForm.totalScore" placeholder="分"/>
        </el-form-item>
        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker
            v-model="examForm.startTime"
            type="datetime"
            placeholder="选择开始时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker
            v-model="examForm.endTime"
            type="datetime"
            placeholder="选择结束时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="考试说明" prop="description">
          <el-input
            v-model="examForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入考试说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="examFormVisible = false">取消</el-button>
          <el-button type="primary" @click="submitExamForm">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const exams = ref([])
const examDetailVisible = ref(false)
const currentExam = ref(null)
const examFormVisible = ref(false)
const examFormTitle = ref('创建考试')
const examFormRef = ref(null)

// 模拟考试数据
const mockExams = [
  {
    id: 'exam001',
    title: '安全生产知识考试',
    category: '安全培训',
    duration: 60,
    totalScore: 100,
    passScore: 60,
    status: '进行中',
    startTime: '2024-01-15 09:00:00',
    endTime: '2024-01-20 18:00:00',
    description: '本次考试主要考察员工对安全生产知识的掌握程度，包括安全操作规程、应急处理等内容。'
  },
  {
    id: 'exam002',
    title: '公司制度学习考试',
    category: '制度学习',
    duration: 45,
    totalScore: 100,
    passScore: 70,
    status: '已结束',
    startTime: '2024-01-10 09:00:00',
    endTime: '2024-01-12 18:00:00',
    description: '考察员工对公司各项制度的了解程度，包括人事制度、财务制度、行政制度等。'
  },
  {
    id: 'exam003',
    title: '专业技能考核',
    category: '技能考核',
    duration: 90,
    totalScore: 100,
    passScore: 80,
    status: '未开始',
    startTime: '2024-01-25 09:00:00',
    endTime: '2024-01-30 18:00:00',
    description: '针对技术部门员工的专业技能考核，包括编程能力、系统设计等。'
  }
]

// 模拟题目数据
const questions = ref([
  {
    id: 'q001',
    order: 1,
    type: '单选题',
    content: '在发生火灾时，以下哪种做法是正确的？',
    score: 10,
    difficulty: '简单'
  },
  {
    id: 'q002',
    order: 2,
    type: '多选题',
    content: '以下哪些是安全生产的基本原则？',
    score: 15,
    difficulty: '中等'
  },
  {
    id: 'q003',
    order: 3,
    type: '判断题',
    content: '员工在工作时必须佩戴安全帽。',
    score: 5,
    difficulty: '简单'
  }
])

// 模拟参与人员数据
const participants = ref([
  {
    id: 'p001',
    realname: '张三',
    department: '技术部',
    status: '已完成',
    score: 85,
    startTime: '2024-01-15 10:30:00',
    endTime: '2024-01-15 11:25:00'
  },
  {
    id: 'p002',
    realname: '李四',
    department: '人事部',
    status: '进行中',
    score: null,
    startTime: '2024-01-15 14:20:00',
    endTime: null
  },
  {
    id: 'p003',
    realname: '王五',
    department: '财务部',
    status: '未开始',
    score: null,
    startTime: null,
    endTime: null
  }
])

// 考试表单数据
const examForm = ref({
  title: '',
  category: '',
  duration: 60,
  totalScore: 100,
  passScore: 60,
  startTime: '',
  endTime: '',
  description: ''
})

// 表单验证规则
const examRules = {
  title: [
    { required: true, message: '请输入考试标题', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择考试类别', trigger: 'change' }
  ],
  duration: [
    { required: true, message: '请输入考试时长', trigger: 'blur' }
  ],
  totalScore: [
    { required: true, message: '请输入总分', trigger: 'blur' }
  ],
  passScore: [
    { required: true, message: '请输入及格分', trigger: 'blur' }
  ],
  startTime: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  endTime: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ]
}

// 方法
const fetchExams = async () => {
  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    exams.value = mockExams
    ElMessage.success('考试列表加载成功')
  } catch (e) {
    ElMessage.error('获取考试列表失败')
  }
}

const refreshExams = () => {
  fetchExams()
}

const createExam = () => {
  examFormTitle.value = '创建考试'
  examForm.value = {
    title: '',
    category: '',
    duration: 60,
    totalScore: 100,
    passScore: 60,
    startTime: '',
    endTime: '',
    description: ''
  }
  examFormVisible.value = true
}

const editExam = (exam) => {
  examFormTitle.value = '编辑考试'
  examForm.value = { ...exam }
  examFormVisible.value = true
}

const submitExamForm = async () => {
  try {
    await examFormRef.value.validate()
    // 模拟提交
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success(examFormTitle.value === '创建考试' ? '考试创建成功' : '考试更新成功')
    examFormVisible.value = false
    fetchExams()
  } catch (error) {
    ElMessage.error('表单验证失败')
  }
}

const deleteExam = async (exam) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除考试"${exam.title}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 模拟删除操作
    exams.value = exams.value.filter(e => e.id !== exam.id)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}

const viewExamDetail = (exam) => {
  currentExam.value = exam
  examDetailVisible.value = true
}

const viewResults = (exam) => {
  ElMessage.info(`查看考试"${exam.title}"的成绩`)
  // 这里可以实现查看成绩的逻辑
}

const addQuestion = () => {
  ElMessage.info('添加题目功能')
  // 这里可以实现添加题目的逻辑
}

const editQuestion = (question) => {
  ElMessage.info(`编辑题目: ${question.content}`)
  // 这里可以实现编辑题目的逻辑
}

const deleteQuestion = async (question) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除题目"${question.content}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 模拟删除操作
    questions.value = questions.value.filter(q => q.id !== question.id)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}

const addParticipant = () => {
  ElMessage.info('添加参与人员功能')
  // 这里可以实现添加参与人员的逻辑
}

const viewParticipantDetail = (participant) => {
  ElMessage.info(`查看${participant.realname}的考试详情`)
  // 这里可以实现查看参与人员详情的逻辑
}

const refreshQuestions = () => {
  ElMessage.success('题目列表已刷新')
}

const refreshParticipants = () => {
  ElMessage.success('参与人员列表已刷新')
}

const handleClose = () => {
  examDetailVisible.value = false
  currentExam.value = null
}

const handleFormClose = () => {
  examFormVisible.value = false
  examFormRef.value?.resetFields()
}

onMounted(fetchExams)
</script>

<style scoped>
.exam-container {
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

.exam-detail {
  padding: 20px;
}

.info-card,
.questions-card,
.participants-card {
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
  align-items: center;
}

.detail-item label {
  font-weight: bold;
  width: 100px;
  color: #606266;
}

.detail-item span {
  color: #303133;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .exam-container {
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
