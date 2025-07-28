<template>
    <div class="rd-expense-container">
      <el-card>
        <div class="header">
          <span>研发费用管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="createExpense" size="small">申请费用</el-button>
            <el-button type="success" @click="refreshExpenses" size="small">刷新</el-button>
            <el-button type="info" @click="showStatistics" size="small">费用统计</el-button>
          </div>
        </div>
        
        <!-- 费用类型Tab -->
        <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick" class="expense-tabs">
          <el-tab-pane label="材料燃料动力费" name="material">
            <div class="tab-content">
              <div class="tab-description">
                <h4>研发活动直接消耗的材料、燃料和动力费用</h4>
                <p>包括研发过程中消耗的原材料、辅助材料、燃料、动力等费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="人工费用" name="personnel">
            <div class="tab-content">
              <div class="tab-description">
                <h4>企业在职研发人员的工资、奖金、津贴、补贴、社会保险费、住房公积金等人工费用以及外聘研发人员的劳务费用</h4>
                <p>包括研发人员的各项薪酬福利和外聘人员费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="固定资产费用" name="depreciation">
            <div class="tab-content">
              <div class="tab-description">
                <h4>用于研发活动的仪器、设备、房屋等固定资产的折旧费或租赁费以及相关固定资产的运行维护、维修等费用</h4>
                <p>包括研发用固定资产的折旧、租赁、维护等费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="无形资产费用" name="intangible">
            <div class="tab-content">
              <div class="tab-description">
                <h4>用于研发活动的软件、专利权、非专利技术等无形资产的摊销费用</h4>
                <p>包括研发用软件、专利、技术等无形资产的摊销费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="试验费用" name="testing">
            <div class="tab-content">
              <div class="tab-description">
                <h4>用于中间试验和产品试制的模具、工艺装备开发及制造费,设备调整及检验费,样品、样机及一般测试手段购置费,试制产品的检验费等</h4>
                <p>包括试制、检验、测试等相关费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="研发成果费用" name="intellectual">
            <div class="tab-content">
              <div class="tab-description">
                <h4>研发成果的论证、评审、验收、评估以及知识产权的申请费、注册费、代理费等费用</h4>
                <p>包括成果评估、知识产权申请等相关费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="外包合作费用" name="outsourcing">
            <div class="tab-content">
              <div class="tab-description">
                <h4>通过外包、合作研发等方式,委托其他单位、个人或者与之合作进行研发而支付的费用</h4>
                <p>包括外包研发、合作开发等相关费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="其他相关费用" name="other">
            <div class="tab-content">
              <div class="tab-description">
                <h4>与研发活动直接相关的其他费用，包括技术图书资料费、资料翻译费、会议费、差旅费、办公费、外事费、研发人员培训费、培养费、专家咨询费、高新科技研发保险费用等</h4>
                <p>包括研发相关的其他各项费用</p>
              </div>
              <el-table :data="filteredExpenses" style="width: 100%;" fit="true">
                <el-table-column prop="projectName" label="项目名称" min-width="150">
                  <template #default="scope">
                    <span class="clickable-title" @click="viewExpenseDetail(scope.row)">{{ scope.row.projectName }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="金额" min-width="120">
                  <template #default="scope">
                    <span class="amount">¥{{ scope.row.amount.toLocaleString() }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.status === 'pending'" type="warning">待审批</el-tag>
                    <el-tag v-else-if="scope.row.status === 'approved'" type="success">已通过</el-tag>
                    <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
                    <el-tag v-else-if="scope.row.status === 'paid'" type="primary">已支付</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="applicant" label="申请人" min-width="120"/>
                <el-table-column prop="department" label="部门" min-width="120"/>
                <el-table-column prop="applyTime" label="申请时间" min-width="150"/>
                <el-table-column prop="approver" label="审批人" min-width="120"/>
                <el-table-column label="操作" min-width="200" fixed="right">
                  <template #default="scope">
                    <el-button size="small" type="primary" @click="viewExpenseDetail(scope.row)">查看</el-button>
                    <el-button v-if="scope.row.status === 'pending'" size="small" type="success" @click="approveExpense(scope.row)">审批</el-button>
                    <el-button v-if="scope.row.status === 'approved'" size="small" type="warning" @click="payExpense(scope.row)">支付</el-button>
                    <el-button size="small" type="danger" @click="deleteExpense(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
  
      <!-- 费用详情弹窗 -->
      <el-dialog v-model="expenseDetailVisible" title="费用详情" width="900px" :before-close="handleClose">
        <div class="expense-detail" v-if="currentExpense">
          <!-- 基本信息 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>费用信息</span>
                <el-button type="primary" size="small" @click="editExpense(currentExpense)">编辑</el-button>
              </div>
            </template>
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>项目名称：</label>
                  <span>{{ currentExpense.projectName }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>费用类型：</label>
                  <el-tag :type="getTagType(currentExpense.type)">{{ getTypeLabel(currentExpense.type) }}</el-tag>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>申请金额：</label>
                  <span class="amount">¥{{ currentExpense.amount.toLocaleString() }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>状态：</label>
                  <el-tag v-if="currentExpense.status === 'pending'" type="warning">待审批</el-tag>
                  <el-tag v-else-if="currentExpense.status === 'approved'" type="success">已通过</el-tag>
                  <el-tag v-else-if="currentExpense.status === 'rejected'" type="danger">已拒绝</el-tag>
                  <el-tag v-else-if="currentExpense.status === 'paid'" type="primary">已支付</el-tag>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="detail-item">
                  <label>申请人：</label>
                  <span>{{ currentExpense.applicant }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="detail-item">
                  <label>申请时间：</label>
                  <span>{{ currentExpense.applyTime }}</span>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="24">
                <div class="detail-item">
                  <label>费用说明：</label>
                  <div class="content-text">{{ currentExpense.description }}</div>
                </div>
              </el-col>
            </el-row>
          </el-card>
  
          <!-- 审批记录 -->
          <el-card class="approval-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>审批记录</span>
              </div>
            </template>
            
            <el-timeline>
              <el-timeline-item
                v-for="(record, index) in approvalRecords"
                :key="index"
                :timestamp="record.time"
                :type="record.type === 'approve' ? 'success' : record.type === 'reject' ? 'danger' : 'primary'"
              >
                <div class="timeline-content">
                  <div class="timeline-title">{{ record.action }}</div>
                  <div class="timeline-user">{{ record.user }} ({{ record.department }})</div>
                  <div v-if="record.comment" class="timeline-comment">{{ record.comment }}</div>
                </div>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </div>
      </el-dialog>
  
      <!-- 申请/编辑费用弹窗 -->
      <el-dialog v-model="expenseFormVisible" :title="expenseFormTitle" width="800px" :before-close="handleFormClose">
        <el-form :model="expenseForm" :rules="expenseRules" ref="expenseFormRef" label-width="120px">
          <el-form-item label="项目名称" prop="projectName">
            <el-input v-model="expenseForm.projectName" placeholder="请输入项目名称"/>
          </el-form-item>
          <el-form-item label="费用类型" prop="type">
            <el-select v-model="expenseForm.type" placeholder="请选择费用类型" style="width: 100%">
              <el-option label="材料燃料动力费" value="material"/>
              <el-option label="人工费用" value="personnel"/>
              <el-option label="固定资产费用" value="depreciation"/>
              <el-option label="无形资产费用" value="intangible"/>
              <el-option label="试验费用" value="testing"/>
              <el-option label="研发成果费用" value="intellectual"/>
              <el-option label="外包合作费用" value="outsourcing"/>
              <el-option label="其他相关费用" value="other"/>
            </el-select>
          </el-form-item>
          <el-form-item label="申请金额" prop="amount">
            <el-input-number 
              v-model="expenseForm.amount" 
              :min="0" 
              :precision="2" 
              :step="100"
              style="width: 100%"
              placeholder="请输入金额"
            />
          </el-form-item>
          <el-form-item label="费用说明" prop="description">
            <el-input
              v-model="expenseForm.description"
              type="textarea"
              :rows="4"
              placeholder="请详细说明费用用途和必要性"
            />
          </el-form-item>
          <el-form-item label="附件">
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleFileChange"
              :file-list="fileList"
              multiple
            >
              <el-button type="primary">选择文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  支持jpg/png/pdf/doc/docx文件，且不超过10MB
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="expenseFormVisible = false">取消</el-button>
            <el-button type="primary" @click="submitExpenseForm">提交申请</el-button>
          </div>
        </template>
      </el-dialog>
  
      <!-- 审批弹窗 -->
      <el-dialog v-model="approvalVisible" title="费用审批" width="600px" :before-close="handleApprovalClose">
        <el-form :model="approvalForm" :rules="approvalRules" ref="approvalFormRef" label-width="100px">
          <el-form-item label="审批结果" prop="result">
            <el-radio-group v-model="approvalForm.result">
              <el-radio label="approve">通过</el-radio>
              <el-radio label="reject">拒绝</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="审批意见" prop="comment">
            <el-input
              v-model="approvalForm.comment"
              type="textarea"
              :rows="4"
              placeholder="请输入审批意见"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="approvalVisible = false">取消</el-button>
            <el-button type="primary" @click="submitApproval">确认审批</el-button>
          </div>
        </template>
      </el-dialog>
  
      <!-- 费用统计弹窗 -->
      <el-dialog v-model="statisticsVisible" title="费用统计" width="1000px" :before-close="handleStatisticsClose">
        <div class="statistics-content">
          <!-- 统计卡片 -->
          <el-row :gutter="20" style="margin-bottom: 30px;">
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-number">¥{{ totalAmount.toLocaleString() }}</div>
                <div class="stat-label">总费用</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-number">{{ pendingCount }}</div>
                <div class="stat-label">待审批</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-number">{{ approvedCount }}</div>
                <div class="stat-label">已通过</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-number">{{ paidCount }}</div>
                <div class="stat-label">已支付</div>
              </el-card>
            </el-col>
          </el-row>
  
          <!-- 费用类型统计 -->
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>费用类型分布</template>
                <div id="typeChart" style="height: 300px;"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>月度费用趋势</template>
                <div id="trendChart" style="height: 300px;"></div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { Search } from '@element-plus/icons-vue'
  
  // 响应式数据
  const activeTab = ref('material')
  const expenses = ref([])
  const expenseDetailVisible = ref(false)
  const currentExpense = ref(null)
  const expenseFormVisible = ref(false)
  const expenseFormTitle = ref('申请费用')
  const expenseFormRef = ref(null)
  const approvalVisible = ref(false)
  const approvalFormRef = ref(null)
  const statisticsVisible = ref(false)
  const fileList = ref([])
  
  // 模拟费用数据 - 按八大类分类
  const mockExpenses = [
    // 材料燃料动力费
    {
      id: 'exp001',
      projectName: 'AI算法优化项目',
      type: 'material',
      amount: 25000,
      status: 'pending',
      applicant: '张工程师',
      department: '技术部',
      applyTime: '2024-01-15 09:00:00',
      approver: '',
      description: '购买高性能GPU服务器用于AI模型训练，包括材料、燃料和动力费用。'
    },
    {
      id: 'exp002',
      projectName: '新材料研发项目',
      type: 'material',
      amount: 18000,
      status: 'approved',
      applicant: '李研究员',
      department: '研发部',
      applyTime: '2024-01-14 14:30:00',
      approver: '王经理',
      description: '研发新材料的原材料采购费用。'
    },
    
    // 人工费用
    {
      id: 'exp003',
      projectName: '移动端开发项目',
      type: 'personnel',
      amount: 150000,
      status: 'approved',
      applicant: '李开发',
      department: '技术部',
      applyTime: '2024-01-14 14:30:00',
      approver: '王经理',
      description: '研发人员工资、奖金、津贴、补贴、社会保险费、住房公积金等人工费用。'
    },
    {
      id: 'exp004',
      projectName: '外聘专家咨询',
      type: 'personnel',
      amount: 50000,
      status: 'paid',
      applicant: '陈主管',
      department: '人事部',
      applyTime: '2024-01-13 11:20:00',
      approver: '刘总监',
      description: '外聘研发专家的劳务费用。'
    },
    
    // 固定资产费用
    {
      id: 'exp005',
      projectName: '产品设计项目',
      type: 'depreciation',
      amount: 80000,
      status: 'paid',
      applicant: '陈设计师',
      department: '设计部',
      applyTime: '2024-01-13 11:20:00',
      approver: '刘总监',
      description: '用于研发活动的仪器、设备、房屋等固定资产的折旧费。'
    },
    {
      id: 'exp006',
      projectName: '实验室设备租赁',
      type: 'depreciation',
      amount: 30000,
      status: 'approved',
      applicant: '赵研究员',
      department: '研发部',
      applyTime: '2024-01-12 16:45:00',
      approver: '孙经理',
      description: '实验室设备租赁费用。'
    },
    
    // 无形资产费用
    {
      id: 'exp007',
      projectName: '软件系统开发',
      type: 'intangible',
      amount: 45000,
      status: 'approved',
      applicant: '赵研究员',
      department: '研发部',
      applyTime: '2024-01-12 16:45:00',
      approver: '孙经理',
      description: '用于研发活动的软件、专利权、非专利技术等无形资产的摊销费用。'
    },
    {
      id: 'exp008',
      projectName: '专利技术购买',
      type: 'intangible',
      amount: 120000,
      status: 'pending',
      applicant: '钱工程师',
      department: '研发部',
      applyTime: '2024-01-11 10:30:00',
      approver: '',
      description: '购买相关专利技术的摊销费用。'
    },
    
    // 试验费用
    {
      id: 'exp009',
      projectName: '新产品试制',
      type: 'testing',
      amount: 35000,
      status: 'pending',
      applicant: '钱工程师',
      department: '研发部',
      applyTime: '2024-01-11 10:30:00',
      approver: '',
      description: '用于中间试验和产品试制的模具、工艺装备开发及制造费，设备调整及检验费。'
    },
    {
      id: 'exp010',
      projectName: '样品制作检验',
      type: 'testing',
      amount: 15000,
      status: 'approved',
      applicant: '孙工程师',
      department: '研发部',
      applyTime: '2024-01-10 15:20:00',
      approver: '李总监',
      description: '样品、样机及一般测试手段购置费，试制产品的检验费等。'
    },
    
    // 研发成果费用
    {
      id: 'exp011',
      projectName: '专利申请项目',
      type: 'intellectual',
      amount: 12000,
      status: 'paid',
      applicant: '孙律师',
      department: '法务部',
      applyTime: '2024-01-10 15:20:00',
      approver: '李总监',
      description: '研发成果的论证、评审、验收、评估以及知识产权的申请费、注册费、代理费等费用。'
    },
    {
      id: 'exp012',
      projectName: '技术成果评估',
      type: 'intellectual',
      amount: 8000,
      status: 'approved',
      applicant: '周工程师',
      department: '技术部',
      applyTime: '2024-01-09 09:15:00',
      approver: '王总监',
      description: '技术成果的评估和认证费用。'
    },
    
    // 外包合作费用
    {
      id: 'exp013',
      projectName: '技术合作开发',
      type: 'outsourcing',
      amount: 200000,
      status: 'approved',
      applicant: '周经理',
      department: '技术部',
      applyTime: '2024-01-09 09:15:00',
      approver: '王总监',
      description: '通过外包、合作研发等方式，委托其他单位、个人或者与之合作进行研发而支付的费用。'
    },
    {
      id: 'exp014',
      projectName: '第三方研发服务',
      type: 'outsourcing',
      amount: 80000,
      status: 'pending',
      applicant: '吴主管',
      department: '人事部',
      applyTime: '2024-01-08 14:00:00',
      approver: '',
      description: '委托第三方机构进行专项研发服务。'
    },
    
    // 其他相关费用
    {
      id: 'exp015',
      projectName: '技术培训会议',
      type: 'other',
      amount: 8000,
      status: 'rejected',
      applicant: '吴主管',
      department: '人事部',
      applyTime: '2024-01-08 14:00:00',
      approver: '陈经理',
      description: '与研发活动直接相关的其他费用，包括技术图书资料费、会议费、差旅费、研发人员培训费等。'
    },
    {
      id: 'exp016',
      projectName: '技术资料翻译',
      type: 'other',
      amount: 5000,
      status: 'approved',
      applicant: '郑翻译',
      department: '技术部',
      applyTime: '2024-01-07 16:30:00',
      approver: '张经理',
      description: '技术资料翻译费用。'
    }
  ]
  
  // 模拟审批记录
  const approvalRecords = ref([
    {
      action: '提交申请',
      user: '张工程师',
      department: '技术部',
      time: '2024-01-15 09:00:00',
      type: 'submit'
    }
  ])
  
  // 费用表单数据
  const expenseForm = ref({
    projectName: '',
    type: '',
    amount: 0,
    description: ''
  })
  
  // 审批表单数据
  const approvalForm = ref({
    result: 'approve',
    comment: ''
  })
  
  // 表单验证规则
  const expenseRules = {
    projectName: [
      { required: true, message: '请输入项目名称', trigger: 'blur' }
    ],
    type: [
      { required: true, message: '请选择费用类型', trigger: 'change' }
    ],
    amount: [
      { required: true, message: '请输入申请金额', trigger: 'blur' }
    ],
    description: [
      { required: true, message: '请输入费用说明', trigger: 'blur' }
    ]
  }
  
  const approvalRules = {
    result: [
      { required: true, message: '请选择审批结果', trigger: 'change' }
    ],
    comment: [
      { required: true, message: '请输入审批意见', trigger: 'blur' }
    ]
  }
  
  // 计算属性
  const filteredExpenses = computed(() => {
    return expenses.value.filter(exp => exp.type === activeTab.value)
  })
  
  const totalAmount = computed(() => {
    return expenses.value.reduce((sum, exp) => sum + exp.amount, 0)
  })
  
  const pendingCount = computed(() => {
    return expenses.value.filter(exp => exp.status === 'pending').length
  })
  
  const approvedCount = computed(() => {
    return expenses.value.filter(exp => exp.status === 'approved').length
  })
  
  const paidCount = computed(() => {
    return expenses.value.filter(exp => exp.status === 'paid').length
  })
  
  // 方法
  const handleTabClick = (tab) => {
    console.log('切换到tab:', tab.props.name)
  }
  
  const getTypeLabel = (type) => {
    const typeMap = {
      'material': '材料燃料动力费',
      'personnel': '人工费用',
      'depreciation': '固定资产费用',
      'intangible': '无形资产费用',
      'testing': '试验费用',
      'intellectual': '研发成果费用',
      'outsourcing': '外包合作费用',
      'other': '其他相关费用'
    }
    return typeMap[type] || '未知类型'
  }
  

  
  const getTagType = (type) => {
    const typeMap = {
      'material': 'primary',
      'personnel': 'success',
      'depreciation': 'warning',
      'intangible': 'info',
      'testing': 'danger',
      'intellectual': 'default',
      'outsourcing': 'primary',
      'other': 'default'
    }
    return typeMap[type] || 'default'
  }
  
  const fetchExpenses = async () => {
    try {
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500))
      expenses.value = mockExpenses
      ElMessage.success('费用列表加载成功')
    } catch (e) {
      ElMessage.error('获取费用列表失败')
    }
  }
  
  const refreshExpenses = () => {
    fetchExpenses()
  }
  
  const createExpense = () => {
    expenseFormTitle.value = '申请费用'
    expenseForm.value = {
      projectName: '',
      type: activeTab.value,
      amount: 0,
      description: ''
    }
    fileList.value = []
    expenseFormVisible.value = true
  }
  
  const editExpense = (expense) => {
    expenseFormTitle.value = '编辑费用'
    expenseForm.value = { ...expense }
    expenseFormVisible.value = true
  }
  
  const submitExpenseForm = async () => {
    try {
      await expenseFormRef.value.validate()
      // 模拟提交
      await new Promise(resolve => setTimeout(resolve, 1000))
      ElMessage.success(expenseFormTitle.value === '申请费用' ? '费用申请提交成功' : '费用信息更新成功')
      expenseFormVisible.value = false
      fetchExpenses()
    } catch (error) {
      ElMessage.error('表单验证失败')
    }
  }
  
  const deleteExpense = async (expense) => {
    try {
      await ElMessageBox.confirm(
        `确定要删除费用申请"${expense.projectName}"吗？`,
        '确认删除',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
      
      // 模拟删除操作
      expenses.value = expenses.value.filter(e => e.id !== expense.id)
      ElMessage.success('删除成功')
    } catch {
      ElMessage.info('已取消删除')
    }
  }
  
  const viewExpenseDetail = (expense) => {
    currentExpense.value = expense
    expenseDetailVisible.value = true
    loadApprovalRecords(expense.id)
  }
  
  const approveExpense = (expense) => {
    currentExpense.value = expense
    approvalForm.value = {
      result: 'approve',
      comment: ''
    }
    approvalVisible.value = true
  }
  
  const submitApproval = async () => {
    try {
      await approvalFormRef.value.validate()
      // 模拟审批
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // 更新费用状态
      const expense = expenses.value.find(e => e.id === currentExpense.value.id)
      if (expense) {
        expense.status = approvalForm.value.result === 'approve' ? 'approved' : 'rejected'
        expense.approver = '当前用户'
      }
      
      ElMessage.success('审批完成')
      approvalVisible.value = false
      fetchExpenses()
    } catch (error) {
      ElMessage.error('表单验证失败')
    }
  }
  
  const payExpense = async (expense) => {
    try {
      await ElMessageBox.confirm(
        `确定要支付费用"${expense.projectName}"吗？`,
        '确认支付',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
      
      // 模拟支付操作
      expense.status = 'paid'
      ElMessage.success('支付成功')
    } catch {
      ElMessage.info('已取消支付')
    }
  }
  
  const showStatistics = () => {
    statisticsVisible.value = true
    // 这里可以加载图表数据
  }
  
  const loadApprovalRecords = (expenseId) => {
    // 模拟加载审批记录
    approvalRecords.value = [
      {
        action: '提交申请',
        user: '张工程师',
        department: '技术部',
        time: '2024-01-15 09:00:00',
        type: 'submit'
      }
    ]
  }
  
  const handleFileChange = (file, fileList) => {
    console.log('文件变化:', file, fileList)
  }
  
  const handleClose = () => {
    expenseDetailVisible.value = false
    currentExpense.value = null
    approvalRecords.value = []
  }
  
  const handleFormClose = () => {
    expenseFormVisible.value = false
    expenseFormRef.value?.resetFields()
    fileList.value = []
  }
  
  const handleApprovalClose = () => {
    approvalVisible.value = false
    approvalFormRef.value?.resetFields()
  }
  
  const handleStatisticsClose = () => {
    statisticsVisible.value = false
  }
  
  onMounted(fetchExpenses)
  </script>
  
  <style scoped>
  .rd-expense-container {
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
  
  .expense-tabs {
    margin-top: 20px;
  }
  
  .tab-content {
    padding: 20px 0;
  }
  
  .tab-description {
    background: #f5f7fa;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 4px solid #409eff;
  }
  
  .tab-description h4 {
    margin: 0 0 10px 0;
    color: #303133;
    font-size: 16px;
  }
  
  .tab-description p {
    margin: 0;
    color: #606266;
    font-size: 14px;
  }
  
  .clickable-title {
    color: #409eff;
    cursor: pointer;
  }
  
  .clickable-title:hover {
    text-decoration: underline;
  }
  
  .amount {
    color: #e6a23c;
    font-weight: bold;
  }
  
  .expense-detail {
    padding: 20px;
  }
  
  .info-card,
  .approval-card {
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
  
  .timeline-content {
    padding: 10px 0;
  }
  
  .timeline-title {
    font-weight: bold;
    color: #303133;
    margin-bottom: 5px;
  }
  
  .timeline-user {
    color: #606266;
    font-size: 14px;
    margin-bottom: 5px;
  }
  
  .timeline-comment {
    color: #909399;
    font-size: 14px;
    background: #f5f7fa;
    padding: 8px;
    border-radius: 4px;
  }
  
  .statistics-content {
    padding: 20px;
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
  
  /* 响应式调整 */
  @media (max-width: 768px) {
    .rd-expense-container {
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