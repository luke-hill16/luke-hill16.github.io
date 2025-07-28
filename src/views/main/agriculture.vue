<template>
  <div class="smart-agriculture-container">
    <el-card>
      <div class="header">
        <span>智慧农业管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="addDevice" size="small">添加设备</el-button>
          <el-button type="success" @click="refreshData" size="small">刷新数据</el-button>
          <el-button type="info" @click="showAnalytics" size="small">数据分析</el-button>
          <el-button type="warning" @click="showAlerts" size="small">告警管理</el-button>
        </div>
      </div>

      <!-- 数据概览卡片 -->
      <el-row :gutter="20" style="margin-bottom: 20px;">
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon temperature">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-value">{{ averageTemperature }}°C</div>
                <div class="overview-label">平均温度</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon humidity">
                <el-icon><Histogram /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-value">{{ averageHumidity }}%</div>
                <div class="overview-label">平均湿度</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon soil">
                <el-icon><Histogram /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-value">{{ averageSoilMoisture }}%</div>
                <div class="overview-label">土壤湿度</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon light">
                <el-icon><Star /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-value">{{ averageLight }} lux</div>
                <div class="overview-label">光照强度</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 搜索筛选 -->
      <div class="search-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索设备名称或位置"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchForm.status" placeholder="设备状态" clearable>
              <el-option label="在线" value="online" />
              <el-option label="离线" value="offline" />
              <el-option label="故障" value="error" />
              <el-option label="维护中" value="maintenance" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="searchForm.type" placeholder="设备类型" clearable>
              <el-option label="传感器" value="sensor" />
              <el-option label="控制器" value="controller" />
              <el-option label="摄像头" value="camera" />
              <el-option label="灌溉设备" value="irrigation" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 设备列表 -->
      <el-table :data="devices" style="width: 100%; margin-top: 20px;" fit="true">
        <el-table-column prop="name" label="设备名称" min-width="150">
          <template #default="scope">
            <span class="clickable-title" @click="viewDeviceDetail(scope.row)">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="设备类型" min-width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.type === 'sensor'" type="primary">传感器</el-tag>
            <el-tag v-else-if="scope.row.type === 'controller'" type="success">控制器</el-tag>
            <el-tag v-else-if="scope.row.type === 'camera'" type="warning">摄像头</el-tag>
            <el-tag v-else-if="scope.row.type === 'irrigation'" type="info">灌溉设备</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="位置" min-width="120"/>
        <el-table-column prop="status" label="状态" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 'online'" type="success">在线</el-tag>
            <el-tag v-else-if="scope.row.status === 'offline'" type="danger">离线</el-tag>
            <el-tag v-else-if="scope.row.status === 'error'" type="danger">故障</el-tag>
            <el-tag v-else-if="scope.row.status === 'maintenance'" type="warning">维护中</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastUpdate" label="最后更新" min-width="150"/>
        <el-table-column prop="battery" label="电量" min-width="100">
          <template #default="scope">
            <el-progress 
              :percentage="scope.row.battery" 
              :color="getBatteryColor(scope.row.battery)"
              :show-text="false"
            />
            <span style="margin-left: 5px;">{{ scope.row.battery }}%</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewDeviceDetail(scope.row)">查看</el-button>
            <el-button size="small" type="success" @click="controlDevice(scope.row)">控制</el-button>
            <el-button size="small" type="warning" @click="maintainDevice(scope.row)">维护</el-button>
            <el-button size="small" type="danger" @click="deleteDevice(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 设备详情弹窗 -->
    <el-dialog v-model="deviceDetailVisible" title="设备详情" width="900px" :before-close="handleClose">
      <div class="device-detail" v-if="currentDevice">
        <!-- 基本信息 -->
        <el-card class="info-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>设备信息</span>
              <el-button type="primary" size="small" @click="editDevice(currentDevice)">编辑</el-button>
            </div>
          </template>
          
          <!-- 设备图片 -->
          <div class="device-image-section">
            <div class="device-image-container">
              <el-image
                :src="currentDevice.image || getDefaultDeviceImage(currentDevice.type)"
                fit="cover"
                class="device-image"
                :preview-src-list="[currentDevice.image || getDefaultDeviceImage(currentDevice.type)]"
                preview-teleported
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                    <span>图片加载失败</span>
                  </div>
                </template>
              </el-image>
              <div class="image-overlay">
                <el-button type="primary" size="small" @click="uploadDeviceImage">更换图片</el-button>
              </div>
            </div>
          </div>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>设备名称：</label>
                <span>{{ currentDevice.name }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>设备类型：</label>
                <el-tag v-if="currentDevice.type === 'sensor'" type="primary">传感器</el-tag>
                <el-tag v-else-if="currentDevice.type === 'controller'" type="success">控制器</el-tag>
                <el-tag v-else-if="currentDevice.type === 'camera'" type="warning">摄像头</el-tag>
                <el-tag v-else-if="currentDevice.type === 'irrigation'" type="info">灌溉设备</el-tag>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>设备位置：</label>
                <span>{{ currentDevice.location }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>设备状态：</label>
                <el-tag v-if="currentDevice.status === 'online'" type="success">在线</el-tag>
                <el-tag v-else-if="currentDevice.status === 'offline'" type="danger">离线</el-tag>
                <el-tag v-else-if="currentDevice.status === 'error'" type="danger">故障</el-tag>
                <el-tag v-else-if="currentDevice.status === 'maintenance'" type="warning">维护中</el-tag>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <label>设备电量：</label>
                <span>{{ currentDevice.battery }}%</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <label>最后更新：</label>
                <span>{{ currentDevice.lastUpdate }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="24">
              <div class="detail-item">
                <label>设备描述：</label>
                <div class="content-text">{{ currentDevice.description }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <!-- 实时数据 -->
        <el-card class="data-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>实时数据</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6" v-for="(data, index) in deviceData" :key="index">
              <div class="data-item">
                <div class="data-label">{{ data.label }}</div>
                <div class="data-value">{{ data.value }}{{ data.unit }}</div>
                <div class="data-status" :class="data.status">{{ data.statusText }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <!-- 历史数据图表 -->
        <el-card class="chart-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>历史数据趋势</span>
              <el-select v-model="selectedChartType" size="small" style="width: 120px;">
                <el-option label="温度" value="temperature" />
                <el-option label="湿度" value="humidity" />
                <el-option label="土壤湿度" value="soil" />
                <el-option label="光照" value="light" />
              </el-select>
            </div>
          </template>
          <div id="historyChart" style="height: 300px;"></div>
        </el-card>
      </div>
    </el-dialog>

    <!-- 添加/编辑设备弹窗 -->
    <el-dialog v-model="deviceFormVisible" :title="deviceFormTitle" width="800px" :before-close="handleFormClose">
      <el-form :model="deviceForm" :rules="deviceRules" ref="deviceFormRef" label-width="120px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="deviceForm.name" placeholder="请输入设备名称"/>
        </el-form-item>
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="deviceForm.type" placeholder="请选择设备类型" style="width: 100%">
            <el-option label="传感器" value="sensor"/>
            <el-option label="控制器" value="controller"/>
            <el-option label="摄像头" value="camera"/>
            <el-option label="灌溉设备" value="irrigation"/>
          </el-select>
        </el-form-item>
        <el-form-item label="设备位置" prop="location">
          <el-input v-model="deviceForm.location" placeholder="请输入设备位置"/>
        </el-form-item>
        <el-form-item label="设备描述" prop="description">
          <el-input
            v-model="deviceForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入设备描述"
          />
        </el-form-item>
        <el-form-item label="设备图片">
          <div class="form-image-upload">
            <el-image
              v-if="deviceForm.image"
              :src="deviceForm.image"
              fit="cover"
              class="form-device-image"
              :preview-src-list="[deviceForm.image]"
              preview-teleported
            />
            <div v-else class="form-image-placeholder">
              <el-icon><Picture /></el-icon>
              <span>暂无图片</span>
            </div>
            <el-button type="primary" @click="selectDeviceImage" style="margin-top: 10px;">
              选择图片
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="设备参数">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-input v-model="deviceForm.parameters.interval" placeholder="数据采集间隔(秒)"/>
            </el-col>
            <el-col :span="12">
              <el-input v-model="deviceForm.parameters.threshold" placeholder="告警阈值"/>
            </el-col>
          </el-row>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="deviceFormVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDeviceForm">提交</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 设备控制弹窗 -->
    <el-dialog v-model="controlVisible" title="设备控制" width="600px" :before-close="handleControlClose">
      <div class="control-panel" v-if="currentDevice">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card>
              <template #header>开关控制</template>
              <div class="control-item">
                <span>设备开关</span>
                <el-switch v-model="controlForm.power" @change="handlePowerChange"/>
              </div>
              <div class="control-item" v-if="currentDevice.type === 'irrigation'">
                <span>灌溉开关</span>
                <el-switch v-model="controlForm.irrigation" @change="handleIrrigationChange"/>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>参数设置</template>
              <div class="control-item">
                <span>采集间隔</span>
                <el-input-number v-model="controlForm.interval" :min="1" :max="3600" size="small"/>
              </div>
              <div class="control-item">
                <span>告警阈值</span>
                <el-input-number v-model="controlForm.threshold" :min="0" :max="100" size="small"/>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="controlVisible = false">取消</el-button>
          <el-button type="primary" @click="submitControl">确认控制</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 数据分析弹窗 -->
    <el-dialog v-model="analyticsVisible" title="数据分析" width="1200px" :before-close="handleAnalyticsClose">
      <div class="analytics-content">
        <!-- 统计卡片 -->
        <el-row :gutter="20" style="margin-bottom: 30px;">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-number">{{ totalDevices }}</div>
              <div class="stat-label">设备总数</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-number">{{ onlineDevices }}</div>
              <div class="stat-label">在线设备</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-number">{{ errorDevices }}</div>
              <div class="stat-label">故障设备</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-number">{{ dataPoints }}</div>
              <div class="stat-label">数据点数</div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 图表区域 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card>
              <template #header>设备状态分布</template>
              <div id="statusChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>环境数据趋势</template>
              <div id="trendChart" style="height: 300px;"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-dialog>

    <!-- 告警管理弹窗 -->
    <el-dialog v-model="alertsVisible" title="告警管理" width="1000px" :before-close="handleAlertsClose">
      <div class="alerts-content">
        <div class="alerts-header">
          <el-button type="primary" @click="addAlert">添加告警规则</el-button>
          <el-button @click="clearAllAlerts">清空所有告警</el-button>
        </div>
        
        <el-table :data="alerts" style="width: 100%; margin-top: 20px;">
          <el-table-column prop="device" label="设备" min-width="120"/>
          <el-table-column prop="type" label="告警类型" min-width="120">
            <template #default="scope">
              <el-tag v-if="scope.row.type === 'temperature'" type="danger">温度异常</el-tag>
              <el-tag v-else-if="scope.row.type === 'humidity'" type="warning">湿度异常</el-tag>
              <el-tag v-else-if="scope.row.type === 'soil'" type="info">土壤异常</el-tag>
              <el-tag v-else-if="scope.row.type === 'device'" type="danger">设备故障</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="告警信息" min-width="200"/>
          <el-table-column prop="time" label="告警时间" min-width="150"/>
          <el-table-column prop="status" label="状态" min-width="100">
            <template #default="scope">
              <el-tag v-if="scope.row.status === 'active'" type="danger">未处理</el-tag>
              <el-tag v-else type="success">已处理</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="150">
            <template #default="scope">
              <el-button size="small" type="success" @click="handleAlert(scope.row)">处理</el-button>
              <el-button size="small" type="danger" @click="deleteAlert(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Monitor, Histogram, Star, Picture } from '@element-plus/icons-vue'

// 响应式数据
const devices = ref([])
const deviceDetailVisible = ref(false)
const currentDevice = ref(null)
const deviceFormVisible = ref(false)
const deviceFormTitle = ref('添加设备')
const deviceFormRef = ref(null)
const controlVisible = ref(false)
const controlFormRef = ref(null)
const analyticsVisible = ref(false)
const alertsVisible = ref(false)
const selectedChartType = ref('temperature')
const deviceData = ref([])
const alerts = ref([])

// 搜索表单
const searchForm = ref({
  keyword: '',
  status: '',
  type: '',
  dateRange: []
})

// 模拟设备数据
const mockDevices = [
  {
    id: 'dev001',
    name: '温湿度传感器-01',
    type: 'sensor',
    location: '大棚A区',
    status: 'online',
    battery: 85,
    lastUpdate: '2024-01-15 14:30:00',
    description: '监测大棚内温湿度变化，支持远程数据采集。',
    image: 'https://picsum.photos/400/300?random=1'
  },
  {
    id: 'dev002',
    name: '土壤传感器-01',
    type: 'sensor',
    location: '大棚B区',
    status: 'online',
    battery: 92,
    lastUpdate: '2024-01-15 14:28:00',
    description: '监测土壤湿度和pH值，为灌溉提供数据支持。',
    image: 'https://picsum.photos/400/300?random=2'
  },
  {
    id: 'dev003',
    name: '智能灌溉控制器',
    type: 'controller',
    location: '大棚A区',
    status: 'online',
    battery: 78,
    lastUpdate: '2024-01-15 14:25:00',
    description: '根据土壤湿度自动控制灌溉系统。',
    image: 'https://picsum.photos/400/300?random=3'
  },
  {
    id: 'dev004',
    name: '监控摄像头-01',
    type: 'camera',
    location: '大棚C区',
    status: 'offline',
    battery: 45,
    lastUpdate: '2024-01-15 13:15:00',
    description: '24小时监控作物生长状况。',
    image: 'https://picsum.photos/400/300?random=4'
  },
  {
    id: 'dev005',
    name: '自动喷灌设备',
    type: 'irrigation',
    location: '大棚B区',
    status: 'maintenance',
    battery: 60,
    lastUpdate: '2024-01-15 12:00:00',
    description: '自动喷灌系统，支持定时和条件触发。',
    image: 'https://picsum.photos/400/300?random=5'
  }
]

// 设备表单数据
const deviceForm = ref({
  name: '',
  type: '',
  location: '',
  description: '',
  image: '',
  parameters: {
    interval: 30,
    threshold: 80
  }
})

// 控制表单数据
const controlForm = ref({
  power: true,
  irrigation: false,
  interval: 30,
  threshold: 80
})

// 表单验证规则
const deviceRules = {
  name: [
    { required: true, message: '请输入设备名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ],
  location: [
    { required: true, message: '请输入设备位置', trigger: 'blur' }
  ]
}

// 计算属性
const averageTemperature = computed(() => {
  return 25.6
})

const averageHumidity = computed(() => {
  return 68.2
})

const averageSoilMoisture = computed(() => {
  return 72.5
})

const averageLight = computed(() => {
  return 45000
})

const totalDevices = computed(() => {
  return devices.value.length
})

const onlineDevices = computed(() => {
  return devices.value.filter(dev => dev.status === 'online').length
})

const errorDevices = computed(() => {
  return devices.value.filter(dev => dev.status === 'error').length
})

const dataPoints = computed(() => {
  return 12580
})

// 方法
const fetchDevices = async () => {
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    devices.value = mockDevices
    ElMessage.success('设备列表加载成功')
  } catch (e) {
    ElMessage.error('获取设备列表失败')
  }
}

const refreshData = () => {
  fetchDevices()
}

const addDevice = () => {
  deviceFormTitle.value = '添加设备'
  deviceForm.value = {
    name: '',
    type: '',
    location: '',
    description: '',
    image: '',
    parameters: {
      interval: 30,
      threshold: 80
    }
  }
  deviceFormVisible.value = true
}

const editDevice = (device) => {
  deviceFormTitle.value = '编辑设备'
  deviceForm.value = { ...device }
  deviceFormVisible.value = true
}

const submitDeviceForm = async () => {
  try {
    await deviceFormRef.value.validate()
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success(deviceFormTitle.value === '添加设备' ? '设备添加成功' : '设备信息更新成功')
    deviceFormVisible.value = false
    fetchDevices()
  } catch (error) {
    ElMessage.error('表单验证失败')
  }
}

const deleteDevice = async (device) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除设备"${device.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    devices.value = devices.value.filter(d => d.id !== device.id)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}

const viewDeviceDetail = (device) => {
  currentDevice.value = device
  deviceDetailVisible.value = true
  loadDeviceData(device.id)
}

const controlDevice = (device) => {
  currentDevice.value = device
  controlForm.value = {
    power: device.status === 'online',
    irrigation: false,
    interval: 30,
    threshold: 80
  }
  controlVisible.value = true
}

const maintainDevice = (device) => {
  ElMessage.info(`设备 ${device.name} 已进入维护模式`)
}

const submitControl = async () => {
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('控制指令发送成功')
    controlVisible.value = false
    fetchDevices()
  } catch (error) {
    ElMessage.error('控制指令发送失败')
  }
}

const showAnalytics = () => {
  analyticsVisible.value = true
}

const showAlerts = () => {
  alertsVisible.value = true
  loadAlerts()
}

const handleSearch = () => {
  let filteredDevices = [...mockDevices]
  
  if (searchForm.value.keyword) {
    const keyword = searchForm.value.keyword.toLowerCase()
    filteredDevices = filteredDevices.filter(device => 
      device.name.toLowerCase().includes(keyword) ||
      device.location.toLowerCase().includes(keyword)
    )
  }
  
  if (searchForm.value.status) {
    filteredDevices = filteredDevices.filter(device => 
      device.status === searchForm.value.status
    )
  }
  
  if (searchForm.value.type) {
    filteredDevices = filteredDevices.filter(device => 
      device.type === searchForm.value.type
    )
  }
  
  devices.value = filteredDevices
  
  if (filteredDevices.length === 0) {
    ElMessage.info('没有找到匹配的设备')
  } else {
    ElMessage.success(`找到 ${filteredDevices.length} 台设备`)
  }
}

const resetSearch = () => {
  searchForm.value = {
    keyword: '',
    status: '',
    type: '',
    dateRange: []
  }
  devices.value = [...mockDevices]
  ElMessage.success('搜索条件已重置')
}

const loadDeviceData = (deviceId) => {
  deviceData.value = [
    { label: '温度', value: '25.6', unit: '°C', status: 'normal', statusText: '正常' },
    { label: '湿度', value: '68.2', unit: '%', status: 'normal', statusText: '正常' },
    { label: '土壤湿度', value: '72.5', unit: '%', status: 'normal', statusText: '正常' },
    { label: '光照强度', value: '45000', unit: ' lux', status: 'normal', statusText: '正常' }
  ]
}

const loadAlerts = () => {
  alerts.value = [
    {
      id: 'alert001',
      device: '温湿度传感器-01',
      type: 'temperature',
      message: '温度超过阈值：28.5°C',
      time: '2024-01-15 14:25:00',
      status: 'active'
    },
    {
      id: 'alert002',
      device: '监控摄像头-01',
      type: 'device',
      message: '设备离线超过30分钟',
      time: '2024-01-15 13:15:00',
      status: 'active'
    },
    {
      id: 'alert003',
      device: '土壤传感器-01',
      type: 'soil',
      message: '土壤湿度低于阈值：45%',
      time: '2024-01-15 12:30:00',
      status: 'handled'
    }
  ]
}

const addAlert = () => {
  ElMessage.info('添加告警规则功能开发中')
}

const handleAlert = (alert) => {
  alert.status = 'handled'
  ElMessage.success('告警已处理')
}

const deleteAlert = (alert) => {
  alerts.value = alerts.value.filter(a => a.id !== alert.id)
  ElMessage.success('告警已删除')
}

const clearAllAlerts = () => {
  alerts.value = []
  ElMessage.success('所有告警已清空')
}

const getBatteryColor = (battery) => {
  if (battery > 80) return '#67C23A'
  if (battery > 50) return '#E6A23C'
  return '#F56C6C'
}

const handlePowerChange = (value) => {
  console.log('电源状态:', value)
}

const handleIrrigationChange = (value) => {
  console.log('灌溉状态:', value)
}

const handleClose = () => {
  deviceDetailVisible.value = false
  currentDevice.value = null
  deviceData.value = []
}

const handleFormClose = () => {
  deviceFormVisible.value = false
  deviceFormRef.value?.resetFields()
}

const handleControlClose = () => {
  controlVisible.value = false
}

const handleAnalyticsClose = () => {
  analyticsVisible.value = false
}

const handleAlertsClose = () => {
  alertsVisible.value = false
}

// 获取默认设备图片
const getDefaultDeviceImage = (deviceType) => {
  const defaultImages = {
    sensor: 'https://picsum.photos/400/300?random=10',
    controller: 'https://picsum.photos/400/300?random=11',
    camera: 'https://picsum.photos/400/300?random=12',
    irrigation: 'https://picsum.photos/400/300?random=13'
  }
  return defaultImages[deviceType] || defaultImages.sensor
}

// 上传设备图片
const uploadDeviceImage = () => {
  ElMessage.info('图片上传功能开发中，当前使用默认图片')
}

// 选择设备图片
const selectDeviceImage = () => {
  // 模拟图片选择，实际项目中可以使用文件上传组件
  const sampleImages = [
    'https://picsum.photos/400/300?random=20',
    'https://picsum.photos/400/300?random=21',
    'https://picsum.photos/400/300?random=22'
  ]
  
  ElMessageBox.confirm(
    '选择图片方式',
    '选择图片',
    {
      confirmButtonText: '使用示例图片',
      cancelButtonText: '取消',
      type: 'info',
    }
  ).then(() => {
    deviceForm.value.image = sampleImages[Math.floor(Math.random() * sampleImages.length)]
    ElMessage.success('图片已选择')
  }).catch(() => {
    ElMessage.info('已取消选择')
  })
}

onMounted(fetchDevices)
</script>

<style scoped>
.smart-agriculture-container {
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

.overview-card {
  margin-bottom: 20px;
}

.overview-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.overview-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.overview-icon.temperature {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
}

.overview-icon.humidity {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
}

.overview-icon.soil {
  background: linear-gradient(135deg, #a29bfe, #6c5ce7);
}

.overview-icon.light {
  background: linear-gradient(135deg, #fdcb6e, #e17055);
}

.overview-info {
  flex: 1;
}

.overview-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.overview-label {
  color: #606266;
  font-size: 14px;
}

.search-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.clickable-title {
  color: #409eff;
  cursor: pointer;
}

.clickable-title:hover {
  text-decoration: underline;
}

.device-detail {
  padding: 20px;
}

.info-card,
.data-card,
.chart-card {
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

.data-item {
  text-align: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 10px;
}

.data-label {
  color: #606266;
  font-size: 14px;
  margin-bottom: 5px;
}

.data-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.data-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.data-status.normal {
  background: #f0f9ff;
  color: #67c23a;
}

.data-status.warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.data-status.danger {
  background: #fef0f0;
  color: #f56c6c;
}

.control-panel {
  padding: 20px;
}

.control-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.control-item:last-child {
  border-bottom: none;
}

.analytics-content {
  padding: 20px;
}

.alerts-content {
  padding: 20px;
}

.alerts-header {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  padding: 20px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.stat-label {
  color: #606266;
  font-size: 14px;
}

/* 设备图片样式 */
.device-image-section {
  margin-bottom: 20px;
  text-align: center;
}

.device-image-container {
  position: relative;
  display: inline-block;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.device-image {
  width: 300px;
  height: 200px;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.device-image:hover {
  transform: scale(1.02);
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 20px 10px 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.device-image-container:hover .image-overlay {
  opacity: 1;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  background: #f5f7fa;
  color: #909399;
  font-size: 14px;
}

.image-error .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

/* 表单图片上传样式 */
.form-image-upload {
  text-align: center;
}

.form-device-image {
  width: 200px;
  height: 150px;
  border-radius: 8px;
  border: 2px solid #e4e7ed;
}

.form-image-placeholder {
  width: 200px;
  height: 150px;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 14px;
  margin: 0 auto;
}

.form-image-placeholder .el-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .smart-agriculture-container {
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
  
  .search-section .el-col {
    margin-bottom: 10px;
  }
  
  .overview-content {
    flex-direction: column;
    text-align: center;
  }
  
  .device-image {
    width: 100%;
    max-width: 300px;
    height: auto;
    min-height: 150px;
  }
}
</style> 