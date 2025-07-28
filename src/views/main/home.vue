<template>
    <div class="home-container">
      <!-- 顶部标题栏 -->
      <div class="header-section">
        <h1 class="main-title">山东省电力作业管理系统</h1>
        <div class="time-info">{{ currentTime }}</div>
      </div>
  
      <div class="main-content">
        <!-- 左侧统计面板 -->
        <div class="left-panel">
          <!-- 今日作业统计 -->
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>今日作业统计</span>
              </div>
            </template>
            <div class="stat-grid">
              <div class="stat-item">
                <div class="stat-number">{{ todayStats.units }}</div>
                <div class="stat-label">作业单位</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ todayStats.personnel }}</div>
                <div class="stat-label">作业人员</div>
              </div>
            </div>
          </el-card>
  
          <!-- 专业类型作业情况 -->
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>专业类型作业情况</span>
              </div>
            </template>
            <div class="professional-stats">
              <div class="prof-item" v-for="item in professionalStats" :key="item.type">
                <div class="prof-info">
                  <span class="prof-name">{{ item.type }}</span>
                  <span class="prof-count">{{ item.count }}</span>
                </div>
                <el-progress :percentage="item.percentage" :color="item.color" />
              </div>
            </div>
          </el-card>
  
          <!-- 风险作业情况 -->
          <el-card class="stat-card">
            <template #header>
              <div class="card-header">
                <span>正在实施的二、三级风险作业</span>
              </div>
            </template>
            <div class="risk-list">
              <div class="risk-item" v-for="risk in riskOperations" :key="risk.id">
                <div class="risk-level" :class="`risk-${risk.level}`">
                  {{ risk.levelText }}
                </div>
                <div class="risk-content">
                  <div class="risk-title">{{ risk.title }}</div>
                  <div class="risk-location">{{ risk.location }}</div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
  
        <!-- 中间地图区域 -->
        <div class="center-panel">
          <el-card class="map-card">
            <template #header>
              <div class="card-header">
                <span>山东省各地市作业计划开展情况</span>
                <el-button size="small" @click="switchMapView" style="margin-left: 10px;">切换视图</el-button>
              </div>
            </template>
            <!-- 地图容器（可替换为ECharts/高德地图） -->
            <div class="map-container">
              <div class="map-title">山东省地图（占位）</div>
              <div class="city-stats">
                <div class="city-item" v-for="city in cityStats" :key="city.name" @click="showCityDetail(city)">
                  <div class="city-name">{{ city.name }}</div>
                  <div class="city-numbers">
                    <span class="not-started" @click.stop="showCityDetail(city, '未开工')">{{ city.notStarted }}</span>
                    <span class="in-progress" @click.stop="showCityDetail(city, '已开工')">{{ city.inProgress }}</span>
                    <span class="completed" @click.stop="showCityDetail(city, '已完工')">{{ city.completed }}</span>
                  </div>
                  <div class="city-labels">
                    <span class="label">未开工</span>
                    <span class="label">已开工</span>
                    <span class="label">已完工</span>
                  </div>
                </div>
              </div>
              <!-- 省图切换按钮 -->
              <div class="province-switch">
                <el-button type="primary" size="small" @click="switchToProvinceMap">省图切换</el-button>
              </div>
            </div>
          </el-card>
  
          <!-- 地图下方：风险等级统计 -->
          <el-card class="risk-stat-card">
            <template #header>
              <div class="card-header">
                <span>作业风险等级/电网风险等级统计</span>
              </div>
            </template>
            <div class="risk-stat-grid">
              <div class="risk-stat-item" v-for="risk in riskLevelStats" :key="risk.level">
                <div class="risk-level-label">{{ risk.level }}</div>
                <el-progress :percentage="risk.count" :color="risk.color" />
                <div class="risk-level-count">{{ risk.count }} 项</div>
              </div>
            </div>
          </el-card>
        </div>
  
        <!-- 右侧异常与黑名单 -->
        <div class="right-panel">
          <el-card class="alert-card">
            <template #header>
              <div class="card-header">
                <span>异常告警</span>
              </div>
            </template>
            <ul class="alert-list">
              <li v-for="alert in alerts" :key="alert.id">
                <el-tag :type="alert.type">{{ alert.typeText }}</el-tag>
                <span class="alert-content">{{ alert.content }}</span>
              </li>
            </ul>
          </el-card>
  
          <el-card class="violation-card">
            <template #header>
              <div class="card-header">
                <span>违章情况</span>
              </div>
            </template>
            <ul class="violation-list">
              <li v-for="vio in violations" :key="vio.id">
                <span class="vio-content">{{ vio.content }}</span>
                <el-tag type="danger" v-if="vio.severe">严重</el-tag>
              </li>
            </ul>
          </el-card>
  
          <el-card class="blacklist-card">
            <template #header>
              <div class="card-header">
                <span>企业黑名单/负面清单</span>
              </div>
            </template>
            <ul class="blacklist-list">
              <li v-for="ent in blacklist" :key="ent.id">
                <span class="ent-name">{{ ent.name }}</span>
                <span class="ent-reason">{{ ent.reason }}</span>
              </li>
            </ul>
          </el-card>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  
  // 当前时间
  const currentTime = ref(new Date().toLocaleString())
  
  // 今日作业单位和人员统计
  const todayStats = ref({
    units: 32,
    personnel: 187
  })
  
  // 专业类型作业情况
  const professionalStats = ref([
    { type: '输电', count: 12, percentage: 40, color: '#409EFF' },
    { type: '变电', count: 8, percentage: 27, color: '#67C23A' },
    { type: '配电', count: 7, percentage: 23, color: '#E6A23C' },
    { type: '通信', count: 3, percentage: 10, color: '#F56C6C' }
  ])
  
  // 风险作业情况
  const riskOperations = ref([
    { id: 1, level: 2, levelText: '二级', title: '济南-变电检修', location: '济南市历城区' },
    { id: 2, level: 3, levelText: '三级', title: '青岛-线路施工', location: '青岛市黄岛区' }
  ])
  
  // 地市作业情况
  const cityStats = ref([
    { name: '济南', notStarted: 2, inProgress: 5, completed: 8 },
    { name: '青岛', notStarted: 1, inProgress: 3, completed: 6 },
    { name: '烟台', notStarted: 0, inProgress: 2, completed: 7 },
    { name: '潍坊', notStarted: 1, inProgress: 2, completed: 5 },
    { name: '临沂', notStarted: 0, inProgress: 1, completed: 4 }
    // ... 其他地市
  ])
  
  // 风险等级统计
  const riskLevelStats = ref([
    { level: '一级', count: 2, color: '#67C23A' },
    { level: '二级', count: 5, color: '#E6A23C' },
    { level: '三级', count: 3, color: '#F56C6C' }
  ])
  
  // 异常告警
  const alerts = ref([
    { id: 1, type: 'danger', typeText: '高危', content: '济南某作业点气体泄漏' },
    { id: 2, type: 'warning', typeText: '预警', content: '青岛某作业点人员未签到' }
  ])
  
  // 违章情况
  const violations = ref([
    { id: 1, content: '烟台某作业未佩戴安全帽', severe: true },
    { id: 2, content: '潍坊某作业未按规定操作', severe: false }
  ])
  
  // 黑名单
  const blacklist = ref([
    { id: 1, name: '山东某电力公司', reason: '多次违章' },
    { id: 2, name: '青岛某外包单位', reason: '安全事故' }
  ])
  
  // 省图切换
  const switchToProvinceMap = () => {
    ElMessage.info('切换到省级地图视图')
  }
  
  // 地市下钻
  const showCityDetail = (city, type) => {
    if (type) {
      ElMessage.info(`下钻到${city.name}，显示${type}：${city[type === '未开工' ? 'notStarted' : type === '已开工' ? 'inProgress' : 'completed']}`)
    } else {
      ElMessage.info(`下钻到${city.name}，显示未开工：${city.notStarted}，已开工：${city.inProgress}，已完工：${city.completed}`)
    }
  }
  
  // 切换地图视图
  const switchMapView = () => {
    ElMessage.info('切换地图视图')
  }
  
  // 更新时间
  onMounted(() => {
    setInterval(() => {
      currentTime.value = new Date().toLocaleString()
    }, 1000)
  })
  </script>
  
  <style scoped>
  .home-container {
    min-height: 10vh;
    background: #e0ecff;;
    padding: 0;
  }
  .header-section {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0px 0px 0 0px;
    position: relative;
    background: #e0ecff;
  }
  .main-title {
    font-size: 28px;
    font-weight: bold;
    color: #303133;
  }
  .time-info {
    font-size: 16px;
    color: #909399;
    position: absolute;
    right: 40px;        /* 右对齐 */
  }
  .main-content {
    display: flex;
    flex-direction: row;
    padding: 30px 60px;
    gap: 20px;
    background: #e0ecff;
  }
  .left-panel, .right-panel {
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    
  }
  .center-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .stat-card, .alert-card, .violation-card, .blacklist-card, .map-card, .risk-stat-card {
    margin-bottom: 0;
    height: 230px;  /* 设置固定高度 */
   display: flex;
   flex-direction: column;
  }
  /* 让卡片内容区域自适应剩余空间 */
