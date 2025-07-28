<template>
  <div class="education-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>教育管理</span>
        </div>
      </template>
      
      <!-- Tab标签页 -->
      <el-tabs v-model="activeTab" type="card" class="education-tabs">
        <!-- 试卷管理Tab -->
        <el-tab-pane label="试卷管理" name="exam">
          <div class="tab-content">
            <!-- 试卷搜索区域 -->
            <div class="search-area">
              <el-form :inline="true" :model="examSearchForm" class="search-form">
                <el-form-item label="试卷名称">
                  <el-input v-model="examSearchForm.name" placeholder="请输入试卷名称" clearable />
                </el-form-item>
                <el-form-item label="试卷类型">
                  <el-select v-model="examSearchForm.type" placeholder="请选择试卷类型" clearable style="width: 180px;">
                    <el-option label="期中考试" value="midterm" />
                    <el-option label="期末考试" value="final" />
                    <el-option label="模拟考试" value="mock" />
                    <el-option label="单元测试" value="unit" />
                  </el-select>
                </el-form-item>
                <el-form-item label="状态">
                  <el-select v-model="examSearchForm.status" placeholder="请选择状态" clearable style="width: 180px;">
                    <el-option label="草稿" value="draft" />
                    <el-option label="已发布" value="published" />
                    <el-option label="已结束" value="ended" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleExamSearch">搜索</el-button>
                  <el-button @click="handleExamReset">重置</el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 试卷操作按钮 -->
            <div class="action-bar">
              <el-button type="primary" @click="handleAddExam">新增试卷</el-button>
            </div>

            <!-- 试卷表格 -->
            <el-table :data="examTableData" style="width: 100%" v-loading="examLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="试卷名称" />
              <el-table-column prop="type" label="试卷类型" width="120">
                <template #default="scope">
                  <el-tag :type="getExamTypeTagType(scope.row.type)">
                    {{ getExamTypeLabel(scope.row.type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="totalScore" label="总分" width="80" />
              <el-table-column prop="duration" label="考试时长(分钟)" width="120" />
              <el-table-column prop="questionCount" label="题目数量" width="100" />
              <el-table-column prop="createTime" label="创建时间" width="120" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getExamStatusTagType(scope.row.status)">
                    {{ getExamStatusLabel(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="handleEditExam(scope.row)">编辑</el-button>
                  <el-button size="small" type="success" @click="handleViewExam(scope.row)">查看</el-button>
                  <el-button size="small" type="warning" @click="handleManageQuestions(scope.row)">管理题目</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteExam(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <!-- 试卷分页 -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="examCurrentPage"
                v-model:page-size="examPageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="examTotal"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleExamSizeChange"
                @current-change="handleExamCurrentChange"
              />
            </div>
          </div>
        </el-tab-pane>

        <!-- 试题管理Tab -->
        <el-tab-pane label="试题管理" name="question">
          <div class="tab-content">
            <!-- 试题搜索区域 -->
            <div class="search-area">
              <el-form :inline="true" :model="questionSearchForm" class="search-form">
                <el-form-item label="题目内容">
                  <el-input v-model="questionSearchForm.content" placeholder="请输入题目内容" clearable />
                </el-form-item>
                <el-form-item label="题目类型">
                  <el-select v-model="questionSearchForm.type" placeholder="请选择题目类型" clearable style="width: 180px;">
                    <el-option label="单选题" value="single" />
                    <el-option label="多选题" value="multiple" />
                    <el-option label="判断题" value="judge" />
                    <el-option label="填空题" value="fill" />
                    <el-option label="简答题" value="short" />
                  </el-select>
                </el-form-item>
                <el-form-item label="难度">
                  <el-select v-model="questionSearchForm.difficulty" placeholder="请选择难度" clearable style="width: 180px;">
                    <el-option label="简单" value="easy" />
                    <el-option label="中等" value="medium" />
                    <el-option label="困难" value="hard" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleQuestionSearch">搜索</el-button>
                  <el-button @click="handleQuestionReset">重置</el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 试题操作按钮 -->
            <div class="action-bar">
              <el-button type="primary" @click="handleAddQuestion">新增试题</el-button>
            </div>

            <!-- 试题表格 -->
            <el-table :data="questionTableData" style="width: 100%" v-loading="questionLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="content" label="题目内容" show-overflow-tooltip />
              <el-table-column prop="type" label="题目类型" width="100">
                <template #default="scope">
                  <el-tag :type="getQuestionTypeTagType(scope.row.type)">
                    {{ getQuestionTypeLabel(scope.row.type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="difficulty" label="难度" width="80">
                <template #default="scope">
                  <el-tag :type="getDifficultyTagType(scope.row.difficulty)">
                    {{ getDifficultyLabel(scope.row.difficulty) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="score" label="分值" width="80" />
              <el-table-column prop="subject" label="科目" width="100" />
              <el-table-column prop="createTime" label="创建时间" width="120" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="handleEditQuestion(scope.row)">编辑</el-button>
                  <el-button size="small" type="success" @click="handleViewQuestion(scope.row)">查看</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteQuestion(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <!-- 试题分页 -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="questionCurrentPage"
                v-model:page-size="questionPageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="questionTotal"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleQuestionSizeChange"
                @current-change="handleQuestionCurrentChange"
              />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 试卷新增/编辑对话框 -->
    <el-dialog v-model="examDialogVisible" :title="examDialogTitle" width="700px">
      <el-form :model="examForm" :rules="examRules" ref="examFormRef" label-width="100px">
        <el-form-item label="试卷名称" prop="name">
          <el-input v-model="examForm.name" placeholder="请输入试卷名称" />
        </el-form-item>
        <el-form-item label="试卷类型" prop="type">
          <el-select v-model="examForm.type" placeholder="请选择试卷类型" style="width: 100%">
            <el-option label="期中考试" value="midterm" />
            <el-option label="期末考试" value="final" />
            <el-option label="模拟考试" value="mock" />
            <el-option label="单元测试" value="unit" />
          </el-select>
        </el-form-item>
        <el-form-item label="总分" prop="totalScore">
          <el-input-number v-model="examForm.totalScore" :min="0" :max="200" style="width: 100%" />
        </el-form-item>
        <el-form-item label="考试时长(分钟)" prop="duration">
          <el-input-number v-model="examForm.duration" :min="30" :max="300" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="examForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="已结束" value="ended" />
          </el-select>
        </el-form-item>
        <el-form-item label="试卷说明" prop="description">
          <el-input v-model="examForm.description" type="textarea" :rows="3" placeholder="请输入试卷说明" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="examDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleExamSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 试题新增/编辑对话框 -->
    <el-dialog v-model="questionDialogVisible" :title="questionDialogTitle" width="800px">
      <el-form :model="questionForm" :rules="questionRules" ref="questionFormRef" label-width="100px">
        <el-form-item label="题目内容" prop="content">
          <el-input v-model="questionForm.content" type="textarea" :rows="4" placeholder="请输入题目内容" />
        </el-form-item>
        <el-form-item label="题目类型" prop="type">
          <el-select v-model="questionForm.type" placeholder="请选择题目类型" style="width: 100%">
            <el-option label="单选题" value="single" />
            <el-option label="多选题" value="multiple" />
            <el-option label="判断题" value="judge" />
            <el-option label="填空题" value="fill" />
            <el-option label="简答题" value="short" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="questionForm.difficulty" placeholder="请选择难度" style="width: 100%">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="分值" prop="score">
          <el-input-number v-model="questionForm.score" :min="1" :max="50" style="width: 100%" />
        </el-form-item>
        <el-form-item label="科目" prop="subject">
          <el-input v-model="questionForm.subject" placeholder="请输入科目" />
        </el-form-item>
        
        <!-- 选项（仅选择题显示） -->
        <template v-if="questionForm.type === 'single' || questionForm.type === 'multiple'">
          <el-form-item label="选项A" prop="optionA">
            <el-input v-model="questionForm.optionA" placeholder="请输入选项A" />
          </el-form-item>
          <el-form-item label="选项B" prop="optionB">
            <el-input v-model="questionForm.optionB" placeholder="请输入选项B" />
          </el-form-item>
          <el-form-item label="选项C" prop="optionC">
            <el-input v-model="questionForm.optionC" placeholder="请输入选项C" />
          </el-form-item>
          <el-form-item label="选项D" prop="optionD">
            <el-input v-model="questionForm.optionD" placeholder="请输入选项D" />
          </el-form-item>
        </template>
        
        <!-- 答案 -->
        <el-form-item label="正确答案" prop="answer">
          <el-input v-model="questionForm.answer" placeholder="请输入正确答案" />
        </el-form-item>
        
        <el-form-item label="解析" prop="analysis">
          <el-input v-model="questionForm.analysis" type="textarea" :rows="3" placeholder="请输入题目解析" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="questionDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleQuestionSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 当前激活的tab
const activeTab = ref('exam')

// 试卷相关数据
const examLoading = ref(false)
const examDialogVisible = ref(false)
const examDialogTitle = ref('新增试卷')
const examCurrentPage = ref(1)
const examPageSize = ref(10)
const examTotal = ref(0)
const examFormRef = ref()

// 试题相关数据
const questionLoading = ref(false)
const questionDialogVisible = ref(false)
const questionDialogTitle = ref('新增试题')
const questionCurrentPage = ref(1)
const questionPageSize = ref(10)
const questionTotal = ref(0)
const questionFormRef = ref()

// 试卷搜索表单
const examSearchForm = reactive({
  name: '',
  type: '',
  status: ''
})

// 试题搜索表单
const questionSearchForm = reactive({
  content: '',
  type: '',
  difficulty: ''
})

// 试卷表格数据
const examTableData = ref([
  {
    id: 1,
    name: '2024年春季期中考试',
    type: 'midterm',
    totalScore: 100,
    duration: 120,
    questionCount: 25,
    createTime: '2024-03-15',
    status: 'published',
    description: '春季学期期中考试试卷'
  },
  {
    id: 2,
    name: '数学单元测试一',
    type: 'unit',
    totalScore: 50,
    duration: 60,
    questionCount: 15,
    createTime: '2024-03-10',
    status: 'draft',
    description: '第一章函数单元测试'
  },
  {
    id: 3,
    name: '高考模拟考试',
    type: 'mock',
    totalScore: 150,
    duration: 180,
    questionCount: 35,
    createTime: '2024-03-01',
    status: 'ended',
    description: '高考模拟考试试卷'
  }
])

// 试题表格数据
const questionTableData = ref([
  {
    id: 1,
    content: '下列哪个是JavaScript的基本数据类型？',
    type: 'single',
    difficulty: 'easy',
    score: 5,
    subject: '计算机科学',
    createTime: '2024-03-15',
    answer: 'A',
    analysis: 'JavaScript的基本数据类型包括：Number、String、Boolean、Undefined、Null、Symbol、BigInt'
  },
  {
    id: 2,
    content: '请简述面向对象编程的三大特性。',
    type: 'short',
    difficulty: 'medium',
    score: 10,
    subject: '计算机科学',
    createTime: '2024-03-14',
    answer: '封装、继承、多态',
    analysis: '面向对象编程的三大特性是封装、继承和多态，这是面向对象编程的核心概念。'
  },
  {
    id: 3,
    content: '1 + 1 = 2',
    type: 'judge',
    difficulty: 'easy',
    score: 2,
    subject: '数学',
    createTime: '2024-03-13',
    answer: '正确',
    analysis: '1加1等于2是基本的数学运算。'
  }
])

// 试卷表单数据
const examForm = reactive({
  id: null,
  name: '',
  type: '',
  totalScore: 100,
  duration: 120,
  status: 'draft',
  description: ''
})

// 试题表单数据
const questionForm = reactive({
  id: null,
  content: '',
  type: '',
  difficulty: '',
  score: 5,
  subject: '',
  optionA: '',
  optionB: '',
  optionC: '',
  optionD: '',
  answer: '',
  analysis: ''
})

// 试卷表单验证规则
const examRules = {
  name: [
    { required: true, message: '请输入试卷名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择试卷类型', trigger: 'change' }
  ],
  totalScore: [
    { required: true, message: '请输入总分', trigger: 'blur' }
  ],
  duration: [
    { required: true, message: '请输入考试时长', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 试题表单验证规则
const questionRules = {
  content: [
    { required: true, message: '请输入题目内容', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择题目类型', trigger: 'change' }
  ],
  difficulty: [
    { required: true, message: '请选择难度', trigger: 'change' }
  ],
  score: [
    { required: true, message: '请输入分值', trigger: 'blur' }
  ],
  subject: [
    { required: true, message: '请输入科目', trigger: 'blur' }
  ],
  answer: [
    { required: true, message: '请输入正确答案', trigger: 'blur' }
  ]
}

// 试卷类型标签样式
const getExamTypeTagType = (type) => {
  const typeMap = {
    midterm: 'warning',
    final: 'danger',
    mock: 'info',
    unit: 'success'
  }
  return typeMap[type] || 'info'
}

// 试卷类型标签文本
const getExamTypeLabel = (type) => {
  const typeMap = {
    midterm: '期中考试',
    final: '期末考试',
    mock: '模拟考试',
    unit: '单元测试'
  }
  return typeMap[type] || '未知'
}

// 试卷状态标签样式
const getExamStatusTagType = (status) => {
  const statusMap = {
    draft: 'info',
    published: 'success',
    ended: 'warning'
  }
  return statusMap[status] || 'info'
}

// 试卷状态标签文本
const getExamStatusLabel = (status) => {
  const statusMap = {
    draft: '草稿',
    published: '已发布',
    ended: '已结束'
  }
  return statusMap[status] || '未知'
}

// 题目类型标签样式
const getQuestionTypeTagType = (type) => {
  const typeMap = {
    single: 'primary',
    multiple: 'success',
    judge: 'warning',
    fill: 'info',
    short: 'danger'
  }
  return typeMap[type] || 'info'
}

// 题目类型标签文本
const getQuestionTypeLabel = (type) => {
  const typeMap = {
    single: '单选题',
    multiple: '多选题',
    judge: '判断题',
    fill: '填空题',
    short: '简答题'
  }
  return typeMap[type] || '未知'
}

// 难度标签样式
const getDifficultyTagType = (difficulty) => {
  const difficultyMap = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return difficultyMap[difficulty] || 'info'
}

// 难度标签文本
const getDifficultyLabel = (difficulty) => {
  const difficultyMap = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return difficultyMap[difficulty] || '未知'
}

// 试卷搜索
const handleExamSearch = () => {
  examCurrentPage.value = 1
  loadExamData()
}

// 试卷重置搜索
const handleExamReset = () => {
  Object.keys(examSearchForm).forEach(key => {
    examSearchForm[key] = ''
  })
  handleExamSearch()
}

// 试题搜索
const handleQuestionSearch = () => {
  questionCurrentPage.value = 1
  loadQuestionData()
}

// 试题重置搜索
const handleQuestionReset = () => {
  Object.keys(questionSearchForm).forEach(key => {
    questionSearchForm[key] = ''
  })
  handleQuestionSearch()
}

// 新增试卷
const handleAddExam = () => {
  examDialogTitle.value = '新增试卷'
  resetExamForm()
  examDialogVisible.value = true
}

// 编辑试卷
const handleEditExam = (row) => {
  examDialogTitle.value = '编辑试卷'
  Object.assign(examForm, row)
  examDialogVisible.value = true
}

// 查看试卷
const handleViewExam = (row) => {
  ElMessage.info(`查看试卷：${row.name}`)
}

// 管理题目
const handleManageQuestions = (row) => {
  ElMessage.info(`管理试卷"${row.name}"的题目`)
}

// 删除试卷
const handleDeleteExam = (row) => {
  ElMessageBox.confirm(
    `确定要删除试卷"${row.name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    const index = examTableData.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      examTableData.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 新增试题
const handleAddQuestion = () => {
  questionDialogTitle.value = '新增试题'
  resetQuestionForm()
  questionDialogVisible.value = true
}

// 编辑试题
const handleEditQuestion = (row) => {
  questionDialogTitle.value = '编辑试题'
  Object.assign(questionForm, row)
  questionDialogVisible.value = true
}

// 查看试题
const handleViewQuestion = (row) => {
  ElMessage.info(`查看试题：${row.content.substring(0, 20)}...`)
}

// 删除试题
const handleDeleteQuestion = (row) => {
  ElMessageBox.confirm(
    `确定要删除这道试题吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    const index = questionTableData.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      questionTableData.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 提交试卷表单
const handleExamSubmit = () => {
  examFormRef.value.validate((valid) => {
    if (valid) {
      if (examForm.id) {
        // 编辑
        const index = examTableData.value.findIndex(item => item.id === examForm.id)
        if (index > -1) {
          Object.assign(examTableData.value[index], { ...examForm })
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newId = Math.max(...examTableData.value.map(item => item.id)) + 1
        examTableData.value.push({
          ...examForm,
          id: newId,
          questionCount: 0,
          createTime: new Date().toISOString().split('T')[0]
        })
        ElMessage.success('新增成功')
      }
      examDialogVisible.value = false
    }
  })
}

// 提交试题表单
const handleQuestionSubmit = () => {
  questionFormRef.value.validate((valid) => {
    if (valid) {
      if (questionForm.id) {
        // 编辑
        const index = questionTableData.value.findIndex(item => item.id === questionForm.id)
        if (index > -1) {
          Object.assign(questionTableData.value[index], { ...questionForm })
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newId = Math.max(...questionTableData.value.map(item => item.id)) + 1
        questionTableData.value.push({
          ...questionForm,
          id: newId,
          createTime: new Date().toISOString().split('T')[0]
        })
        ElMessage.success('新增成功')
      }
      questionDialogVisible.value = false
    }
  })
}

// 重置试卷表单
const resetExamForm = () => {
  Object.keys(examForm).forEach(key => {
    examForm[key] = key === 'totalScore' ? 100 : key === 'duration' ? 120 : key === 'status' ? 'draft' : ''
  })
  examForm.id = null
}

// 重置试题表单
const resetQuestionForm = () => {
  Object.keys(questionForm).forEach(key => {
    questionForm[key] = key === 'score' ? 5 : ''
  })
  questionForm.id = null
}

// 试卷分页大小改变
const handleExamSizeChange = (val) => {
  examPageSize.value = val
  loadExamData()
}

// 试卷当前页改变
const handleExamCurrentChange = (val) => {
  examCurrentPage.value = val
  loadExamData()
}

// 试题分页大小改变
const handleQuestionSizeChange = (val) => {
  questionPageSize.value = val
  loadQuestionData()
}

// 试题当前页改变
const handleQuestionCurrentChange = (val) => {
  questionCurrentPage.value = val
  loadQuestionData()
}

// 加载试卷数据
const loadExamData = () => {
  examLoading.value = true
  setTimeout(() => {
    examLoading.value = false
    examTotal.value = examTableData.value.length
  }, 500)
}

// 加载试题数据
const loadQuestionData = () => {
  questionLoading.value = true
  setTimeout(() => {
    questionLoading.value = false
    questionTotal.value = questionTableData.value.length
  }, 500)
}

// 组件挂载时加载数据
onMounted(() => {
  loadExamData()
  loadQuestionData()
})
</script>

<style scoped>
.education-container {
  padding: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-area {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.search-form {
  margin-bottom: 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 确保下拉框有足够的宽度 */
.search-form .el-select {
  min-width: 180px;
}

.search-form .el-input {
  min-width: 200px;
}

/* Tab标签页样式 */
.education-tabs {
  margin-top: 10px;
}

.tab-content {
  padding: 20px 0;
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-start;
}

/* 自定义tab样式 */
.education-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
}

.education-tabs :deep(.el-tabs__nav-wrap) {
  padding: 0 20px;
}

.education-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  padding: 0 30px;
  height: 50px;
  line-height: 50px;
}

.education-tabs :deep(.el-tabs__item.is-active) {
  font-weight: bold;
  color: #409eff;
}

.education-tabs :deep(.el-tabs__content) {
  padding: 0;
}
</style> 