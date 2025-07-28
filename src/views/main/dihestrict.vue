<template>
  <div class="district-container">
    <div class="page-header">
      <h2>区县管理系统</h2>
      <div class="header-actions">
        <el-button type="success" @click="exportData">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          添加区县
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
                <el-icon><Location /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">区县总数</div>
                <div class="card-value">{{ districtStats.total }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon success">
                <el-icon><User /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">总人口</div>
                <div class="card-value">{{ formatNumber(districtStats.totalPopulation) }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon warning">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">GDP总量</div>
                <div class="card-value">{{ formatCurrency(districtStats.totalGDP) }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon info">
                <el-icon><OfficeBuilding /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">企业数量</div>
                <div class="card-value">{{ formatNumber(districtStats.totalCompanies) }}</div>
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
            placeholder="区县名称"
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
          <el-select v-model="searchForm.level" placeholder="行政级别" clearable @change="handleSearch">
            <el-option label="市辖区" value="district" />
            <el-option label="县级市" value="county" />
            <el-option label="县" value="county-level" />
            <el-option label="自治县" value="autonomous" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="searchForm.region" placeholder="所属区域" clearable @change="handleSearch">
            <el-option label="城区" value="urban" />
            <el-option label="郊区" value="suburban" />
            <el-option label="农村" value="rural" />
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

    <!-- 区县列表 -->
    <div class="district-list">
      <el-table :data="districtList" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="区县名称" />
        <el-table-column prop="level" label="行政级别" width="120">
          <template #default="scope">
            <el-tag :type="getLevelTagType(scope.row.level)">
              {{ getLevelLabel(scope.row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="region" label="所属区域" width="100">
          <template #default="scope">
            <el-tag :type="getRegionTagType(scope.row.region)">
              {{ getRegionLabel(scope.row.region) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="population" label="人口(万)" width="100" />
        <el-table-column prop="area" label="面积(km²)" width="120" />
        <el-table-column prop="gdp" label="GDP(亿元)" width="120" />
        <el-table-column prop="companies" label="企业数量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewDistrict(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editDistrict(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteDistrict(scope.row)">删除</el-button>
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

    <!-- 添加/编辑区县对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      @close="resetForm"
    >
      <el-form :model="districtForm" :rules="rules" ref="districtFormRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="区县名称" prop="name">
              <el-input v-model="districtForm.name" placeholder="请输入区县名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行政级别" prop="level">
              <el-select v-model="districtForm.level" placeholder="请选择行政级别" style="width: 100%">
                <el-option label="市辖区" value="district" />
                <el-option label="县级市" value="county" />
                <el-option label="县" value="county-level" />
                <el-option label="自治县" value="autonomous" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属区域" prop="region">
              <el-select v-model="districtForm.region" placeholder="请选择所属区域" style="width: 100%">
                <el-option label="城区" value="urban" />
                <el-option label="郊区" value="suburban" />
                <el-option label="农村" value="rural" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮政编码" prop="postcode">
              <el-input v-model="districtForm.postcode" placeholder="请输入邮政编码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="人口(万)" prop="population">
              <el-input-number v-model="districtForm.population" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="面积(km²)" prop="area">
              <el-input-number v-model="districtForm.area" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="GDP(亿元)" prop="gdp">
              <el-input-number v-model="districtForm.gdp" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="企业数量" prop="companies">
              <el-input-number v-model="districtForm.companies" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="区县状态" prop="status">
              <el-select v-model="districtForm.status" placeholder="请选择区县状态" style="width: 100%">
                <el-option label="正常" value="normal" />
                <el-option label="发展中" value="developing" />
                <el-option label="待开发" value="pending" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="成立时间" prop="establishDate">
              <el-date-picker
                v-model="districtForm.establishDate"
                type="date"
                placeholder="选择成立时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="地理位置" prop="location">
          <el-input v-model="districtForm.location" placeholder="请输入地理位置描述" />
        </el-form-item>
        <el-form-item label="区县描述" prop="description">
          <el-input
            v-model="districtForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入区县描述"
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

    <!-- 区县详情对话框 -->
    <el-dialog v-model="detailVisible" title="区县详情" width="800px">
      <div v-if="currentDistrict" class="district-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="区县名称">{{ currentDistrict.name }}</el-descriptions-item>
          <el-descriptions-item label="行政级别">
            <el-tag :type="getLevelTagType(currentDistrict.level)">
              {{ getLevelLabel(currentDistrict.level) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="所属区域">
            <el-tag :type="getRegionTagType(currentDistrict.region)">
              {{ getRegionLabel(currentDistrict.region) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="邮政编码">{{ currentDistrict.postcode }}</el-descriptions-item>
          <el-descriptions-item label="人口">{{ currentDistrict.population }}万人</el-descriptions-item>
          <el-descriptions-item label="面积">{{ currentDistrict.area }} km²</el-descriptions-item>
          <el-descriptions-item label="GDP">{{ currentDistrict.gdp }}亿元</el-descriptions-item>
          <el-descriptions-item label="企业数量">{{ currentDistrict.companies }}家</el-descriptions-item>
          <el-descriptions-item label="区县状态">
            <el-tag :type="getStatusTagType(currentDistrict.status)">
              {{ getStatusLabel(currentDistrict.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="成立时间">{{ currentDistrict.establishDate }}</el-descriptions-item>
          <el-descriptions-item label="地理位置" :span="2">{{ currentDistrict.location }}</el-descriptions-item>
          <el-descriptions-item label="区县描述" :span="2">{{ currentDistrict.description || '暂无描述' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Search, Location, User, TrendCharts, OfficeBuilding } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const districtFormRef = ref()
const currentDistrict = ref(null)

// 搜索表单
const searchForm = reactive({
  name: '',
  level: '',
  region: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 区县表单
const districtForm = reactive({
  id: null,
  name: '',
  level: '',
  region: '',
  postcode: '',
  population: 0,
  area: 0,
  gdp: 0,
  companies: 0,
  status: 'normal',
  establishDate: '',
  location: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入区县名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择行政级别', trigger: 'change' }
  ],
  region: [
    { required: true, message: '请选择所属区域', trigger: 'change' }
  ],
  postcode: [
    { pattern: /^\d{6}$/, message: '邮政编码格式不正确', trigger: 'blur' }
  ],
  population: [
    { required: true, message: '请输入人口数量', trigger: 'blur' }
  ],
  area: [
    { required: true, message: '请输入面积', trigger: 'blur' }
  ]
}

// 统计数据
const districtStats = reactive({
  total: 0,
  totalPopulation: 0,
  totalGDP: 0,
  totalCompanies: 0
})

// 区县列表
const districtList = ref([
  {
    id: 1,
    name: '朝阳区',
    level: 'district',
    region: 'urban',
    postcode: '100020',
    population: 345.2,
    area: 470.8,
    gdp: 1250.5,
    companies: 15680,
    status: 'normal',
    establishDate: '1958-05-01',
    location: '北京市东部',
    description: '北京市中心城区之一，经济发达，文化繁荣',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 2,
    name: '海淀区',
    level: 'district',
    region: 'urban',
    postcode: '100080',
    population: 332.1,
    area: 431.0,
    gdp: 1180.3,
    companies: 14250,
    status: 'normal',
    establishDate: '1952-09-01',
    location: '北京市西北部',
    description: '科技教育中心，中关村科技园区所在地',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 3,
    name: '昌平区',
    level: 'district',
    region: 'suburban',
    postcode: '102200',
    population: 196.8,
    area: 1343.5,
    gdp: 680.2,
    companies: 8560,
    status: 'developing',
    establishDate: '1999-09-16',
    location: '北京市北部',
    description: '北京市重要的生态涵养区和科技创新基地',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 4,
    name: '密云区',
    level: 'district',
    region: 'rural',
    postcode: '101500',
    population: 45.6,
    area: 2229.5,
    gdp: 180.5,
    companies: 2340,
    status: 'developing',
    establishDate: '2015-11-17',
    location: '北京市东北部',
    description: '生态涵养区，以旅游业和农业为主',
    createTime: '2020-01-01 10:00:00'
  }
])

// 计算属性
const dialogTitle = computed(() => {
  return districtForm.id ? '编辑区县' : '添加区县'
})

// 方法
const getLevelLabel = (level) => {
  const levelMap = {
    district: '市辖区',
    county: '县级市',
    'county-level': '县',
    autonomous: '自治县'
  }
  return levelMap[level] || '未知'
}

const getLevelTagType = (level) => {
  const levelMap = {
    district: 'primary',
    county: 'success',
    'county-level': 'warning',
    autonomous: 'info'
  }
  return levelMap[level] || ''
}

const getRegionLabel = (region) => {
  const regionMap = {
    urban: '城区',
    suburban: '郊区',
    rural: '农村'
  }
  return regionMap[region] || '未知'
}

const getRegionTagType = (region) => {
  const regionMap = {
    urban: 'primary',
    suburban: 'warning',
    rural: 'success'
  }
  return regionMap[region] || ''
}

const getStatusLabel = (status) => {
  const statusMap = {
    normal: '正常',
    developing: '发展中',
    pending: '待开发'
  }
  return statusMap[status] || '未知'
}

const getStatusTagType = (status) => {
  const statusMap = {
    normal: 'success',
    developing: 'warning',
    pending: 'info'
  }
  return statusMap[status] || ''
}

const formatNumber = (num) => {
  return num.toLocaleString()
}

const formatCurrency = (num) => {
  return (num / 10000).toFixed(1) + '万亿'
}

const showAddDialog = () => {
  districtForm.id = null
  dialogVisible.value = true
}

const editDistrict = (row) => {
  Object.assign(districtForm, row)
  dialogVisible.value = true
}

const viewDistrict = (row) => {
  currentDistrict.value = row
  detailVisible.value = true
}

const deleteDistrict = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除区县"${row.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = districtList.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      districtList.value.splice(index, 1)
      updateStats()
      ElMessage.success('删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

const submitForm = async () => {
  if (!districtFormRef.value) return
  
  try {
    await districtFormRef.value.validate()
    submitting.value = true
    
    // 模拟提交操作
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (districtForm.id) {
      // 编辑
      const index = districtList.value.findIndex(item => item.id === districtForm.id)
      if (index > -1) {
        districtList.value[index] = { ...districtForm }
      }
      ElMessage.success('编辑成功')
    } else {
      // 新增
      const newDistrict = {
        ...districtForm,
        id: Date.now(),
        createTime: new Date().toLocaleString()
      }
      districtList.value.unshift(newDistrict)
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
  if (districtFormRef.value) {
    districtFormRef.value.resetFields()
  }
  Object.assign(districtForm, {
    id: null,
    name: '',
    level: '',
    region: '',
    postcode: '',
    population: 0,
    area: 0,
    gdp: 0,
    companies: 0,
    status: 'normal',
    establishDate: '',
    location: '',
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
    level: '',
    region: ''
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
  ElMessage.success('区县数据导出成功')
}

const updateStats = () => {
  districtStats.total = districtList.value.length
  districtStats.totalPopulation = districtList.value.reduce((sum, item) => sum + item.population, 0)
  districtStats.totalGDP = districtList.value.reduce((sum, item) => sum + item.gdp, 0)
  districtStats.totalCompanies = districtList.value.reduce((sum, item) => sum + item.companies, 0)
}

// 生命周期
onMounted(() => {
  updateStats()
  pagination.total = districtList.value.length
})
</script>

<style scoped>
.district-container {
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

.district-list {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.district-detail {
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