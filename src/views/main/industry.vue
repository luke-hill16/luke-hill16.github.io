<template>
  <div class="industry-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>工信管理</span>
          <el-button type="primary" @click="handleAdd">新增工信项目</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="项目名称">
            <el-input v-model="searchForm.name" placeholder="请输入项目名称" clearable />
          </el-form-item>
          <el-form-item label="项目类型">
            <el-select v-model="searchForm.type" placeholder="请选择项目类型" clearable style="width: 180px;">
              <el-option label="技术创新" value="innovation" />
              <el-option label="产业升级" value="upgrade" />
              <el-option label="智能制造" value="smart" />
              <el-option label="数字化转型" value="digital" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 180px;">
              <el-option label="进行中" value="ongoing" />
              <el-option label="已完成" value="completed" />
              <el-option label="暂停" value="paused" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="项目名称" />
        <el-table-column prop="type" label="项目类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="budget" label="预算(万元)" width="120" />
        <el-table-column prop="startDate" label="开始时间" width="120" />
        <el-table-column prop="endDate" label="结束时间" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="manager" label="负责人" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="handleView(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择项目类型" style="width: 100%">
            <el-option label="技术创新" value="innovation" />
            <el-option label="产业升级" value="upgrade" />
            <el-option label="智能制造" value="smart" />
            <el-option label="数字化转型" value="digital" />
          </el-select>
        </el-form-item>
        <el-form-item label="预算(万元)" prop="budget">
          <el-input-number v-model="form.budget" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="开始时间" prop="startDate">
          <el-date-picker v-model="form.startDate" type="date" placeholder="选择开始时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束时间" prop="endDate">
          <el-date-picker v-model="form.endDate" type="date" placeholder="选择结束时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="进行中" value="ongoing" />
            <el-option label="已完成" value="completed" />
            <el-option label="暂停" value="paused" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人" prop="manager">
          <el-input v-model="form.manager" placeholder="请输入负责人" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入项目描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增工信项目')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const formRef = ref()

// 搜索表单
const searchForm = reactive({
  name: '',
  type: '',
  status: ''
})

// 表格数据
const tableData = ref([
  {
    id: 1,
    name: '智能制造示范项目',
    type: 'smart',
    budget: 500.00,
    startDate: '2024-01-01',
    endDate: '2024-12-31',
    status: 'ongoing',
    manager: '张三',
    description: '推进企业智能制造转型升级'
  },
  {
    id: 2,
    name: '数字化转型项目',
    type: 'digital',
    budget: 300.00,
    startDate: '2024-02-01',
    endDate: '2024-08-31',
    status: 'completed',
    manager: '李四',
    description: '企业数字化管理系统建设'
  },
  {
    id: 3,
    name: '技术创新研发项目',
    type: 'innovation',
    budget: 800.00,
    startDate: '2024-03-01',
    endDate: '2025-02-28',
    status: 'ongoing',
    manager: '王五',
    description: '新技术研发与应用'
  }
])

// 表单数据
const form = reactive({
  id: null,
  name: '',
  type: '',
  budget: 0,
  startDate: '',
  endDate: '',
  status: '',
  manager: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择项目类型', trigger: 'change' }
  ],
  budget: [
    { required: true, message: '请输入预算', trigger: 'blur' }
  ],
  startDate: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  endDate: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  manager: [
    { required: true, message: '请输入负责人', trigger: 'blur' }
  ]
}

// 获取类型标签样式
const getTypeTagType = (type) => {
  const typeMap = {
    innovation: 'success',
    upgrade: 'warning',
    smart: 'primary',
    digital: 'info'
  }
  return typeMap[type] || 'info'
}

// 获取类型标签文本
const getTypeLabel = (type) => {
  const typeMap = {
    innovation: '技术创新',
    upgrade: '产业升级',
    smart: '智能制造',
    digital: '数字化转型'
  }
  return typeMap[type] || '未知'
}

// 获取状态标签样式
const getStatusTagType = (status) => {
  const statusMap = {
    ongoing: 'primary',
    completed: 'success',
    paused: 'warning'
  }
  return statusMap[status] || 'info'
}

// 获取状态标签文本
const getStatusLabel = (status) => {
  const statusMap = {
    ongoing: '进行中',
    completed: '已完成',
    paused: '暂停'
  }
  return statusMap[status] || '未知'
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

// 重置搜索
const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  handleSearch()
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增工信项目'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑工信项目'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 查看
const handleView = (row) => {
  ElMessage.info(`查看项目：${row.name}`)
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除项目"${row.name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    // 这里应该调用删除API
    const index = tableData.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      tableData.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 提交表单
const handleSubmit = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      if (form.id) {
        // 编辑
        const index = tableData.value.findIndex(item => item.id === form.id)
        if (index > -1) {
          Object.assign(tableData.value[index], { ...form })
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newId = Math.max(...tableData.value.map(item => item.id)) + 1
        tableData.value.push({
          ...form,
          id: newId
        })
        ElMessage.success('新增成功')
      }
      dialogVisible.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  Object.keys(form).forEach(key => {
    form[key] = key === 'budget' ? 0 : ''
  })
  form.id = null
}

// 分页大小改变
const handleSizeChange = (val) => {
  pageSize.value = val
  loadData()
}

// 当前页改变
const handleCurrentChange = (val) => {
  currentPage.value = val
  loadData()
}

// 加载数据
const loadData = () => {
  loading.value = true
  // 模拟API调用
  setTimeout(() => {
    loading.value = false
    total.value = tableData.value.length
  }, 500)
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.industry-container {
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












































































</style> 