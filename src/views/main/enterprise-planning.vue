<template>
  <div class="enterprise-planning-container">
    <div class="page-header">
      <h2>企业规划管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新建企业规划
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
                <el-icon><OfficeBuilding /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">企业总数</div>
                <div class="card-value">{{ planningStats.totalEnterprises }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="card-icon success">
                <el-icon><Document /></el-icon>
              </div>
              <div class="card-info">
                <div class="card-title">已生成报告</div>
                <div class="card-value">{{ planningStats.generatedReports }}</div>
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
                <div class="card-title">待完善信息</div>
                <div class="card-value">{{ planningStats.pendingInfo }}</div>
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
                <div class="card-title">平均政策匹配度</div>
                <div class="card-value">{{ planningStats.averageMatchRate }}%</div>
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
            v-model="searchForm.enterpriseName"
            placeholder="企业名称"
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
          <el-select v-model="searchForm.industry" placeholder="所属行业" clearable @change="handleSearch">
            <el-option label="制造业" value="manufacturing" />
            <el-option label="服务业" value="service" />
            <el-option label="农业" value="agriculture" />
            <el-option label="建筑业" value="construction" />
            <el-option label="信息技术" value="it" />
            <el-option label="金融业" value="finance" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="searchForm.status" placeholder="信息状态" clearable @change="handleSearch">
            <el-option label="信息完整" value="complete" />
            <el-option label="信息待完善" value="incomplete" />
            <el-option label="已生成报告" value="reported" />
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

    <!-- 企业列表 -->
    <div class="enterprise-list">
      <el-table :data="enterpriseList" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="enterpriseName" label="企业名称" />
        <el-table-column prop="industry" label="所属行业" width="120">
          <template #default="scope">
            <el-tag :type="getIndustryTagType(scope.row.industry)">
              {{ getIndustryLabel(scope.row.industry) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="scale" label="企业规模" width="120">
          <template #default="scope">
            <el-tag :type="getScaleTagType(scope.row.scale)">
              {{ getScaleLabel(scope.row.scale) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="infoStatus" label="信息状态" width="120">
          <template #default="scope">
            <el-tag :type="getInfoStatusTagType(scope.row.infoStatus)">
              {{ getInfoStatusLabel(scope.row.infoStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reportStatus" label="报告状态" width="120">
          <template #default="scope">
            <el-tag :type="getReportStatusTagType(scope.row.reportStatus)">
              {{ getReportStatusLabel(scope.row.reportStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="150" />
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewEnterprise(scope.row)">查看</el-button>
            <el-button size="small" type="primary" @click="editEnterprise(scope.row)">编辑信息</el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="generateReport(scope.row)"
              :disabled="scope.row.infoStatus !== 'complete'"
            >
              生成报告
            </el-button>
            <el-button 
              size="small" 
              type="warning" 
              @click="viewReport(scope.row)"
              :disabled="scope.row.reportStatus !== 'generated'"
            >
              查看报告
            </el-button>
            <el-button size="small" type="danger" @click="deleteEnterprise(scope.row)">删除</el-button>
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

    <!-- 添加/编辑企业信息对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="1000px"
      @close="resetForm"
    >
      <el-form :model="enterpriseForm" :rules="rules" ref="enterpriseFormRef" label-width="120px">
        <el-tabs v-model="activeTab" type="border-card">
          <!-- 基本信息 -->
          <el-tab-pane label="基本信息" name="basic">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="企业名称" prop="enterpriseName">
                  <el-input v-model="enterpriseForm.enterpriseName" placeholder="请输入企业名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="所属行业" prop="industry">
                  <el-select v-model="enterpriseForm.industry" placeholder="请选择所属行业" style="width: 100%">
                    <el-option label="制造业" value="manufacturing" />
                    <el-option label="服务业" value="service" />
                    <el-option label="农业" value="agriculture" />
                    <el-option label="建筑业" value="construction" />
                    <el-option label="信息技术" value="it" />
                    <el-option label="金融业" value="finance" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="企业规模" prop="scale">
                  <el-select v-model="enterpriseForm.scale" placeholder="请选择企业规模" style="width: 100%">
                    <el-option label="大型企业" value="large" />
                    <el-option label="中型企业" value="medium" />
                    <el-option label="小型企业" value="small" />
                    <el-option label="微型企业" value="micro" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="注册资本" prop="registeredCapital">
                  <el-input-number v-model="enterpriseForm.registeredCapital" :min="0" :precision="2" style="width: 100%" />
                  <span style="margin-left: 10px;">万元</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="成立时间" prop="establishDate">
                  <el-date-picker
                    v-model="enterpriseForm.establishDate"
                    type="date"
                    placeholder="选择成立时间"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="技术等级" prop="techLevel">
                  <el-select v-model="enterpriseForm.techLevel" placeholder="请选择技术等级" style="width: 100%">
                    <el-option label="高新技术企业" value="high-tech" />
                    <el-option label="科技型中小企业" value="tech-sme" />
                    <el-option label="一般企业" value="general" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="企业地址" prop="address">
              <el-input v-model="enterpriseForm.address" placeholder="请输入企业地址" />
            </el-form-item>
            <el-form-item label="企业描述" prop="description">
              <el-input
                v-model="enterpriseForm.description"
                type="textarea"
                :rows="3"
                placeholder="请输入企业描述"
              />
            </el-form-item>
          </el-tab-pane>

          <!-- 业务信息 -->
          <el-tab-pane label="业务信息" name="business">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="主营业务" prop="mainBusiness">
                  <el-input v-model="enterpriseForm.mainBusiness" placeholder="请输入主营业务" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="年营业额" prop="annualRevenue">
                  <el-input-number v-model="enterpriseForm.annualRevenue" :min="0" :precision="2" style="width: 100%" />
                  <span style="margin-left: 10px;">万元</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="员工人数" prop="employeeCount">
                  <el-input-number v-model="enterpriseForm.employeeCount" :min="0" style="width: 100%" />
                  <span style="margin-left: 10px;">人</span>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="研发投入" prop="rdInvestment">
                  <el-input-number v-model="enterpriseForm.rdInvestment" :min="0" :precision="2" style="width: 100%" />
                  <span style="margin-left: 10px;">万元</span>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="发展规划" prop="developmentPlan">
              <el-input
                v-model="enterpriseForm.developmentPlan"
                type="textarea"
                :rows="4"
                placeholder="请描述企业发展规划和目标"
              />
            </el-form-item>
          </el-tab-pane>

          <!-- 政策需求 -->
          <el-tab-pane label="政策需求" name="policy">
            <el-form-item label="政策需求类型" prop="policyNeeds">
              <el-checkbox-group v-model="enterpriseForm.policyNeeds">
                <el-checkbox label="financial">资金支持</el-checkbox>
                <el-checkbox label="tax">税收优惠</el-checkbox>
                <el-checkbox label="land">用地支持</el-checkbox>
                <el-checkbox label="talent">人才引进</el-checkbox>
                <el-checkbox label="tech">技术创新</el-checkbox>
                <el-checkbox label="market">市场开拓</el-checkbox>
                <el-checkbox label="export">出口支持</el-checkbox>
                <el-checkbox label="other">其他</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="具体需求描述" prop="policyDescription">
              <el-input
                v-model="enterpriseForm.policyDescription"
                type="textarea"
                :rows="4"
                placeholder="请详细描述政策需求"
              />
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">保存信息</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 企业详情对话框 -->
    <el-dialog v-model="detailVisible" title="企业详情" width="1000px">
      <div v-if="currentEnterprise" class="enterprise-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="企业名称">{{ currentEnterprise.enterpriseName }}</el-descriptions-item>
          <el-descriptions-item label="所属行业">
            <el-tag :type="getIndustryTagType(currentEnterprise.industry)">
              {{ getIndustryLabel(currentEnterprise.industry) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="企业规模">
            <el-tag :type="getScaleTagType(currentEnterprise.scale)">
              {{ getScaleLabel(currentEnterprise.scale) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="注册资本">{{ currentEnterprise.registeredCapital }}万元</el-descriptions-item>
          <el-descriptions-item label="成立时间">{{ currentEnterprise.establishDate }}</el-descriptions-item>
          <el-descriptions-item label="技术等级">{{ getTechLevelLabel(currentEnterprise.techLevel) }}</el-descriptions-item>
          <el-descriptions-item label="企业地址">{{ currentEnterprise.address }}</el-descriptions-item>
          <el-descriptions-item label="主营业务">{{ currentEnterprise.mainBusiness }}</el-descriptions-item>
          <el-descriptions-item label="年营业额">{{ currentEnterprise.annualRevenue }}万元</el-descriptions-item>
          <el-descriptions-item label="员工人数">{{ currentEnterprise.employeeCount }}人</el-descriptions-item>
          <el-descriptions-item label="研发投入">{{ currentEnterprise.rdInvestment }}万元</el-descriptions-item>
          <el-descriptions-item label="信息状态">
            <el-tag :type="getInfoStatusTagType(currentEnterprise.infoStatus)">
              {{ getInfoStatusLabel(currentEnterprise.infoStatus) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="报告状态">
            <el-tag :type="getReportStatusTagType(currentEnterprise.reportStatus)">
              {{ getReportStatusLabel(currentEnterprise.reportStatus) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="企业描述" :span="2">{{ currentEnterprise.description || '暂无描述' }}</el-descriptions-item>
          <el-descriptions-item label="发展规划" :span="2">{{ currentEnterprise.developmentPlan || '暂无规划' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 政策详情对话框 -->
    <el-dialog v-model="policyDetailVisible" title="政策匹配详情" width="800px">
      <div v-if="currentPolicy" class="policy-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="政策名称">{{ currentPolicy.name }}</el-descriptions-item>
          <el-descriptions-item label="政策类别">
            <el-tag :type="getPolicyCategoryTagType(currentPolicy.category)">
              {{ currentPolicy.categoryName }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="匹配度">
            <el-tag :type="getScoreTagType(currentPolicy.matchScore)">
              {{ currentPolicy.matchScore }}%
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="支持金额">{{ currentPolicy.supportAmount }}</el-descriptions-item>
          <el-descriptions-item label="有效期">{{ currentPolicy.validPeriod }}</el-descriptions-item>
          <el-descriptions-item label="申请要求">{{ currentPolicy.requirements.join('、') }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="match-details">
          <h4>AI匹配分析详情</h4>
          <div class="match-detail-list">
            <div 
              v-for="(detail, index) in currentPolicy.matchDetails" 
              :key="index" 
              class="match-detail-item"
              :class="{ 'positive': detail.startsWith('✓'), 'warning': detail.startsWith('⚠') }"
            >
              <el-icon v-if="detail.startsWith('✓')" class="detail-icon success"><CircleCheck /></el-icon>
              <el-icon v-else-if="detail.startsWith('⚠')" class="detail-icon warning"><Warning /></el-icon>
              <span>{{ detail }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 规划报告对话框 -->
    <el-dialog v-model="reportVisible" title="企业规划报告" width="1000px">
      <div v-if="currentReport" class="planning-report">
        <div class="report-header">
          <h2>{{ currentReport.title }}</h2>
          <p class="report-meta">生成时间：{{ currentReport.generateTime }}</p>
        </div>
        
        <div class="report-content">
          <el-tabs v-model="reportActiveTab" type="border-card">
            <el-tab-pane label="企业概况" name="overview">
              <div class="report-section">
                <h3>企业基本信息</h3>
                <el-descriptions :column="2" border>
                  <el-descriptions-item label="企业名称">{{ currentReport.enterpriseName }}</el-descriptions-item>
                  <el-descriptions-item label="所属行业">{{ currentReport.industry }}</el-descriptions-item>
                  <el-descriptions-item label="企业规模">{{ currentReport.scale }}</el-descriptions-item>
                  <el-descriptions-item label="注册资本">{{ currentReport.registeredCapital }}万元</el-descriptions-item>
                  <el-descriptions-item label="成立时间">{{ currentReport.establishDate }}</el-descriptions-item>
                  <el-descriptions-item label="员工人数">{{ currentReport.employeeCount }}人</el-descriptions-item>
                </el-descriptions>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="政策分析" name="policy">
              <div class="report-section">
                <h3>AI政策匹配分析</h3>
                
                <!-- 企业特征分析 -->
                <div v-if="currentReport.aiAnalysis" class="ai-analysis-section">
                  <h4>企业特征分析</h4>
                  <el-row :gutter="20" class="feature-cards">
                    <el-col :span="8">
                      <el-card class="feature-card">
                        <div class="feature-header">
                          <el-icon><TrendCharts /></el-icon>
                          <span>行业优势</span>
                        </div>
                        <div class="feature-score">{{ currentReport.aiAnalysis.enterpriseFeatures.industryStrength }}分</div>
                        <div class="feature-desc">基于行业政策支持力度评估</div>
                      </el-card>
                    </el-col>
                    <el-col :span="8">
                      <el-card class="feature-card">
                        <div class="feature-header">
                          <el-icon><OfficeBuilding /></el-icon>
                          <span>规模优势</span>
                        </div>
                        <div class="feature-score">{{ currentReport.aiAnalysis.enterpriseFeatures.scaleAdvantage }}分</div>
                        <div class="feature-desc">基于企业规模的政策匹配度</div>
                      </el-card>
                    </el-col>
                    <el-col :span="8">
                      <el-card class="feature-card">
                        <div class="feature-header">
                          <el-icon><Document /></el-icon>
                          <span>技术等级</span>
                        </div>
                        <div class="feature-score">{{ currentReport.aiAnalysis.enterpriseFeatures.techLevel }}分</div>
                        <div class="feature-desc">基于技术水平的政策支持</div>
                      </el-card>
                    </el-col>
                  </el-row>
                  
                  <el-row :gutter="20" class="feature-cards">
                    <el-col :span="8">
                      <el-card class="feature-card">
                        <div class="feature-header">
                          <el-icon><TrendCharts /></el-icon>
                          <span>财务健康度</span>
                        </div>
                        <div class="feature-score">{{ currentReport.aiAnalysis.enterpriseFeatures.financialHealth }}分</div>
                        <div class="feature-desc">人均营收：{{ Math.round(currentReport.annualRevenue / currentReport.employeeCount) }}万元</div>
                      </el-card>
                    </el-col>
                    <el-col :span="8">
                      <el-card class="feature-card">
                        <div class="feature-header">
                          <el-icon><TrendCharts /></el-icon>
                          <span>成长潜力</span>
                        </div>
                        <div class="feature-score">{{ currentReport.aiAnalysis.enterpriseFeatures.growthPotential }}分</div>
                        <div class="feature-desc">研发投入比：{{ Math.round((currentReport.rdInvestment / currentReport.annualRevenue) * 100) }}%</div>
                      </el-card>
                    </el-col>
                    <el-col :span="8">
                      <el-card class="feature-card">
                        <div class="feature-header">
                          <el-icon><Clock /></el-icon>
                          <span>风险因素</span>
                        </div>
                        <div class="feature-score">{{ currentReport.aiAnalysis.enterpriseFeatures.riskFactors.length }}个</div>
                        <div class="feature-desc">需要关注的风险点</div>
                      </el-card>
                    </el-col>
                  </el-row>
                  
                  <!-- 风险因素详情 -->
                  <div v-if="currentReport.aiAnalysis.enterpriseFeatures.riskFactors.length > 0" class="risk-factors">
                    <h5>风险因素分析</h5>
                    <el-alert
                      v-for="(risk, index) in currentReport.aiAnalysis.enterpriseFeatures.riskFactors"
                      :key="index"
                      :title="risk"
                      type="warning"
                      :closable="false"
                      show-icon
                      style="margin-bottom: 10px;"
                    />
                  </div>
                  <div><span>根据企业当前资质信息，AI智能分析如下：

核心技术领域匹配

企业主营业务属于《国家重点支持的高新技术领域》，涵盖电子信息、先进制造、新材料等方向，符合高企认定的技术领域要求。

✅ 匹配
知识产权情况

企业已拥有发明专利2项、实用新型专利5项、软件著作权8项，知识产权数量与质量满足“通过自主研发获得核心知识产权”的要求。

✅ 匹配
研发费用占比

近一年研发费用占销售收入比例达5.2%（近三年平均4.8%），高于政策要求的“最近一年销售收入小于5000万元的企业，比例不低于5%”标准。

✅ 匹配
科技人员占比

企业科技人员总数占职工总数32%，高于政策规定的“不低于10%”要求。

✅ 匹配
高新技术产品（服务）收入

最近一年高新技术产品收入占企业总收入78%，超过政策要求的“不低于60%”标准。

✅ 匹配
成长性指标

企业净资产和销售收入近三年保持稳定增长，年均增长率超过10%，具备良好发展潜力。

✅ 基本匹配
综合结论与建议
🔹 匹配结论：企业当前在核心技术、知识产权、研发投入、人员结构、收入构成等方面均高度符合高新技术企业认定的核心条件，AI综合评估匹配度为 95%，具备较强的申报成功潜力。</span></div>
                </div>
                
                <!-- 政策匹配分析 -->
                <div class="policy-analysis">
                  <h4>政策匹配度分析</h4>
                  <div class="analysis-summary">
                    <div class="analysis-item">
                      <div class="analysis-label">综合政策得分：</div>
                      <div class="analysis-value">{{ currentReport.policyScore }}分</div>
                    </div>
                    <div class="analysis-item">
                      <div class="analysis-label">匹配政策数：</div>
                      <div class="analysis-value">{{ currentReport.matchedPoliciesCount }}个</div>
                    </div>
                    <div class="analysis-item">
                      <div class="analysis-label">总支持金额：</div>
                      <div class="analysis-value">{{ currentReport.totalSupportAmount }}万元</div>
                    </div>
                  </div>
                </div>
                
                <!-- 政策详情表格 -->
                <h4>推荐政策详情</h4>
                <el-table :data="currentReport.recommendedPolicies" stripe>
                  <el-table-column prop="name" label="政策名称" />
                  <el-table-column prop="categoryName" label="类别" width="100" />
                  <el-table-column prop="matchScore" label="匹配度" width="100">
                    <template #default="scope">
                      <el-tag :type="getScoreTagType(scope.row.matchScore)">
                        {{ scope.row.matchScore }}%
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="supportAmount" label="支持金额" width="120" />
                  <el-table-column prop="validPeriod" label="有效期" width="100" />
                  <el-table-column label="操作" width="120">
                    <template #default="scope">
                      <el-button size="small" @click="showPolicyDetail(scope.row)">查看详情</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="发展规划" name="planning">
              <div class="report-section">
                <h3>发展规划建议</h3>
                <div class="planning-suggestions">
                  <div v-for="(suggestion, index) in currentReport.suggestions" :key="index" class="suggestion-item">
                    <h4>{{ suggestion.title }}</h4>
                    <p>{{ suggestion.content }}</p>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="实施路径" name="implementation">
              <div class="report-section">
                <h3>实施路径规划</h3>
                <el-timeline>
                  <el-timeline-item
                    v-for="(step, index) in currentReport.implementationSteps"
                    :key="index"
                    :timestamp="step.time"
                    :type="step.type"
                  >
                    <h4>{{ step.title }}</h4>
                    <p>{{ step.description }}</p>
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
import { Plus, Search, OfficeBuilding, Document, TrendCharts, Clock, CircleCheck, Warning } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const detailVisible = ref(false)
const reportVisible = ref(false)
const policyDetailVisible = ref(false)
const enterpriseFormRef = ref()
const currentEnterprise = ref(null)
const currentReport = ref(null)
const currentPolicy = ref(null)
const activeTab = ref('basic')
const reportActiveTab = ref('overview')

// 搜索表单
const searchForm = reactive({
  enterpriseName: '',
  industry: '',
  status: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 企业信息表单
const enterpriseForm = reactive({
  id: null,
  enterpriseName: '',
  industry: '',
  scale: '',
  registeredCapital: 0,
  establishDate: '',
  address: '',
  description: '',
  mainBusiness: '',
  annualRevenue: 0,
  employeeCount: 0,
  techLevel: '',
  rdInvestment: 0,
  developmentPlan: '',
  policyNeeds: [],
  policyDescription: ''
})

// 表单验证规则
const rules = {
  enterpriseName: [
    { required: true, message: '请输入企业名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  industry: [
    { required: true, message: '请选择所属行业', trigger: 'change' }
  ],
  scale: [
    { required: true, message: '请选择企业规模', trigger: 'change' }
  ],
  address: [
    { required: true, message: '请输入企业地址', trigger: 'blur' }
  ],
  mainBusiness: [
    { required: true, message: '请输入主营业务', trigger: 'blur' }
  ],
  employeeCount: [
    { required: true, message: '请输入员工人数', trigger: 'blur' }
  ]
}

// 统计数据
const planningStats = reactive({
  totalEnterprises: 0,
  generatedReports: 0,
  pendingInfo: 0,
  averageMatchRate: 0
})

// 企业列表
const enterpriseList = ref([
  {
    id: 1,
    enterpriseName: '北京科技有限公司',
    industry: 'it',
    scale: 'medium',
    registeredCapital: 1000,
    establishDate: '2018-01-01',
    address: '北京市海淀区中关村',
    description: '专注于智能制造系统开发的高新技术企业',
    mainBusiness: '软件开发、系统集成',
    annualRevenue: 5000,
    employeeCount: 150,
    techLevel: 'high-tech',
    rdInvestment: 800,
    developmentPlan: '扩大研发团队，提升产品竞争力',
    infoStatus: 'complete',
    reportStatus: 'generated',
    createTime: '2024-01-15 10:00:00'
  },
  {
    id: 2,
    enterpriseName: '上海制造有限公司',
    industry: 'manufacturing',
    scale: 'large',
    registeredCapital: 5000,
    establishDate: '2010-05-01',
    address: '上海市浦东新区',
    description: '专业从事新能源汽车零部件制造',
    mainBusiness: '汽车零部件制造',
    annualRevenue: 20000,
    employeeCount: 500,
    techLevel: 'high-tech',
    rdInvestment: 2000,
    developmentPlan: '扩大产能，提升自动化水平',
    infoStatus: 'complete',
    reportStatus: 'generated',
    createTime: '2024-02-01 14:30:00'
  },
  {
    id: 3,
    enterpriseName: '深圳服务有限公司',
    industry: 'service',
    scale: 'small',
    registeredCapital: 500,
    establishDate: '2020-03-01',
    address: '深圳市南山区',
    description: '为企业提供数字化转型解决方案',
    mainBusiness: 'IT咨询服务',
    annualRevenue: 2000,
    employeeCount: 50,
    techLevel: 'tech-sme',
    rdInvestment: 300,
    developmentPlan: '拓展服务领域，提升服务质量',
    infoStatus: 'incomplete',
    reportStatus: 'not_generated',
    createTime: '2024-02-15 09:15:00'
  }
])

// 计算属性
const dialogTitle = computed(() => {
  return enterpriseForm.id ? '编辑企业信息' : '新建企业规划'
})

// 方法
const getIndustryLabel = (industry) => {
  const industryMap = {
    manufacturing: '制造业',
    service: '服务业',
    agriculture: '农业',
    construction: '建筑业',
    it: '信息技术',
    finance: '金融业'
  }
  return industryMap[industry] || '未知'
}

const getIndustryTagType = (industry) => {
  const typeMap = {
    manufacturing: 'primary',
    service: 'success',
    agriculture: 'warning',
    construction: 'info',
    it: 'danger',
    finance: 'danger'
  }
  return typeMap[industry] || ''
}

const getScaleLabel = (scale) => {
  const scaleMap = {
    large: '大型企业',
    medium: '中型企业',
    small: '小型企业',
    micro: '微型企业'
  }
  return scaleMap[scale] || '未知'
}

const getScaleTagType = (scale) => {
  const typeMap = {
    large: 'danger',
    medium: 'warning',
    small: 'success',
    micro: 'info'
  }
  return typeMap[scale] || ''
}

const getTechLevelLabel = (techLevel) => {
  const levelMap = {
    'high-tech': '高新技术企业',
    'tech-sme': '科技型中小企业',
    'general': '一般企业'
  }
  return levelMap[techLevel] || '未知'
}

const getInfoStatusLabel = (status) => {
  const statusMap = {
    complete: '信息完整',
    incomplete: '信息待完善'
  }
  return statusMap[status] || '未知'
}

const getInfoStatusTagType = (status) => {
  const statusMap = {
    complete: 'success',
    incomplete: 'warning'
  }
  return statusMap[status] || ''
}

const getReportStatusLabel = (status) => {
  const statusMap = {
    generated: '已生成',
    not_generated: '未生成'
  }
  return statusMap[status] || '未知'
}

const getReportStatusTagType = (status) => {
  const statusMap = {
    generated: 'success',
    not_generated: 'info'
  }
  return statusMap[status] || ''
}

const getScoreTagType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  return 'danger'
}

const showAddDialog = () => {
  enterpriseForm.id = null
  activeTab.value = 'basic'
  dialogVisible.value = true
}

const editEnterprise = (row) => {
  Object.assign(enterpriseForm, row)
  activeTab.value = 'basic'
  dialogVisible.value = true
}

const viewEnterprise = (row) => {
  currentEnterprise.value = row
  detailVisible.value = true
}

const deleteEnterprise = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除企业"${row.enterpriseName}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = enterpriseList.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      enterpriseList.value.splice(index, 1)
      updateStats()
      ElMessage.success('删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

const generateReport = async (row) => {
  if (row.infoStatus !== 'complete') {
    ElMessage.warning('请先完善企业信息')
    return
  }
  
  loading.value = true
  try {
    // 模拟AI分析过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // AI分析企业特征和政策匹配度
    const aiAnalysis = await performAIAnalysis(row)
    
    // 生成报告
    const generatedReport = {
      title: `${row.enterpriseName} - 企业规划报告`,
      generateTime: new Date().toLocaleString(),
      enterpriseName: row.enterpriseName,
      industry: getIndustryLabel(row.industry),
      scale: getScaleLabel(row.scale),
      registeredCapital: row.registeredCapital,
      establishDate: row.establishDate,
      employeeCount: row.employeeCount,
      policyScore: aiAnalysis.totalScore,
      matchedPoliciesCount: aiAnalysis.matchedPolicies.length,
      totalSupportAmount: aiAnalysis.totalSupportAmount,
      aiAnalysis: aiAnalysis,
      recommendedPolicies: aiAnalysis.matchedPolicies,
      suggestions: aiAnalysis.suggestions,
      implementationSteps: aiAnalysis.implementationSteps
    }
    
    // 更新企业状态并存储生成的报告数据
    const index = enterpriseList.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      enterpriseList.value[index].reportStatus = 'generated'
      enterpriseList.value[index].generatedReportData = generatedReport
    }
    
    currentReport.value = generatedReport
    
    updateStats()
    ElMessage.success('报告生成成功')
    reportVisible.value = true
  } catch (error) {
    ElMessage.error('生成报告失败')
  } finally {
    loading.value = false
  }
}

const showPolicyDetail = (policy) => {
  currentPolicy.value = policy
  policyDetailVisible.value = true
}

const viewReport = (row) => {
  if (row.reportStatus !== 'generated') {
    ElMessage.warning('请先生成报告')
    return
  }
  
  // 从存储的数据中获取报告
  if (row.generatedReportData) {
    currentReport.value = row.generatedReportData
  } else {
    // 如果没有存储的数据，重新生成报告
    ElMessage.warning('报告数据丢失，正在重新生成...')
    generateReport(row)
    return
  }
  
  reportVisible.value = true
}

const submitForm = async () => {
  if (!enterpriseFormRef.value) return
  
  try {
    await enterpriseFormRef.value.validate()
    submitting.value = true
    
    // 模拟提交操作
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 检查信息完整性
    const isComplete = checkInfoCompleteness(enterpriseForm)
    
    if (enterpriseForm.id) {
      // 编辑
      const index = enterpriseList.value.findIndex(item => item.id === enterpriseForm.id)
      if (index > -1) {
        enterpriseList.value[index] = { 
          ...enterpriseForm,
          infoStatus: isComplete ? 'complete' : 'incomplete',
          reportStatus: isComplete ? enterpriseList.value[index].reportStatus : 'not_generated'
        }
      }
      ElMessage.success('编辑成功')
    } else {
      // 新增
      const newEnterprise = {
        ...enterpriseForm,
        id: Date.now(),
        infoStatus: isComplete ? 'complete' : 'incomplete',
        reportStatus: 'not_generated',
        createTime: new Date().toLocaleString()
      }
      enterpriseList.value.unshift(newEnterprise)
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

const checkInfoCompleteness = (form) => {
  const requiredFields = [
    'enterpriseName', 'industry', 'scale', 'address', 
    'mainBusiness', 'employeeCount', 'description', 'developmentPlan'
  ]
  
  return requiredFields.every(field => {
    const value = form[field]
    if (Array.isArray(value)) {
      return value.length > 0
    }
    return value && value.toString().trim() !== ''
  })
}

const resetForm = () => {
  if (enterpriseFormRef.value) {
    enterpriseFormRef.value.resetFields()
  }
  Object.assign(enterpriseForm, {
    id: null,
    enterpriseName: '',
    industry: '',
    scale: '',
    registeredCapital: 0,
    establishDate: '',
    address: '',
    description: '',
    mainBusiness: '',
    annualRevenue: 0,
    employeeCount: 0,
    techLevel: '',
    rdInvestment: 0,
    developmentPlan: '',
    policyNeeds: [],
    policyDescription: ''
  })
}

const handleSearch = () => {
  pagination.currentPage = 1
  // 这里可以调用实际的搜索API
  console.log('搜索条件:', searchForm)
}

const resetSearch = () => {
  Object.assign(searchForm, {
    enterpriseName: '',
    industry: '',
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

// AI分析函数
const performAIAnalysis = async (enterprise) => {
  // 模拟AI分析过程
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // 企业特征分析
  const enterpriseFeatures = analyzeEnterpriseFeatures(enterprise)
  
  // 政策匹配分析
  const policyMatches = analyzePolicyMatches(enterprise, enterpriseFeatures)
  
  // 计算总分
  const totalScore = calculateTotalScore(policyMatches)
  
  // 生成建议
  const suggestions = generateSuggestions(enterprise, policyMatches)
  
  // 制定实施路径
  const implementationSteps = generateImplementationSteps(enterprise, policyMatches)
  
  return {
    enterpriseFeatures,
    policyMatches,
    totalScore,
    matchedPolicies: policyMatches,
    totalSupportAmount: calculateTotalSupportAmount(policyMatches),
    suggestions,
    implementationSteps
  }
}

// 分析企业特征
const analyzeEnterpriseFeatures = (enterprise) => {
  const features = {
    industryStrength: 0,
    scaleAdvantage: 0,
    techLevel: 0,
    financialHealth: 0,
    growthPotential: 0,
    riskFactors: []
  }
  
  // 行业优势分析
  const industryScores = {
    'it': 85,
    'manufacturing': 80,
    'service': 75,
    'agriculture': 70,
    'construction': 65,
    'finance': 90
  }
  features.industryStrength = industryScores[enterprise.industry] || 70
  
  // 规模优势分析
  const scaleScores = {
    'large': 90,
    'medium': 80,
    'small': 70,
    'micro': 60
  }
  features.scaleAdvantage = scaleScores[enterprise.scale] || 70
  
  // 技术等级分析
  const techScores = {
    'high-tech': 95,
    'tech-sme': 85,
    'general': 70
  }
  features.techLevel = techScores[enterprise.techLevel] || 70
  
  // 财务健康度分析
  const revenuePerEmployee = enterprise.annualRevenue / enterprise.employeeCount
  if (revenuePerEmployee > 100) {
    features.financialHealth = 90
  } else if (revenuePerEmployee > 50) {
    features.financialHealth = 80
  } else if (revenuePerEmployee > 20) {
    features.financialHealth = 70
  } else {
    features.financialHealth = 60
  }
  
  // 成长潜力分析
  const rdRatio = enterprise.rdInvestment / enterprise.annualRevenue
  if (rdRatio > 0.1) {
    features.growthPotential = 90
  } else if (rdRatio > 0.05) {
    features.growthPotential = 80
  } else if (rdRatio > 0.02) {
    features.growthPotential = 70
  } else {
    features.growthPotential = 60
  }
  
  // 风险因素识别
  if (enterprise.employeeCount < 50) {
    features.riskFactors.push('员工规模较小，可能影响政策申请')
  }
  if (enterprise.rdInvestment < 100) {
    features.riskFactors.push('研发投入较低，可能影响技术创新政策')
  }
  if (enterprise.registeredCapital < 1000) {
    features.riskFactors.push('注册资本较低，可能影响资金支持政策')
  }
  
  return features
}

// 分析政策匹配
const analyzePolicyMatches = (enterprise, features) => {
  const policies = [
    {
      name: '高新技术企业认定',
      category: 'tech',
      categoryName: '技术创新',
      baseScore: 85,
      conditions: ['high-tech', 'tech-sme'],
      supportAmount: '企业所得税减免15%',
      validPeriod: '3年',
      requirements: ['研发投入占比≥5%', '高新技术产品收入占比≥60%', '科技人员占比≥10%'],
      matchDetails: []
    },
    {
      name: '研发费用加计扣除',
      category: 'tax',
      categoryName: '税收优惠',
      baseScore: 80,
      conditions: ['all'],
      supportAmount: '研发费用加计扣除75%',
      validPeriod: '年度',
      requirements: ['有研发活动', '研发费用归集准确'],
      matchDetails: []
    },
    {
      name: '中小企业发展专项资金',
      category: 'financial',
      categoryName: '资金支持',
      baseScore: 75,
      conditions: ['small', 'micro', 'medium'],
      supportAmount: '最高500万元',
      validPeriod: '年度',
      requirements: ['符合中小企业标准', '有明确发展项目'],
      matchDetails: []
    },
    {
      name: '人才引进补贴',
      category: 'talent',
      categoryName: '人才引进',
      baseScore: 70,
      conditions: ['all'],
      supportAmount: '每人最高10万元',
      validPeriod: '3年',
      requirements: ['引进高层次人才', '有明确岗位需求'],
      matchDetails: []
    },
    {
      name: '用地支持政策',
      category: 'land',
      categoryName: '用地支持',
      baseScore: 65,
      conditions: ['large', 'medium'],
      supportAmount: '优先供地，价格优惠',
      validPeriod: '长期',
      requirements: ['有扩产需求', '符合产业规划'],
      matchDetails: []
    }
  ]
  
  return policies.map(policy => {
    let matchScore = policy.baseScore
    const matchDetails = []
    
    // 行业匹配度
    if (enterprise.industry === 'it' && policy.category === 'tech') {
      matchScore += 10
      matchDetails.push('✓ 信息技术行业，符合技术创新政策导向')
    }
    
    // 技术等级匹配
    if (policy.conditions.includes(enterprise.techLevel)) {
      matchScore += 15
      matchDetails.push(`✓ 技术等级${getTechLevelLabel(enterprise.techLevel)}，符合政策要求`)
    }
    
    // 规模匹配
    if (policy.conditions.includes(enterprise.scale) || policy.conditions.includes('all')) {
      matchScore += 10
      matchDetails.push(`✓ 企业规模${getScaleLabel(enterprise.scale)}，符合政策范围`)
    }
    
    // 研发投入匹配
    if (policy.category === 'tech' && enterprise.rdInvestment > 100) {
      matchScore += 8
      matchDetails.push('✓ 研发投入充足，有利于技术创新政策申请')
    }
    
    // 员工规模匹配
    if (enterprise.employeeCount > 100 && policy.category === 'talent') {
      matchScore += 5
      matchDetails.push('✓ 员工规模较大，人才需求明显')
    }
    
    // 财务健康度影响
    if (features.financialHealth > 80) {
      matchScore += 5
      matchDetails.push('✓ 财务状况良好，政策申请成功率较高')
    }
    
    // 成长潜力影响
    if (features.growthPotential > 80) {
      matchScore += 5
      matchDetails.push('✓ 成长潜力大，符合政策支持方向')
    }
    
    // 风险因素影响
    features.riskFactors.forEach(risk => {
      if (risk.includes('研发投入') && policy.category === 'tech') {
        matchScore -= 10
        matchDetails.push('⚠ 研发投入较低，可能影响技术创新政策申请')
      }
      if (risk.includes('员工规模') && policy.category === 'talent') {
        matchScore -= 5
        matchDetails.push('⚠ 员工规模较小，人才政策申请可能受限')
      }
    })
    
    // 确保分数在合理范围内
    matchScore = Math.max(0, Math.min(100, matchScore))
    
    return {
      ...policy,
      matchScore: Math.round(matchScore),
      matchDetails
    }
  }).filter(policy => policy.matchScore > 60) // 只返回匹配度大于60%的政策
}

// 计算总分
const calculateTotalScore = (policyMatches) => {
  if (policyMatches.length === 0) return 0
  
  const totalScore = policyMatches.reduce((sum, policy) => sum + policy.matchScore, 0)
  return Math.round(totalScore / policyMatches.length)
}

// 计算总支持金额
const calculateTotalSupportAmount = (policyMatches) => {
  let total = 0
  policyMatches.forEach(policy => {
    if (policy.supportAmount.includes('万元')) {
      const amount = parseInt(policy.supportAmount.match(/\d+/)[0])
      total += amount
    } else if (policy.supportAmount.includes('税收')) {
      total += 500 // 税收优惠估算价值
    } else if (policy.supportAmount.includes('人才')) {
      total += 100 // 人才补贴估算价值
    }
  })
  return total.toString()
}

// 生成建议
const generateSuggestions = (enterprise, policyMatches) => {
  const suggestions = []
  
  // 基于政策匹配生成建议
  const techPolicies = policyMatches.filter(p => p.category === 'tech')
  if (techPolicies.length > 0) {
    suggestions.push({
      title: '技术创新建议',
      content: `基于您的企业特征，建议优先申请${techPolicies[0].name}等技术创新政策。您的技术等级为${getTechLevelLabel(enterprise.techLevel)}，研发投入${enterprise.rdInvestment}万元，符合技术创新政策的基本要求。`,
      priority: 'high'
    })
  }
  
  const financialPolicies = policyMatches.filter(p => p.category === 'financial')
  if (financialPolicies.length > 0) {
    suggestions.push({
      title: '资金支持建议',
      content: `作为${getScaleLabel(enterprise.scale)}，您可以申请${financialPolicies[0].name}等资金支持政策。建议准备详细的项目计划书和财务资料，提高申请成功率。`,
      priority: 'medium'
    })
  }
  
  const talentPolicies = policyMatches.filter(p => p.category === 'talent')
  if (talentPolicies.length > 0) {
    suggestions.push({
      title: '人才引进建议',
      content: `您的企业有${enterprise.employeeCount}名员工，建议制定人才引进计划，申请人才引进补贴政策。重点关注技术研发和经营管理人才的引进。`,
      priority: 'medium'
    })
  }
  
  return suggestions
}

// 生成实施路径
const generateImplementationSteps = (enterprise, policyMatches) => {
  const steps = []
  let month = 1
  
  // 按优先级排序政策
  const sortedPolicies = policyMatches.sort((a, b) => b.matchScore - a.matchScore)
  
  sortedPolicies.forEach((policy, index) => {
    steps.push({
      title: `申请${policy.name}`,
      description: `准备${policy.requirements.join('、')}等材料，预计申请周期${policy.validPeriod}。`,
      time: `第${month}-${month + 2}个月`,
      type: index === 0 ? 'primary' : 'success',
      policy: policy
    })
    month += 3
  })
  
  return steps
}

const updateStats = () => {
  planningStats.totalEnterprises = enterpriseList.value.length
  planningStats.generatedReports = enterpriseList.value.filter(item => item.reportStatus === 'generated').length
  planningStats.pendingInfo = enterpriseList.value.filter(item => item.infoStatus === 'incomplete').length
  planningStats.averageMatchRate = Math.floor(Math.random() * 30) + 70 // 模拟数据
}

// 生命周期
onMounted(() => {
  updateStats()
  pagination.total = enterpriseList.value.length
})
</script>

<style scoped>
.enterprise-planning-container {
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

.enterprise-list {
  margin-top: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.enterprise-detail {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}

.planning-report {
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

.policy-analysis {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.analysis-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.analysis-label {
  font-weight: bold;
  color: #606266;
}

.analysis-value {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

.planning-suggestions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.suggestion-item {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
}

.suggestion-item h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.suggestion-item p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
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

/* AI分析相关样式 */
.ai-analysis-section {
  margin-bottom: 30px;
}

.feature-cards {
  margin-bottom: 20px;
}

.feature-card {
  height: 120px;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: #606266;
  font-size: 14px;
}

.feature-score {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.feature-desc {
  font-size: 12px;
  color: #909399;
}

.risk-factors {
  margin-top: 20px;
}

.risk-factors h5 {
  margin-bottom: 15px;
  color: #e6a23c;
}

.analysis-summary {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.policy-detail {
  padding: 20px 0;
}

.match-details {
  margin-top: 30px;
}

.match-details h4 {
  margin-bottom: 20px;
  color: #303133;
  border-left: 4px solid #409eff;
  padding-left: 15px;
}

.match-detail-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.match-detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 6px;
  background: #f8f9fa;
}

.match-detail-item.positive {
  background: #f0f9ff;
  border-left: 4px solid #67c23a;
}

.match-detail-item.warning {
  background: #fef7e0;
  border-left: 4px solid #e6a23c;
}

.detail-icon {
  font-size: 16px;
}

.detail-icon.success {
  color: #67c23a;
}

.detail-icon.warning {
  color: #e6a23c;
}
</style> 