.stat-card :deep(.el-card__body),
.alert-card :deep(.el-card__body),
.violation-card :deep(.el-card__body),
.blacklist-card :deep(.el-card__body),
.map-card :deep(.el-card__body),
.risk-stat-card :deep(.el-card__body) {
  flex: 1;
  overflow: auto;  /* 内容过多时可滚动 */
}

/* 地图卡片可以设置更大高度 */
.map-card {
  height: 400px;
}

/* 风险统计卡片可以设置更小高度 */
.risk-stat-card {
    height: 290px;  /* 从150px改为200px */
}
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .stat-grid {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }
  .stat-item {
    text-align: center;
  }
  .stat-number {
    font-size: 28px;
    color: #409EFF;
    font-weight: bold;
  }
  .stat-label {
    font-size: 14px;
    color: #606266;
  }
  .professional-stats {
    margin-top: 10px;
  }
  .prof-item {
    margin-bottom: 10px;
  }
  .prof-info {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
  }
  .risk-list {
    margin-top: 10px;
  }
  .risk-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
  }
  .risk-level {
    width: 40px;
    text-align: center;
    font-weight: bold;
    border-radius: 4px;
    margin-right: 10px;
    color: #e0ecff;
    padding: 2px 0;
  }
  .risk-2 {
    background: #E6A23C;
  }
  .risk-3 {
    background: #F56C6C;
  }
  .risk-content {
    flex: 1;
  }
  .map-card {
    min-height: 400px;
  }
  .map-container {
    width: 100%;
    height: 350px;
    background: #e0ecff;
    border-radius: 10px;
    position: relative;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .map-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  .city-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
  }
  .city-item {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(64,158,255,0.08);
    padding: 10px 16px;
    cursor: pointer;
    min-width: 120px;
    text-align: center;
    transition: box-shadow 0.2s;
  }
  .city-item:hover {
    box-shadow: 0 4px 16px rgba(64,158,255,0.18);
  }
  .city-name {
    font-weight: bold;
    color: #409EFF;
    margin-bottom: 4px;
  }
  .city-numbers {
    display: flex;
    justify-content: space-between;
    gap: 6px;
    font-size: 18px;
    margin-bottom: 2px;
  }
  .city-labels {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #909399;
  }
  .not-started { color: #909399; cursor: pointer; }
  .in-progress { color: #E6A23C; cursor: pointer; }
  .completed { color: #67C23A; cursor: pointer; }
  .province-switch {
    position: absolute;
    right: 20px;
    bottom: 20px;
  }
  .risk-stat-card {
    margin-top: 20px;
  }
  .risk-stat-grid {
    display: flex;
    gap: 20px;
    margin-top: 10px;
  }
  .risk-stat-item {
    flex: 1;
    text-align: center;
  }
  .risk-level-label {
    font-weight: bold;
    margin-bottom: 4px;
  }
  .risk-level-count {
    font-size: 14px;
    color: #606266;
    margin-top: 4px;
  }
  .alert-list, .violation-list, .blacklist-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .alert-list li, .violation-list li, .blacklist-list li {
    margin-bottom: 8px;
    font-size: 14px;
  }
  .alert-content, .vio-content, .ent-name, .ent-reason {
    margin-left: 8px;
  }
  .ent-name {
    font-weight: bold;
    color: #F56C6C;
  }
  .ent-reason {
    color: #909399;
    margin-left: 8px;
  }
  </style>








