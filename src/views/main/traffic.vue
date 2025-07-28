<template>
  <div class="traffic-container">
    <div class="page-header">
      <h2>交通管理系统</h2>
      <div class="header-actions">
        <el-button type="success" @click="exportData">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          添加设施
        </el-button>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="overview-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon primary">
                <el-icon><Document /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">道路总数</div>
                <div class="card-value">{{ trafficStats.totalRoads }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon success">
                <el-icon><Location /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">车辆流量</div>
                <div class="card-value">{{ formatNumber(trafficStats.totalVehicles) }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon warning">
                <el-icon><Bell /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">事故数量</div>
                <div class="card-value">{{ trafficStats.totalAccidents }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon info">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">信号灯</div>
                <div class="card-value">{{ trafficStats.totalSignals }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.name"
            placeholder="设施名称"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select v-model="searchForm.type" placeholder="设施类型" clearable @change="handleSearch">
            <el-option label="道路" value="road" />
            <el-option label="桥梁" value="bridge" />
            <el-option label="隧道" value="tunnel" />
            <el-option label="信号灯" value="signal" />
            <el-option label="停车场" value="parking" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="searchForm.status" placeholder="设施状态" clearable @change="handleSearch">
            <el-option label="正常" value="normal" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="故障" value="fault" />
            <el-option label="建设中" value="construction" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 交通设施列表 -->
    <div class="traffic-list">
      <el-table :data="trafficList" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="设施名称" />
        <el-table-column prop="type" label="设施类型" width="100">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="length" label="长度(km)" width="100" />
        <el-table-column prop="capacity" label="通行能力" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastMaintenance" label="最后维护" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewTraffic(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editTraffic(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteTraffic(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 添加/编辑交通设施对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      @close="resetForm"
    >
      <el-form :model="trafficForm" :rules="rules" ref="trafficFormRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="设施名称" prop="name">
              <el-input v-model="trafficForm.name" placeholder="请输入设施名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设施类型" prop="type">
              <el-select v-model="trafficForm.type" placeholder="请选择设施类型" style="width: 100%">
                <el-option label="道路" value="road" />
                <el-option label="桥梁" value="bridge" />
                <el-option label="隧道" value="tunnel" />
                <el-option label="信号灯" value="signal" />
                <el-option label="停车场" value="parking" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="位置" prop="location">
              <el-input v-model="trafficForm.location" placeholder="请输入设施位置" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="长度(km)" prop="length">
              <el-input-number v-model="trafficForm.length" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="通行能力" prop="capacity">
              <el-input v-model="trafficForm.capacity" placeholder="如：双向四车道" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="设施状态" prop="status">
              <el-select v-model="trafficForm.status" placeholder="请选择设施状态" style="width: 100%">
                <el-option label="正常" value="normal" />
                <el-option label="维护中" value="maintenance" />
                <el-option label="故障" value="fault" />
                <el-option label="建设中" value="construction" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="建设时间" prop="buildDate">
              <el-date-picker
                v-model="trafficForm.buildDate"
                type="date"
                placeholder="选择建设时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最后维护" prop="lastMaintenance">
              <el-date-picker
                v-model="trafficForm.lastMaintenance"
                type="date"
                placeholder="选择最后维护时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="设施描述" prop="description">
          <el-input
            v-model="trafficForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入设施描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 交通设施详情对话框 -->
    <el-dialog v-model="detailVisible" title="交通设施详情" width="800px">
      <div v-if="currentTraffic" class="traffic-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="设施名称">{{ currentTraffic.name }}</el-descriptions-item>
          <el-descriptions-item label="设施类型">
            <el-tag :type="getTypeTagType(currentTraffic.type)">
              {{ getTypeLabel(currentTraffic.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="位置">{{ currentTraffic.location }}</el-descriptions-item>
          <el-descriptions-item label="长度">{{ currentTraffic.length }} km</el-descriptions-item>
          <el-descriptions-item label="通行能力">{{ currentTraffic.capacity }}</el-descriptions-item>
          <el-descriptions-item label="设施状态">
            <el-tag :type="getStatusTagType(currentTraffic.status)">
              {{ getStatusLabel(currentTraffic.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="建设时间">{{ currentTraffic.buildDate }}</el-descriptions-item>
          <el-descriptions-item label="最后维护">{{ currentTraffic.lastMaintenance }}</el-descriptions-item>
          <el-descriptions-item label="设施描述" :span="2">{{ currentTraffic.description || '暂无描述' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Search, Document, Bell, Location, Monitor } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const trafficFormRef = ref()
const currentTraffic = ref(null)

// 搜索表单
const searchForm = reactive({
  name: '',
  type: '',
  status: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 交通设施表单
const trafficForm = reactive({
  id: null,
  name: '',
  type: '',
  location: '',
  length: 0,
  capacity: '',
  status: 'normal',
  buildDate: '',
  lastMaintenance: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入设施名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择设施类型', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入设施位置', trigger: 'blur' }
  ],
  length: [
    { required: true, message: '请输入设施长度', trigger: 'blur' }
  ],
  capacity: [
    { required: true, message: '请输入通行能力', trigger: 'blur' }
  ]
}

// 统计数据
const trafficStats = reactive({
  totalRoads: 0,
  totalVehicles: 0,
  totalAccidents: 0,
  totalSignals: 0
})

// 交通设施列表
const trafficList = ref([
  {
    id: 1,
    name: '长安街',
    type: 'road',
    location: '北京市中心',
    length: 3.8,
    capacity: '双向八车道',
    status: 'normal',
    buildDate: '1950-01-01',
    lastMaintenance: '2024-01-15',
    description: '北京市最重要的东西向主干道，连接天安门广场',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 2,
    name: '二环路',
    type: 'road',
    location: '北京市二环',
    length: 32.7,
    capacity: '双向六车道',
    status: 'normal',
    buildDate: '1980-01-01',
    lastMaintenance: '2024-02-01',
    description: '北京市重要的环形主干道',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 3,
    name: '长安街信号灯系统',
    type: 'signal',
    location: '长安街沿线',
    length: 0,
    capacity: '智能控制',
    status: 'normal',
    buildDate: '2010-01-01',
    lastMaintenance: '2024-01-20',
    description: '智能交通信号灯系统，实现绿波带控制',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 4,
    name: '西直门立交桥',
    type: 'bridge',
    location: '西直门地区',
    length: 1.2,
    capacity: '双向四车道',
    status: 'maintenance',
    buildDate: '1995-01-01',
    lastMaintenance: '2024-03-01',
    description: '重要的交通枢纽立交桥',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 5,
    name: '王府井停车场',
    type: 'parking',
    location: '王府井商业区',
    length: 0,
    capacity: '500个车位',
    status: 'normal',
    buildDate: '2005-01-01',
    lastMaintenance: '2024-01-10',
    description: '王府井商业区地下停车场',
    createTime: '2020-01-01 10:00:00'
  }
])

// 计算属性
const dialogTitle = computed(() => {
  return trafficForm.id ? '编辑交通设施' : '添加交通设施'
})

// 方法
const getTypeLabel = (type) => {
  const typeMap = {
    road: '道路',
    bridge: '桥梁',
    tunnel: '隧道',
    signal: '信号灯',
    parking: '停车场'
  }
  return typeMap[type] || '未知'
}

const getTypeTagType = (type) => {
  const typeMap = {
    road: 'primary',
    bridge: 'success',
    tunnel: 'warning',
    signal: 'info',
    parking: 'danger'
  }
  return typeMap[type] || ''
}

const getStatusLabel = (status) => {
  const statusMap = {
    normal: '正常',
    maintenance: '维护中',
    fault: '故障',
    construction: '建设中'
  }
  return statusMap[status] || '未知'
}

const getStatusTagType = (status) => {
  const statusMap = {
    normal: 'success',
    maintenance: 'warning',
    fault: 'danger',
    construction: 'info'
  }
  return statusMap[status] || ''
}

const formatNumber = (num) => {
  return num.toLocaleString()
}

const showAddDialog = () => {
  trafficForm.id = null
  dialogVisible.value = true
}

const editTraffic = (row) => {
  Object.assign(trafficForm, row)
  dialogVisible.value = true
}

const viewTraffic = (row) => {
  currentTraffic.value = row
  detailVisible.value = true
}

const deleteTraffic = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除交通设施"${row.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = trafficList.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      trafficList.value.splice(index, 1)
      updateStats()
      ElMessage.success('删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

const submitForm = async () => {
  if (!trafficFormRef.value) return
  
  try {
    await trafficFormRef.value.validate()
    submitting.value = true
    
    // 模拟提交操作
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (trafficForm.id) {
      // 编辑
      const index = trafficList.value.findIndex(item => item.id === trafficForm.id)
      if (index > -1) {
        trafficList.value[index] = { ...trafficForm }
      }
      ElMessage.success('编辑成功')
    } else {
      // 新增
      const newTraffic = {
        ...trafficForm,
        id: Date.now(),
        createTime: new Date().toLocaleString()
      }
      trafficList.value.unshift(newTraffic)
      ElMessage.success('添加成功')
    }
    
    updateStats()
    dialogVisible.value = false
    resetForm()
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  if (trafficFormRef.value) {
    trafficFormRef.value.resetFields()
  }
  Object.assign(trafficForm, {
    id: null,
    name: '',
    type: '',
    location: '',
    length: 0,
    capacity: '',
    status: 'normal',
    buildDate: '',
    lastMaintenance: '',
    description: ''
  })
}

const handleSearch = () => {
  pagination.currentPage = 1
  // 这里可以调用实际的搜索API
  console.log('搜索条件:', searchForm)
}

const resetSearch = () => {
  Object.assign(searchForm, {
    name: '',
    type: '',
    status: ''
  })
  handleSearch()
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
  // 重新加载数据
}

const handleCurrentChange = (val) => {
  pagination.currentPage = val
  // 重新加载数据
}

const exportData = () => {
  // 模拟导出功能
  ElMessage.success('交通设施数据导出成功')
}

const updateStats = () => {
  trafficStats.totalRoads = trafficList.value.filter(item => item.type === 'road').length
  trafficStats.totalVehicles = 1500000 // 模拟数据
  trafficStats.totalAccidents = 25 // 模拟数据
  trafficStats.totalSignals = trafficList.value.filter(item => item.type === 'signal').length
}

// 生命周期
onMounted(() => {
  updateStats()
  pagination.total = trafficList.value.length
})
</script>

<style scoped>
.traffic-container {
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

.card-icon.primary {
  background: linear-gradient(135deg, #409eff, #66b1ff);
}

.card-icon.success {
  background: linear-gradient(135deg, #67c23a, #85ce61);
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

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.traffic-list {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.traffic-detail {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}

:deep(.el-descriptions__label) {
  font-weight: bold;
  color: #606266;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}
</style> 