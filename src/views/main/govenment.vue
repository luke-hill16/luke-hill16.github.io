<template>
    <div class="ai-management-container">
      <div class="page-header">
        <h2>AI管理</h2>
        <div class="header-actions">
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            新建AI模型
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
                  <el-icon><Cpu /></el-icon>
                </div>
                <div class="card-info">
                  <div class="card-title">AI模型总数</div>
                  <div class="card-value">{{ aiStats.totalModels }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="overview-card">
              <div class="card-content">
                <div class="card-icon success">
                  <el-icon><Connection /></el-icon>
                </div>
                <div class="card-info">
                  <div class="card-title">运行中模型</div>
                  <div class="card-value">{{ aiStats.runningModels }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="overview-card">
              <div class="card-content">
                <div class="card-icon warning">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="card-info">
                  <div class="card-title">训练中模型</div>
                  <div class="card-value">{{ aiStats.trainingModels }}</div>
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
                  <div class="card-title">平均准确率</div>
                  <div class="card-value">{{ aiStats.averageAccuracy }}%</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
  
      <!-- AI智能检索区域 -->
      <div class="ai-search-section">
        <el-card class="ai-search-card">
          <template #header>
            <div class="ai-search-header">
              <el-icon><Star /></el-icon>
              <span>AI智能检索</span>
            </div>
          </template>
          
          <div class="ai-search-content">
            <el-row :gutter="20">
              <el-col :span="16">
                <el-input
                  v-model="aiSearchQuery"
                  placeholder="请输入自然语言描述，如：查找准确率大于90%的文本分类模型，或者：显示最近一周训练的模型"
                  type="textarea"
                  :rows="3"
                  @keyup.enter="handleAISearch"
                >
                  <template #prefix>
                    <el-icon><ChatLineRound /></el-icon>
                  </template>
                </el-input>
              </el-col>
              <el-col :span="8">
                <div class="ai-search-actions">
                  <el-button type="primary" @click="handleAISearch" :loading="aiSearchLoading">
                    <el-icon><Search /></el-icon>
                    AI检索
                  </el-button>
                  <el-button @click="clearAISearch">清空</el-button>
                </div>
              </el-col>
            </el-row>
            
            <!-- AI解析结果 -->
            <div v-if="aiSearchResult" class="ai-search-result">
              <el-alert
                :title="`AI解析结果：${aiSearchResult.summary}`"
                type="info"
                :closable="false"
                show-icon
              >
                <template #default>
                  <div class="ai-result-details">
                    <p><strong>解析条件：</strong>{{ aiSearchResult.conditions }}</p>
                    <p><strong>匹配数量：</strong>{{ aiSearchResult.matchCount }} 个模型</p>
                  </div>
                </template>
              </el-alert>
            </div>
          </div>
        </el-card>
      </div>
  
      <!-- 传统搜索和筛选区域 -->
      <div class="search-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.modelName"
              placeholder="模型名称"
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
            <el-select v-model="searchForm.modelType" placeholder="模型类型" clearable @change="handleSearch">
              <el-option label="文本分类" value="text_classification" />
              <el-option label="图像识别" value="image_recognition" />
              <el-option label="语音识别" value="speech_recognition" />
              <el-option label="推荐系统" value="recommendation" />
              <el-option label="自然语言处理" value="nlp" />
              <el-option label="计算机视觉" value="computer_vision" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="searchForm.status" placeholder="运行状态" clearable @change="handleSearch">
              <el-option label="运行中" value="running" />
              <el-option label="训练中" value="training" />
              <el-option label="已停止" value="stopped" />
              <el-option label="部署中" value="deploying" />
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
  
      <!-- AI模型列表 -->
      <div class="ai-model-list">
        <el-table :data="aiModelList" v-loading="loading" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="modelName" label="模型名称" />
          <el-table-column prop="modelType" label="模型类型" width="120">
            <template #default="scope">
              <el-tag :type="getModelTypeTagType(scope.row.modelType)">
                {{ getModelTypeLabel(scope.row.modelType) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="accuracy" label="准确率" width="100">
            <template #default="scope">
              <el-tag :type="getAccuracyTagType(scope.row.accuracy)">
                {{ scope.row.accuracy }}%
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="运行状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ getStatusLabel(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="version" label="版本" width="100" />
          <el-table-column prop="createTime" label="创建时间" width="150" />
          <el-table-column label="操作" width="350" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewModel(scope.row)">查看</el-button>
              <el-button size="small" type="primary" @click="editModel(scope.row)">编辑</el-button>
              <el-button 
                size="small" 
                type="success" 
                @click="startModel(scope.row)"
                :disabled="scope.row.status === 'running'"
              >
                启动
              </el-button>
              <el-button 
                size="small" 
                type="warning" 
                @click="stopModel(scope.row)"
                :disabled="scope.row.status !== 'running'"
              >
                停止
              </el-button>
              <el-button 
                size="small" 
                type="info" 
                @click="deployModel(scope.row)"
                :disabled="scope.row.status !== 'stopped'"
              >
                部署
              </el-button>
              <el-button size="small" type="danger" @click="deleteModel(scope.row)">删除</el-button>
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
  
      <!-- 添加/编辑AI模型对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="1000px"
        @close="resetForm"
      >
        <el-form :model="aiModelForm" :rules="rules" ref="aiModelFormRef" label-width="120px">
          <el-tabs v-model="activeTab" type="border-card">
            <!-- 基本信息 -->
            <el-tab-pane label="基本信息" name="basic">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="模型名称" prop="modelName">
                    <el-input v-model="aiModelForm.modelName" placeholder="请输入模型名称" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="模型类型" prop="modelType">
                    <el-select v-model="aiModelForm.modelType" placeholder="请选择模型类型" style="width: 100%">
                      <el-option label="文本分类" value="text_classification" />
                      <el-option label="图像识别" value="image_recognition" />
                      <el-option label="语音识别" value="speech_recognition" />
                      <el-option label="推荐系统" value="recommendation" />
                      <el-option label="自然语言处理" value="nlp" />
                      <el-option label="计算机视觉" value="computer_vision" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="模型版本" prop="version">
                    <el-input v-model="aiModelForm.version" placeholder="请输入版本号，如：v1.0.0" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="准确率" prop="accuracy">
                    <el-input-number 
                      v-model="aiModelForm.accuracy" 
                      :min="0" 
                      :max="100" 
                      :precision="2" 
                      style="width: 100%" 
                    />
                    <span style="margin-left: 10px;">%</span>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="训练数据集" prop="dataset">
                    <el-input v-model="aiModelForm.dataset" placeholder="请输入训练数据集名称" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="模型大小" prop="modelSize">
                    <el-input-number 
                      v-model="aiModelForm.modelSize" 
                      :min="0" 
                      :precision="2" 
                      style="width: 100%" 
                    />
                    <span style="margin-left: 10px;">MB</span>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="模型描述" prop="description">
                <el-input
                  v-model="aiModelForm.description"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入模型描述"
                />
              </el-form-item>
            </el-tab-pane>
  
            <!-- 训练配置 -->
            <el-tab-pane label="训练配置" name="training">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="学习率" prop="learningRate">
                    <el-input-number 
                      v-model="aiModelForm.learningRate" 
                      :min="0" 
                      :precision="6" 
                      style="width: 100%" 
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="批次大小" prop="batchSize">
                    <el-input-number 
                      v-model="aiModelForm.batchSize" 
                      :min="1" 
                      style="width: 100%" 
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="训练轮数" prop="epochs">
                    <el-input-number 
                      v-model="aiModelForm.epochs" 
                      :min="1" 
                      style="width: 100%" 
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="优化器" prop="optimizer">
                    <el-select v-model="aiModelForm.optimizer" placeholder="请选择优化器" style="width: 100%">
                      <el-option label="Adam" value="adam" />
                      <el-option label="SGD" value="sgd" />
                      <el-option label="RMSprop" value="rmsprop" />
                      <el-option label="Adagrad" value="adagrad" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="训练参数" prop="trainingParams">
                <el-input
                  v-model="aiModelForm.trainingParams"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入其他训练参数（JSON格式）"
                />
              </el-form-item>
            </el-tab-pane>
  
            <!-- 部署配置 -->
            <el-tab-pane label="部署配置" name="deployment">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="部署环境" prop="deploymentEnv">
                    <el-select v-model="aiModelForm.deploymentEnv" placeholder="请选择部署环境" style="width: 100%">
                      <el-option label="生产环境" value="production" />
                      <el-option label="测试环境" value="testing" />
                      <el-option label="开发环境" value="development" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="资源需求" prop="resourceRequirements">
                    <el-select v-model="aiModelForm.resourceRequirements" placeholder="请选择资源需求" style="width: 100%">
                      <el-option label="低配置" value="low" />
                      <el-option label="中配置" value="medium" />
                      <el-option label="高配置" value="high" />
                      <el-option label="GPU加速" value="gpu" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="API接口" prop="apiEndpoint">
                <el-input v-model="aiModelForm.apiEndpoint" placeholder="请输入API接口地址" />
              </el-form-item>
              <el-form-item label="部署说明" prop="deploymentNotes">
                <el-input
                  v-model="aiModelForm.deploymentNotes"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入部署说明"
                />
              </el-form-item>
            </el-tab-pane>
          </el-tabs>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitForm" :loading="submitting">保存模型</el-button>
          </div>
        </template>
      </el-dialog>
  
      <!-- AI模型详情对话框 -->
      <el-dialog v-model="detailVisible" title="AI模型详情" width="1000px">
        <div v-if="currentModel" class="ai-model-detail">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="模型名称">{{ currentModel.modelName }}</el-descriptions-item>
            <el-descriptions-item label="模型类型">
              <el-tag :type="getModelTypeTagType(currentModel.modelType)">
                {{ getModelTypeLabel(currentModel.modelType) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="准确率">
              <el-tag :type="getAccuracyTagType(currentModel.accuracy)">
                {{ currentModel.accuracy }}%
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="运行状态">
              <el-tag :type="getStatusTagType(currentModel.status)">
                {{ getStatusLabel(currentModel.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="版本">{{ currentModel.version }}</el-descriptions-item>
            <el-descriptions-item label="模型大小">{{ currentModel.modelSize }}MB</el-descriptions-item>
            <el-descriptions-item label="训练数据集">{{ currentModel.dataset }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ currentModel.createTime }}</el-descriptions-item>
            <el-descriptions-item label="模型描述" :span="2">{{ currentModel.description || '暂无描述' }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </el-dialog>
  
      <!-- 模型性能报告对话框 -->
      <el-dialog v-model="reportVisible" title="AI模型性能报告" width="1000px">
        <div v-if="currentReport" class="ai-performance-report">
          <div class="report-header">
            <h2>{{ currentReport.title }}</h2>
            <p class="report-meta">生成时间：{{ currentReport.generateTime }}</p>
          </div>
          
          <div class="report-content">
            <el-tabs v-model="reportActiveTab" type="border-card">
              <el-tab-pane label="性能概览" name="overview">
                <div class="report-section">
                  <h3>模型基本信息</h3>
                  <el-descriptions :column="2" border>
                    <el-descriptions-item label="模型名称">{{ currentReport.modelName }}</el-descriptions-item>
                    <el-descriptions-item label="模型类型">{{ currentReport.modelType }}</el-descriptions-item>
                    <el-descriptions-item label="版本">{{ currentReport.version }}</el-descriptions-item>
                    <el-descriptions-item label="准确率">{{ currentReport.accuracy }}%</el-descriptions-item>
                    <el-descriptions-item label="训练时间">{{ currentReport.trainingTime }}</el-descriptions-item>
                    <el-descriptions-item label="推理速度">{{ currentReport.inferenceSpeed }}ms</el-descriptions-item>
                  </el-descriptions>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="性能指标" name="metrics">
                <div class="report-section">
                  <h3>详细性能指标</h3>
                  <div class="metrics-analysis">
                    <div class="metrics-item">
                      <div class="metrics-label">精确率：</div>
                      <div class="metrics-value">{{ currentReport.precision }}%</div>
                    </div>
                    <div class="metrics-item">
                      <div class="metrics-label">召回率：</div>
                      <div class="metrics-value">{{ currentReport.recall }}%</div>
                    </div>
                    <div class="metrics-item">
                      <div class="metrics-label">F1分数：</div>
                      <div class="metrics-value">{{ currentReport.f1Score }}%</div>
                    </div>
                    <div class="metrics-item">
                      <div class="metrics-label">AUC：</div>
                      <div class="metrics-value">{{ currentReport.auc }}</div>
                    </div>
                  </div>
                  
                  <h4>混淆矩阵</h4>
                  <el-table :data="currentReport.confusionMatrix" stripe>
                    <el-table-column prop="actual" label="实际值" />
                    <el-table-column prop="predicted" label="预测值" />
                    <el-table-column prop="count" label="数量" />
                    <el-table-column prop="percentage" label="百分比" />
                  </el-table>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="训练历史" name="training">
                <div class="report-section">
                  <h3>训练过程</h3>
                  <div class="training-history">
                    <div v-for="(epoch, index) in currentReport.trainingHistory" :key="index" class="epoch-item">
                      <h4>第{{ epoch.epoch }}轮</h4>
                      <p>训练损失：{{ epoch.trainLoss }}</p>
                      <p>验证损失：{{ epoch.valLoss }}</p>
                      <p>验证准确率：{{ epoch.valAccuracy }}%</p>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
              
              <el-tab-pane label="优化建议" name="optimization">
                <div class="report-section">
                  <h3>模型优化建议</h3>
                  <el-timeline>
                    <el-timeline-item
                      v-for="(suggestion, index) in currentReport.optimizationSuggestions"
                      :key="index"
                      :timestamp="suggestion.priority"
                      :type="suggestion.type"
                    >
                      <h4>{{ suggestion.title }}</h4>
                      <p>{{ suggestion.description }}</p>
                      <p><strong>预期提升：</strong>{{ suggestion.expectedImprovement }}</p>
                    </el-timeline-item>
                  </el-timeline>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { Plus, Search, Cpu, Connection, TrendCharts, Clock, Star, ChatLineRound } from '@element-plus/icons-vue'
  
  // 响应式数据
  const loading = ref(false)
  const submitting = ref(false)
  const dialogVisible = ref(false)
  const detailVisible = ref(false)
  const reportVisible = ref(false)
  const aiModelFormRef = ref()
  const currentModel = ref(null)
  const currentReport = ref(null)
  const activeTab = ref('basic')
  const reportActiveTab = ref('overview')
  
  // AI检索相关
  const aiSearchQuery = ref('')
  const aiSearchLoading = ref(false)
  const aiSearchResult = ref(null)
  
  // 搜索表单
  const searchForm = reactive({
    modelName: '',
    modelType: '',
    status: ''
  })
  
  // 分页
  const pagination = reactive({
    currentPage: 1,
    pageSize: 10,
    total: 0
  })
  
  // AI模型表单
  const aiModelForm = reactive({
    id: null,
    modelName: '',
    modelType: '',
    version: '',
    accuracy: 0,
    dataset: '',
    modelSize: 0,
    description: '',
    learningRate: 0.001,
    batchSize: 32,
    epochs: 100,
    optimizer: 'adam',
    trainingParams: '',
    deploymentEnv: 'development',
    resourceRequirements: 'medium',
    apiEndpoint: '',
    deploymentNotes: ''
  })
  
  // 表单验证规则
  const rules = {
    modelName: [
      { required: true, message: '请输入模型名称', trigger: 'blur' },
      { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
    ],
    modelType: [
      { required: true, message: '请选择模型类型', trigger: 'change' }
    ],
    version: [
      { required: true, message: '请输入版本号', trigger: 'blur' }
    ],
    accuracy: [
      { required: true, message: '请输入准确率', trigger: 'blur' }
    ],
    dataset: [
      { required: true, message: '请输入训练数据集', trigger: 'blur' }
    ]
  }
  
  // 统计数据
  const aiStats = reactive({
    totalModels: 0,
    runningModels: 0,
    trainingModels: 0,
    averageAccuracy: 0
  })
  
  // AI模型列表
  const aiModelList = ref([
    {
      id: 1,
      modelName: 'BERT文本分类模型',
      modelType: 'text_classification',
      accuracy: 95.2,
      status: 'running',
      version: 'v1.0.0',
      dataset: 'IMDB电影评论',
      modelSize: 420,
      description: '基于BERT的文本分类模型，用于情感分析',
      createTime: '2024-01-15 10:00:00'
    },
    {
      id: 2,
      modelName: 'ResNet图像识别模型',
      modelType: 'image_recognition',
      accuracy: 92.8,
      status: 'training',
      version: 'v2.1.0',
      dataset: 'ImageNet',
      modelSize: 98,
      description: '基于ResNet的图像分类模型',
      createTime: '2024-02-01 14:30:00'
    },
    {
      id: 3,
      modelName: 'LSTM语音识别模型',
      modelType: 'speech_recognition',
      accuracy: 88.5,
      status: 'stopped',
      version: 'v1.5.0',
      dataset: 'LibriSpeech',
      modelSize: 156,
      description: '基于LSTM的语音识别模型',
      createTime: '2024-02-15 09:15:00'
    }
  ])
  
  // 计算属性
  const dialogTitle = computed(() => {
    return aiModelForm.id ? '编辑AI模型' : '新建AI模型'
  })
  
  // 方法
  const getModelTypeLabel = (modelType) => {
    const typeMap = {
      text_classification: '文本分类',
      image_recognition: '图像识别',
      speech_recognition: '语音识别',
      recommendation: '推荐系统',
      nlp: '自然语言处理',
      computer_vision: '计算机视觉'
    }
    return typeMap[modelType] || '未知'
  }
  
  const getModelTypeTagType = (modelType) => {
    const typeMap = {
      text_classification: 'primary',
      image_recognition: 'success',
      speech_recognition: 'warning',
      recommendation: 'info',
      nlp: 'danger',
      computer_vision: 'danger'
    }
    return typeMap[modelType] || ''
  }
  
  const getAccuracyTagType = (accuracy) => {
    if (accuracy >= 95) return 'success'
    if (accuracy >= 90) return 'primary'
    if (accuracy >= 85) return 'warning'
    return 'danger'
  }
  
  const getStatusLabel = (status) => {
    const statusMap = {
      running: '运行中',
      training: '训练中',
      stopped: '已停止',
      deploying: '部署中'
    }
    return statusMap[status] || '未知'
  }
  
  const getStatusTagType = (status) => {
    const statusMap = {
      running: 'success',
      training: 'warning',
      stopped: 'info',
      deploying: 'primary'
    }
    return statusMap[status] || ''
  }
  
  // AI检索功能
  const handleAISearch = async () => {
    if (!aiSearchQuery.value.trim()) {
      ElMessage.warning('请输入检索条件')
      return
    }
    
    aiSearchLoading.value = true
    try {
      // 模拟AI解析自然语言查询
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // 解析查询条件
      const query = aiSearchQuery.value.toLowerCase()
      let conditions = []
      let matchCount = 0
      
      if (query.includes('准确率') && query.includes('大于')) {
        const match = query.match(/准确率.*?大于.*?(\d+)/)
        if (match) {
          const threshold = parseInt(match[1])
          conditions.push(`准确率 > ${threshold}%`)
          matchCount = aiModelList.value.filter(model => model.accuracy > threshold).length
        }
      } else if (query.includes('最近') && query.includes('训练')) {
        conditions.push('最近一周创建的模型')
        const oneWeekAgo = new Date()
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
        matchCount = aiModelList.value.filter(model => new Date(model.createTime) > oneWeekAgo).length
      } else if (query.includes('文本分类')) {
        conditions.push('模型类型为文本分类')
        matchCount = aiModelList.value.filter(model => model.modelType === 'text_classification').length
      } else if (query.includes('运行中')) {
        conditions.push('状态为运行中')
        matchCount = aiModelList.value.filter(model => model.status === 'running').length
      } else {
        conditions.push('通用搜索')
        matchCount = aiModelList.value.length
      }
      
      aiSearchResult.value = {
        summary: `找到 ${matchCount} 个符合条件的模型`,
        conditions: conditions.join('，'),
        matchCount: matchCount
      }
      
      ElMessage.success('AI检索完成')
    } catch (error) {
      ElMessage.error('AI检索失败')
    } finally {
      aiSearchLoading.value = false
    }
  }
  
  const clearAISearch = () => {
    aiSearchQuery.value = ''
    aiSearchResult.value = null
  }
  
  const showAddDialog = () => {
    aiModelForm.id = null
    activeTab.value = 'basic'
    dialogVisible.value = true
  }
  
  const editModel = (row) => {
    Object.assign(aiModelForm, row)
    activeTab.value = 'basic'
    dialogVisible.value = true
  }
  
  const viewModel = (row) => {
    currentModel.value = row
    detailVisible.value = true
  }
  
  const deleteModel = async (row) => {
    try {
      await ElMessageBox.confirm(
        `确定要删除模型"${row.modelName}"吗？`,
        '确认删除',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      // 模拟删除操作
      const index = aiModelList.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        aiModelList.value.splice(index, 1)
        updateStats()
        ElMessage.success('删除成功')
      }
    } catch (error) {
      // 用户取消删除
    }
  }
  
  const startModel = async (row) => {
    loading.value = true
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const index = aiModelList.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        aiModelList.value[index].status = 'running'
      }
      
      updateStats()
      ElMessage.success('模型启动成功')
    } catch (error) {
      ElMessage.error('启动失败')
    } finally {
      loading.value = false
    }
  }
  
  const stopModel = async (row) => {
    loading.value = true
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const index = aiModelList.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        aiModelList.value[index].status = 'stopped'
      }
      
      updateStats()
      ElMessage.success('模型停止成功')
    } catch (error) {
      ElMessage.error('停止失败')
    } finally {
      loading.value = false
    }
  }
  
  const deployModel = async (row) => {
    loading.value = true
    try {
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      const index = aiModelList.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        aiModelList.value[index].status = 'running'
      }
      
      updateStats()
      ElMessage.success('模型部署成功')
    } catch (error) {
      ElMessage.error('部署失败')
    } finally {
      loading.value = false
    }
  }
  
  const submitForm = async () => {
    if (!aiModelFormRef.value) return
    
    try {
      await aiModelFormRef.value.validate()
      submitting.value = true
      
      // 模拟提交操作
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      if (aiModelForm.id) {
        // 编辑
        const index = aiModelList.value.findIndex(item => item.id === aiModelForm.id)
        if (index > -1) {
          aiModelList.value[index] = { 
            ...aiModelForm,
            createTime: aiModelList.value[index].createTime
          }
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newModel = {
          ...aiModelForm,
          id: Date.now(),
          status: 'stopped',
          createTime: new Date().toLocaleString()
        }
        aiModelList.value.unshift(newModel)
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
    if (aiModelFormRef.value) {
      aiModelFormRef.value.resetFields()
    }
    Object.assign(aiModelForm, {
      id: null,
      modelName: '',
      modelType: '',
      version: '',
      accuracy: 0,
      dataset: '',
      modelSize: 0,
      description: '',
      learningRate: 0.001,
      batchSize: 32,
      epochs: 100,
      optimizer: 'adam',
      trainingParams: '',
      deploymentEnv: 'development',
      resourceRequirements: 'medium',
      apiEndpoint: '',
      deploymentNotes: ''
    })
  }
  
  const handleSearch = () => {
    pagination.currentPage = 1
    // 这里可以调用实际的搜索API
    console.log('搜索条件:', searchForm)
  }
  
  const resetSearch = () => {
    Object.assign(searchForm, {
      modelName: '',
      modelType: '',
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
  
  const updateStats = () => {
    aiStats.totalModels = aiModelList.value.length
    aiStats.runningModels = aiModelList.value.filter(item => item.status === 'running').length
    aiStats.trainingModels = aiModelList.value.filter(item => item.status === 'training').length
    aiStats.averageAccuracy = Math.floor(aiModelList.value.reduce((sum, model) => sum + model.accuracy, 0) / aiModelList.value.length)
  }
  
  // 生命周期
  onMounted(() => {
    updateStats()
    pagination.total = aiModelList.value.length
  })
  </script>
  
  <style scoped>
  .ai-management-container {
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
  
  .ai-search-section {
    margin-bottom: 30px;
  }
  
  .ai-search-card {
    border: 2px solid #e1f5fe;
    background: linear-gradient(135deg, #f8fdff, #f0f9ff);
  }
  
  .ai-search-header {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #409eff;
    font-weight: bold;
  }
  
  .ai-search-content {
    padding: 10px 0;
  }
  
  .ai-search-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    justify-content: center;
  }
  
  .ai-search-result {
    margin-top: 20px;
  }
  
  .ai-result-details {
    margin-top: 10px;
  }
  
  .ai-result-details p {
    margin: 5px 0;
    color: #606266;
  }
  
  .search-section {
    margin-bottom: 20px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
  }
  
  .ai-model-list {
    margin-top: 20px;
  }
  
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
  
  .ai-model-detail {
    padding: 20px 0;
  }
  
  .dialog-footer {
    text-align: right;
  }
  
  .ai-performance-report {
    padding: 20px 0;
  }
  
  .report-header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #ebeef5;
  }
  
  .report-header h2 {
    margin: 0 0 10px 0;
    color: #303133;
  }
  
  .report-meta {
    color: #909399;
    margin: 0;
  }
  
  .report-section {
    margin-bottom: 30px;
  }
  
  .report-section h3 {
    margin-bottom: 20px;
    color: #303133;
    border-left: 4px solid #409eff;
    padding-left: 15px;
  }
  
  .metrics-analysis {
    display: flex;
    gap: 30px;
    margin-bottom: 30px;
  }
  
  .metrics-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .metrics-label {
    font-weight: bold;
    color: #606266;
  }
  
  .metrics-value {
    font-size: 18px;
    font-weight: bold;
    color: #409eff;
  }
  
  .training-history {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .epoch-item {
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #67c23a;
  }
  
  .epoch-item h4 {
    margin: 0 0 10px 0;
    color: #303133;
  }
  
  .epoch-item p {
    margin: 5px 0;
    color: #606266;
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
  
  :deep(.el-tabs__content) {
    padding: 20px 0;
  }
  </style> 