<template>
  <div class="building-container">
    <div class="page-header">
      <h2>建筑管理系统</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon>
        添加建筑
      </el-button>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.name"
            placeholder="建筑名称"
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
          <el-select v-model="searchForm.status" placeholder="建筑状态" clearable @change="handleSearch">
            <el-option label="正常" value="normal" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="停用" value="disabled" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="searchForm.type" placeholder="建筑类型" clearable @change="handleSearch">
            <el-option label="办公楼" value="office" />
            <el-option label="住宅楼" value="residential" />
            <el-option label="商业楼" value="commercial" />
            <el-option label="工业建筑" value="industrial" />
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

    <!-- 建筑列表 -->
    <div class="building-list">
      <el-table :data="buildingList" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="建筑名称" />
        <el-table-column prop="type" label="建筑类型">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="floors" label="楼层数" width="100" />
        <el-table-column prop="area" label="建筑面积(m²)" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="buildDate" label="建成日期" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewBuilding(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editBuilding(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteBuilding(scope.row)">删除</el-button>
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

    <!-- 添加/编辑建筑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="buildingForm" :rules="rules" ref="buildingFormRef" label-width="100px">
        <el-form-item label="建筑名称" prop="name">
          <el-input v-model="buildingForm.name" placeholder="请输入建筑名称" />
        </el-form-item>
        <el-form-item label="建筑类型" prop="type">
          <el-select v-model="buildingForm.type" placeholder="请选择建筑类型" style="width: 100%">
            <el-option label="办公楼" value="office" />
            <el-option label="住宅楼" value="residential" />
            <el-option label="商业楼" value="commercial" />
            <el-option label="工业建筑" value="industrial" />
          </el-select>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="buildingForm.address" placeholder="请输入建筑地址" />
        </el-form-item>
        <el-form-item label="楼层数" prop="floors">
          <el-input-number v-model="buildingForm.floors" :min="1" :max="200" style="width: 100%" />
        </el-form-item>
        <el-form-item label="建筑面积" prop="area">
          <el-input-number v-model="buildingForm.area" :min="1" :precision="2" style="width: 100%" />
          <span style="margin-left: 10px; color: #666;">m²</span>
        </el-form-item>
        <el-form-item label="建筑状态" prop="status">
          <el-select v-model="buildingForm.status" placeholder="请选择建筑状态" style="width: 100%">
            <el-option label="正常" value="normal" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="停用" value="disabled" />
          </el-select>
        </el-form-item>
        <el-form-item label="建成日期" prop="buildDate">
          <el-date-picker
            v-model="buildingForm.buildDate"
            type="date"
            placeholder="选择建成日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="buildingForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入建筑描述"
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

    <!-- 建筑详情对话框 -->
    <el-dialog v-model="detailVisible" title="建筑详情" width="800px">
      <div v-if="currentBuilding" class="building-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="建筑名称">{{ currentBuilding.name }}</el-descriptions-item>
          <el-descriptions-item label="建筑类型">
            <el-tag :type="getTypeTagType(currentBuilding.type)">
              {{ getTypeLabel(currentBuilding.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="地址">{{ currentBuilding.address }}</el-descriptions-item>
          <el-descriptions-item label="楼层数">{{ currentBuilding.floors }}层</el-descriptions-item>
          <el-descriptions-item label="建筑面积">{{ currentBuilding.area }} m²</el-descriptions-item>
          <el-descriptions-item label="建筑状态">
            <el-tag :type="getStatusTagType(currentBuilding.status)">
              {{ getStatusLabel(currentBuilding.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="建成日期">{{ currentBuilding.buildDate }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentBuilding.createTime }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ currentBuilding.description || '暂无描述' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
          <el-button type="primary" @click="showRouteDialog">路径规划</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="routeVisible" title="路径规划" width="800px">
      <div>
        <el-form :model="routeForm" label-width="80px" inline>
          <el-form-item label="起点">
            <el-input v-model="routeForm.start" placeholder="请输入起点" style="width:200px;" />
          </el-form-item>
          <el-form-item label="终点">
            <el-input v-model="routeForm.end" placeholder="请输入终点" style="width:200px;" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="planRoute">规划路径</el-button>
          </el-form-item>
        </el-form>
        <div id="baiduMapContainer" style="width:100%;height:400px;margin-top:16px;"></div>
        <div v-if="routeResult" style="margin-top:16px;">
          <el-alert :title="routeResult" type="success" show-icon />
        </div>
        <div v-if="routeHistory.length" style="margin-top:24px;">
          <h4>历史路径规划</h4>
          <el-table :data="routeHistory" size="small" style="width:100%">
            <el-table-column prop="start" label="起点" />
            <el-table-column prop="end" label="终点" />
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column label="操作" width="80">
              <template #default="scope">
                <el-button size="small" @click="replayRoute(scope.row)">回显</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const buildingFormRef = ref()
const currentBuilding = ref(null)

const routeVisible = ref(false)
const routeForm = reactive({
  start: '',
  end: ''
})
const routeResult = ref('')
const routeHistory = ref([])

// 搜索表单
const searchForm = reactive({
  name: '',
  status: '',
  type: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 建筑表单
const buildingForm = reactive({
  id: null,
  name: '',
  type: '',
  address: '',
  floors: 1,
  area: 0,
  status: 'normal',
  buildDate: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入建筑名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择建筑类型', trigger: 'change' }
  ],
  address: [
    { required: true, message: '请输入建筑地址', trigger: 'blur' }
  ],
  floors: [
    { required: true, message: '请输入楼层数', trigger: 'blur' }
  ],
  area: [
    { required: true, message: '请输入建筑面积', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择建筑状态', trigger: 'change' }
  ],
  buildDate: [
    { required: true, message: '请选择建成日期', trigger: 'change' }
  ]
}

// 模拟建筑数据
const buildingList = ref([
  {
    id: 1,
    name: '益客大厦A座',
    type: 'office',
    address: '北京市朝阳区建国路88号',
    floors: 25,
    area: 15000.50,
    status: 'normal',
    buildDate: '2020-06-15',
    description: '现代化办公大楼，配套设施完善',
    createTime: '2020-01-01 10:00:00'
  },
  {
    id: 2,
    name: '益客住宅小区',
    type: 'residential',
    address: '北京市海淀区中关村大街100号',
    floors: 18,
    area: 25000.00,
    status: 'normal',
    buildDate: '2019-12-01',
    description: '高品质住宅小区，环境优美',
    createTime: '2019-06-01 10:00:00'
  },
  {
    id: 3,
    name: '益客商业中心',
    type: 'commercial',
    address: '北京市西城区西单大街200号',
    floors: 12,
    area: 18000.00,
    status: 'maintenance',
    buildDate: '2018-08-20',
    description: '综合性商业中心，交通便利',
    createTime: '2018-03-01 10:00:00'
  }
])

// 计算属性
const dialogTitle = computed(() => {
  return buildingForm.id ? '编辑建筑' : '添加建筑'
})

// 方法
const getTypeLabel = (type) => {
  const typeMap = {
    office: '办公楼',
    residential: '住宅楼',
    commercial: '商业楼',
    industrial: '工业建筑'
  }
  return typeMap[type] || '未知'
}

const getTypeTagType = (type) => {
  const typeMap = {
    office: 'primary',
    residential: 'success',
    commercial: 'warning',
    industrial: 'info'
  }
  return typeMap[type] || ''
}

const getStatusLabel = (status) => {
  const statusMap = {
    normal: '正常',
    maintenance: '维护中',
    disabled: '停用'
  }
  return statusMap[status] || '未知'
}

const getStatusTagType = (status) => {
  const statusMap = {
    normal: 'success',
    maintenance: 'warning',
    disabled: 'danger'
  }
  return statusMap[status] || ''
}

const showAddDialog = () => {
  buildingForm.id = null
  dialogVisible.value = true
}

const editBuilding = (row) => {
  Object.assign(buildingForm, row)
  dialogVisible.value = true
}

const viewBuilding = (row) => {
  currentBuilding.value = row
  detailVisible.value = true
}

const deleteBuilding = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除建筑"${row.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = buildingList.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      buildingList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

const submitForm = async () => {
  if (!buildingFormRef.value) return
  
  try {
    await buildingFormRef.value.validate()
    submitting.value = true
    
    // 模拟提交操作
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (buildingForm.id) {
      // 编辑
      const index = buildingList.value.findIndex(item => item.id === buildingForm.id)
      if (index > -1) {
        buildingList.value[index] = { ...buildingForm }
      }
      ElMessage.success('编辑成功')
    } else {
      // 新增
      const newBuilding = {
        ...buildingForm,
        id: Date.now(),
        createTime: new Date().toLocaleString()
      }
      buildingList.value.unshift(newBuilding)
      ElMessage.success('添加成功')
    }
    
    dialogVisible.value = false
    resetForm()
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  if (buildingFormRef.value) {
    buildingFormRef.value.resetFields()
  }
  Object.assign(buildingForm, {
    id: null,
    name: '',
    type: '',
    address: '',
    floors: 1,
    area: 0,
    status: 'normal',
    buildDate: '',
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
    status: '',
    type: ''
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

function showRouteDialog() {
  routeForm.start = ''
  routeForm.end = currentBuilding.value?.address || ''
  routeResult.value = ''
  routeVisible.value = true
  nextTick(() => {
    initBaiduMap()
  })
  loadRouteHistory()
}

function planRoute() {
  if (!routeForm.start || !routeForm.end) {
    routeResult.value = '请填写起点和终点'
    return
  }
  // 百度地图路径规划
  const map = new window.BMap.Map('baiduMapContainer')
  map.centerAndZoom(routeForm.end, 14)
  map.enableScrollWheelZoom(true)
  const driving = new window.BMap.DrivingRoute(map, {
    renderOptions: { map: map, autoViewport: true }
  })
  driving.search(routeForm.start, routeForm.end)
  routeResult.value = `已为您规划从【${routeForm.start}】到【${routeForm.end}】的路径`
  // 保存历史
  saveRouteHistory({
    start: routeForm.start,
    end: routeForm.end,
    time: new Date().toLocaleString()
  })
  loadRouteHistory()
}

function replayRoute(item) {
  routeForm.start = item.start
  routeForm.end = item.end
  planRoute()
}

function initBaiduMap() {
  const map = new window.BMap.Map('baiduMapContainer')
  map.centerAndZoom(routeForm.end || '北京', 12)
  map.enableScrollWheelZoom(true)
  map.clearOverlays()
  map.addEventListener('click', function(e) {
    const point = e.point
    const geoc = new window.BMap.Geocoder()
    geoc.getLocation(point, function(rs) {
      const addr = rs.address
      ElMessageBox({
        title: '地图点选',
        message: `将【${addr}】设为起点还是终点？`,
        showCancelButton: true,
        confirmButtonText: '起点',
        cancelButtonText: '终点'
      }).then(() => {
        routeForm.start = addr
      }).catch(() => {
        routeForm.end = addr
      })
    })
  })
}

function saveRouteHistory(record) {
  const key = 'building_route_history'
  let history = JSON.parse(localStorage.getItem(key) || '[]')
  history.unshift(record)
  if (history.length > 10) history = history.slice(0, 10)
  localStorage.setItem(key, JSON.stringify(history))
}

function loadRouteHistory() {
  const key = 'building_route_history'
  routeHistory.value = JSON.parse(localStorage.getItem(key) || '[]')
}

// 生命周期
onMounted(() => {
  pagination.total = buildingList.value.length
})
</script>

<style scoped>
.building-container {
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

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.building-list {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.building-detail {
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