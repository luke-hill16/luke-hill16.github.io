<template>
  <div class="enterprise-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>企业管理</span>
          <el-button type="primary" @click="handleAddEnterprise">新增企业</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="企业名称">
            <el-input v-model="searchForm.name" placeholder="请输入企业名称" clearable />
          </el-form-item>
          <el-form-item label="统一社会信用代码">
            <el-input v-model="searchForm.creditCode" placeholder="请输入统一社会信用代码" clearable />
          </el-form-item>
          <el-form-item label="企业类型">
            <el-select v-model="searchForm.type" placeholder="请选择企业类型" clearable style="width: 180px;">
              <el-option label="有限责任公司" value="limited" />
              <el-option label="股份有限公司" value="joint" />
              <el-option label="个人独资企业" value="individual" />
              <el-option label="合伙企业" value="partnership" />
              <el-option label="国有企业" value="state" />
              <el-option label="外资企业" value="foreign" />
            </el-select>
          </el-form-item>
          <el-form-item label="行业">
            <el-select v-model="searchForm.industry" placeholder="请选择行业" clearable style="width: 180px;">
              <el-option label="制造业" value="manufacturing" />
              <el-option label="信息技术" value="it" />
              <el-option label="金融业" value="finance" />
              <el-option label="房地产业" value="realestate" />
              <el-option label="教育" value="education" />
              <el-option label="医疗健康" value="healthcare" />
              <el-option label="零售业" value="retail" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="注册资本">
            <el-select v-model="searchForm.capitalRange" placeholder="请选择注册资本" clearable style="width: 180px;">
              <el-option label="100万以下" value="under100" />
              <el-option label="100-500万" value="100-500" />
              <el-option label="500-1000万" value="500-1000" />
              <el-option label="1000-5000万" value="1000-5000" />
              <el-option label="5000万以上" value="over5000" />
            </el-select>
          </el-form-item>
          <el-form-item label="经营状态">
            <el-select v-model="searchForm.status" placeholder="请选择经营状态" clearable style="width: 180px;">
              <el-option label="在业" value="active" />
              <el-option label="存续" value="existing" />
              <el-option label="吊销" value="revoked" />
              <el-option label="注销" value="cancelled" />
              <el-option label="迁出" value="moved" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 企业列表 -->
      <div class="enterprise-list">
        <div 
          v-for="enterprise in enterpriseList" 
          :key="enterprise.id" 
          class="enterprise-item"
          @click="handleViewEnterprise(enterprise)"
        >
          <div class="enterprise-header">
            <div class="enterprise-name">
              <span class="name" @click.stop="handleViewEnterpriseDetail(enterprise)">{{ enterprise.name }}</span>
              <el-tag :type="getStatusTagType(enterprise.status)" size="small">
                {{ getStatusLabel(enterprise.status) }}
              </el-tag>
            </div>
            <div class="enterprise-actions">
              <el-button size="small" @click.stop="handleEditEnterprise(enterprise)">编辑</el-button>
              <el-button size="small" type="danger" @click.stop="handleDeleteEnterprise(enterprise)">删除</el-button>
            </div>
          </div>
          
          <div class="enterprise-info">
            <div class="info-row">
              <div class="info-item">
                <span class="label">统一社会信用代码：</span>
                <span class="value">{{ enterprise.creditCode }}</span>
              </div>
              <div class="info-item">
                <span class="label">法定代表人：</span>
                <span class="value">{{ enterprise.legalRepresentative }}</span>
              </div>
            </div>
            
            <div class="info-row">
              <div class="info-item">
                <span class="label">企业类型：</span>
                <span class="value">{{ getTypeLabel(enterprise.type) }}</span>
              </div>
              <div class="info-item">
                <span class="label">注册资本：</span>
                <span class="value">{{ formatCapital(enterprise.registeredCapital) }}</span>
              </div>
            </div>
            
            <div class="info-row">
              <div class="info-item">
                <span class="label">成立日期：</span>
                <span class="value">{{ enterprise.establishDate }}</span>
              </div>
              <div class="info-item">
                <span class="label">行业：</span>
                <span class="value">{{ getIndustryLabel(enterprise.industry) }}</span>
              </div>
            </div>
            
            <div class="info-row">
              <div class="info-item full-width">
                <span class="label">注册地址：</span>
                <span class="value">{{ enterprise.address }}</span>
              </div>
            </div>
            
            <div class="info-row">
              <div class="info-item">
                <span class="label">联系电话：</span>
                <span class="value">{{ enterprise.phone }}</span>
              </div>
              <div class="info-item">
                <span class="label">邮箱：</span>
                <span class="value">{{ enterprise.email }}</span>
              </div>
            </div>
          </div>
          
          <div class="enterprise-footer">
            <div class="footer-item">
              <span class="label">经营范围：</span>
              <span class="value">{{ enterprise.businessScope }}</span>
            </div>
          </div>
        </div>
      </div>

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

    <!-- 企业详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="企业详情" width="1000px" class="enterprise-detail-dialog">
      <div class="enterprise-detail">
        <!-- 企业基本信息 -->
        <div class="detail-section">
          <h3 class="section-title">基本信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">企业名称：</span>
                <span class="value">{{ currentEnterprise.name }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">统一社会信用代码：</span>
                <span class="value">{{ currentEnterprise.creditCode }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">企业类型：</span>
                <span class="value">{{ getTypeLabel(currentEnterprise.type) }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">行业：</span>
                <span class="value">{{ getIndustryLabel(currentEnterprise.industry) }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">注册资本：</span>
                <span class="value">{{ formatCapital(currentEnterprise.registeredCapital) }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">成立日期：</span>
                <span class="value">{{ currentEnterprise.establishDate }}</span>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">法定代表人：</span>
                <span class="value">{{ currentEnterprise.legalRepresentative }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">经营状态：</span>
                <el-tag :type="getStatusTagType(currentEnterprise.status)">
                  {{ getStatusLabel(currentEnterprise.status) }}
                </el-tag>
              </div>
            </el-col>
          </el-row>
          <div class="detail-item">
            <span class="label">注册地址：</span>
            <span class="value">{{ currentEnterprise.address }}</span>
          </div>
          <div class="detail-item">
            <span class="label">经营范围：</span>
            <span class="value">{{ currentEnterprise.businessScope }}</span>
          </div>
        </div>

        <!-- 联系信息 -->
        <div class="detail-section">
          <h3 class="section-title">联系信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">联系电话：</span>
                <span class="value">{{ currentEnterprise.phone }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="detail-item">
                <span class="label">邮箱：</span>
                <span class="value">{{ currentEnterprise.email }}</span>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 联系人记录 -->
        <div class="detail-section">
          <div class="section-header">
            <h3 class="section-title">联系人记录</h3>
            <el-button type="primary" size="small" @click="handleAddContact">新增联系人</el-button>
          </div>
          
          <!-- 联系人列表 -->
          <div class="contact-list">
            <!-- 显示全部选项 -->
            <div 
              class="contact-item"
              :class="{ active: !selectedContact }"
              @click="showAllContacts"
            >
              <div class="contact-header">
                <div class="contact-info">
                  <div class="contact-name">显示全部通话记录</div>
                  <div class="contact-position">查看所有联系人的通话记录</div>
                </div>
              </div>
            </div>
            
            <div 
              v-for="contact in contactList" 
              :key="contact.id" 
              class="contact-item"
              :class="{ active: selectedContact?.id === contact.id }"
              @click="selectContact(contact)"
            >
              <div class="contact-header">
                <div class="contact-info">
                  <div class="contact-name">{{ contact.name }}</div>
                  <div class="contact-position">{{ contact.position }} | {{ contact.department }}</div>
                </div>
                <div class="contact-actions">
                  <el-button size="small" type="success" @click.stop="handleCall(contact)">
                    <el-icon><Phone /></el-icon>拨打电话
                  </el-button>
                  <el-button size="small" @click.stop="handleEditContact(contact)">编辑</el-button>
                  <el-button size="small" type="danger" @click.stop="handleDeleteContact(contact)">删除</el-button>
                </div>
              </div>
              <div class="contact-details">
                <div class="contact-phone">{{ contact.phone }}</div>
                <div class="contact-email">{{ contact.email }}</div>
              </div>
            </div>
          </div>

          <!-- 通话记录和跟进记录 -->
          <div class="call-records-section">
            <div class="section-header">
              <h4 class="sub-section-title">
                {{ selectedContact ? selectedContact.name + ' - 通话记录' : '全部通话记录' }}
              </h4>
              <el-button type="primary" size="small" @click="handleAddCallRecord">新增通话记录</el-button>
            </div>
            
            <el-table :data="callRecords" style="width: 100%" v-loading="callRecordLoading">
              <el-table-column prop="contactName" label="联系人" width="100" v-if="!selectedContact" />
              <el-table-column prop="callTime" label="通话时间" width="160" />
              <el-table-column prop="duration" label="通话时长" width="100" />
              <el-table-column prop="callType" label="通话类型" width="100">
                <template #default="scope">
                  <el-tag :type="getCallTypeTagType(scope.row.callType)">
                    {{ getCallTypeLabel(scope.row.callType) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="result" label="通话结果" width="100">
                <template #default="scope">
                  <el-tag :type="getCallResultTagType(scope.row.result)">
                    {{ getCallResultLabel(scope.row.result) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="nextFollowUp" label="下次跟进" width="120" />
              <el-table-column prop="notes" label="通话记录" show-overflow-tooltip />
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="handleEditCallRecord(scope.row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteCallRecord(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 企业新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="140px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="企业名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入企业名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="统一社会信用代码" prop="creditCode">
              <el-input v-model="form.creditCode" placeholder="请输入统一社会信用代码" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="企业类型" prop="type">
              <el-select v-model="form.type" placeholder="请选择企业类型" style="width: 100%">
                <el-option label="有限责任公司" value="limited" />
                <el-option label="股份有限公司" value="joint" />
                <el-option label="个人独资企业" value="individual" />
                <el-option label="合伙企业" value="partnership" />
                <el-option label="国有企业" value="state" />
                <el-option label="外资企业" value="foreign" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行业" prop="industry">
              <el-select v-model="form.industry" placeholder="请选择行业" style="width: 100%">
                <el-option label="制造业" value="manufacturing" />
                <el-option label="信息技术" value="it" />
                <el-option label="金融业" value="finance" />
                <el-option label="房地产业" value="realestate" />
                <el-option label="教育" value="education" />
                <el-option label="医疗健康" value="healthcare" />
                <el-option label="零售业" value="retail" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="注册资本(万元)" prop="registeredCapital">
              <el-input-number v-model="form.registeredCapital" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="成立日期" prop="establishDate">
              <el-date-picker v-model="form.establishDate" type="date" placeholder="选择成立日期" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="法定代表人" prop="legalRepresentative">
              <el-input v-model="form.legalRepresentative" placeholder="请输入法定代表人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="经营状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择经营状态" style="width: 100%">
                <el-option label="在业" value="active" />
                <el-option label="存续" value="existing" />
                <el-option label="吊销" value="revoked" />
                <el-option label="注销" value="cancelled" />
                <el-option label="迁出" value="moved" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="注册地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入注册地址" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="经营范围" prop="businessScope">
          <el-input v-model="form.businessScope" type="textarea" :rows="3" placeholder="请输入经营范围" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 联系人新增/编辑对话框 -->
    <el-dialog v-model="contactDialogVisible" :title="contactDialogTitle" width="600px">
      <el-form :model="contactForm" :rules="contactRules" ref="contactFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="contactForm.name" placeholder="请输入联系人姓名" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="contactForm.position" placeholder="请输入职位" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="contactForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="contactForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="contactForm.department" placeholder="请输入部门" />
        </el-form-item>
        <el-form-item label="最后联系时间" prop="lastContactDate">
          <el-date-picker v-model="contactForm.lastContactDate" type="date" placeholder="选择最后联系时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="contactForm.notes" type="textarea" :rows="3" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="contactDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleContactSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 通话记录新增/编辑对话框 -->
    <el-dialog v-model="callRecordDialogVisible" :title="callRecordDialogTitle" width="700px">
      <el-form :model="callRecordForm" :rules="callRecordRules" ref="callRecordFormRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="通话时间" prop="callTime">
              <el-date-picker 
                v-model="callRecordForm.callTime" 
                type="datetime" 
                placeholder="选择通话时间" 
                style="width: 100%" 
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="通话时长(分钟)" prop="duration">
              <el-input-number v-model="callRecordForm.duration" :min="0" :max="300" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="通话类型" prop="callType">
              <el-select v-model="callRecordForm.callType" placeholder="请选择通话类型" style="width: 100%">
                <el-option label="呼入" value="incoming" />
                <el-option label="呼出" value="outgoing" />
                <el-option label="未接" value="missed" />
                <el-option label="拒接" value="rejected" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="通话结果" prop="result">
              <el-select v-model="callRecordForm.result" placeholder="请选择通话结果" style="width: 100%">
                <el-option label="成功" value="success" />
                <el-option label="失败" value="failed" />
                <el-option label="待跟进" value="pending" />
                <el-option label="已成交" value="closed" />
                <el-option label="无兴趣" value="no_interest" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="下次跟进时间" prop="nextFollowUp">
          <el-date-picker 
            v-model="callRecordForm.nextFollowUp" 
            type="datetime" 
            placeholder="选择下次跟进时间" 
            style="width: 100%" 
          />
        </el-form-item>
        
        <el-form-item label="通话记录" prop="notes">
          <el-input 
            v-model="callRecordForm.notes" 
            type="textarea" 
            :rows="4" 
            placeholder="请详细记录通话内容、客户反馈、跟进计划等" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="callRecordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCallRecordSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Phone } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新增企业')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const formRef = ref()

// 企业详情相关
const detailDialogVisible = ref(false)
const currentEnterprise = ref({})

// 联系人相关
const contactDialogVisible = ref(false)
const contactDialogTitle = ref('新增联系人')
const contactLoading = ref(false)
const contactFormRef = ref()
const contactList = ref([])
const selectedContact = ref(null)

// 通话记录相关
const callRecordDialogVisible = ref(false)
const callRecordDialogTitle = ref('新增通话记录')
const callRecordLoading = ref(false)
const callRecordFormRef = ref()
const callRecords = ref([])

// 搜索表单
const searchForm = reactive({
  name: '',
  creditCode: '',
  type: '',
  industry: '',
  capitalRange: '',
  status: ''
})

// 企业列表数据
const enterpriseList = ref([
  {
    id: 1,
    name: '北京科技有限公司',
    creditCode: '91110000123456789X',
    type: 'limited',
    industry: 'it',
    registeredCapital: 1000.00,
    establishDate: '2020-01-15',
    legalRepresentative: '张三',
    status: 'active',
    address: '北京市海淀区中关村大街1号',
    phone: '010-12345678',
    email: 'contact@techcompany.com',
    businessScope: '软件开发、技术服务、技术咨询、技术转让；计算机系统服务；数据处理；基础软件服务；应用软件服务；软件咨询；产品设计；模型设计；包装装潢设计；教育咨询；经济贸易咨询；文化咨询；体育咨询；公共关系服务；会议服务；工艺美术设计；电脑动画设计；项目投资；投资管理；资产管理；企业管理；企业管理咨询；企业策划、设计；设计、制作、代理、发布广告；市场调查；企业管理咨询；组织文化艺术交流活动；承办展览展示活动；会议服务；公共关系服务；销售计算机、软件及辅助设备、电子产品、机械设备、通讯设备。'
  },
  {
    id: 2,
    name: '上海制造有限公司',
    creditCode: '91310000123456789Y',
    type: 'limited',
    industry: 'manufacturing',
    registeredCapital: 5000.00,
    establishDate: '2018-06-20',
    legalRepresentative: '李四',
    status: 'active',
    address: '上海市浦东新区张江高科技园区',
    phone: '021-87654321',
    email: 'info@manufacturing.com',
    businessScope: '机械设备制造、销售；电子产品制造、销售；货物进出口、技术进出口；机械设备租赁；技术开发、技术咨询、技术服务。'
  },
  {
    id: 3,
    name: '深圳金融服务有限公司',
    creditCode: '91440300123456789Z',
    type: 'joint',
    industry: 'finance',
    registeredCapital: 10000.00,
    establishDate: '2019-03-10',
    legalRepresentative: '王五',
    status: 'active',
    address: '深圳市福田区金融中心',
    phone: '0755-12345678',
    email: 'service@finance.com',
    businessScope: '金融信息服务；投资咨询；企业管理咨询；财务咨询；税务咨询；法律咨询；商务信息咨询；市场调研；企业形象策划；市场营销策划；会展服务；翻译服务；计算机软件开发；网络技术开发；技术服务。'
  },
  {
    id: 4,
    name: '广州教育科技有限公司',
    creditCode: '91440100123456789A',
    type: 'limited',
    industry: 'education',
    registeredCapital: 500.00,
    establishDate: '2021-09-01',
    legalRepresentative: '赵六',
    status: 'active',
    address: '广州市天河区珠江新城',
    phone: '020-87654321',
    email: 'contact@education.com',
    businessScope: '教育软件开发；教育信息咨询；教育技术开发、技术咨询、技术服务；计算机软件开发；网络技术开发；技术服务；技术转让；技术推广；计算机系统服务；数据处理；基础软件服务；应用软件服务；软件咨询；产品设计；模型设计；包装装潢设计；教育咨询；经济贸易咨询；文化咨询；体育咨询；公共关系服务；会议服务；工艺美术设计；电脑动画设计；项目投资；投资管理；资产管理；企业管理；企业管理咨询；企业策划、设计；设计、制作、代理、发布广告；市场调查；企业管理咨询；组织文化艺术交流活动；承办展览展示活动；会议服务；公共关系服务；销售计算机、软件及辅助设备、电子产品、机械设备、通讯设备。'
  },
  {
    id: 5,
    name: '杭州医疗健康有限公司',
    creditCode: '91330100123456789B',
    type: 'limited',
    industry: 'healthcare',
    registeredCapital: 2000.00,
    establishDate: '2020-12-15',
    legalRepresentative: '钱七',
    status: 'active',
    address: '杭州市西湖区文三路',
    phone: '0571-12345678',
    email: 'info@healthcare.com',
    businessScope: '医疗技术开发、技术咨询、技术服务；医疗器械销售；健康管理咨询；营养健康咨询服务；心理咨询；康复理疗；保健服务；医疗信息咨询；医疗设备租赁；医疗软件开发；网络技术开发；技术服务；技术转让；技术推广；计算机系统服务；数据处理；基础软件服务；应用软件服务；软件咨询；产品设计；模型设计；包装装潢设计；教育咨询；经济贸易咨询；文化咨询；体育咨询；公共关系服务；会议服务；工艺美术设计；电脑动画设计；项目投资；投资管理；资产管理；企业管理；企业管理咨询；企业策划、设计；设计、制作、代理、发布广告；市场调查；企业管理咨询；组织文化艺术交流活动；承办展览展示活动；会议服务；公共关系服务；销售计算机、软件及辅助设备、电子产品、机械设备、通讯设备。'
  }
])

// 表单数据
const form = reactive({
  id: null,
  name: '',
  creditCode: '',
  type: '',
  industry: '',
  registeredCapital: 0,
  establishDate: '',
  legalRepresentative: '',
  status: 'active',
  address: '',
  phone: '',
  email: '',
  businessScope: ''
})

// 联系人表单数据
const contactForm = reactive({
  id: null,
  name: '',
  position: '',
  phone: '',
  email: '',
  department: '',
  lastContactDate: '',
  notes: ''
})

// 通话记录表单数据
const callRecordForm = reactive({
  id: null,
  callTime: '',
  duration: 0,
  callType: '',
  result: '',
  nextFollowUp: '',
  notes: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入企业名称', trigger: 'blur' }
  ],
  creditCode: [
    { required: true, message: '请输入统一社会信用代码', trigger: 'blur' },
    { pattern: /^[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}$/, message: '请输入正确的统一社会信用代码', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择企业类型', trigger: 'change' }
  ],
  industry: [
    { required: true, message: '请选择行业', trigger: 'change' }
  ],
  registeredCapital: [
    { required: true, message: '请输入注册资本', trigger: 'blur' }
  ],
  establishDate: [
    { required: true, message: '请选择成立日期', trigger: 'change' }
  ],
  legalRepresentative: [
    { required: true, message: '请输入法定代表人', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择经营状态', trigger: 'change' }
  ],
  address: [
    { required: true, message: '请输入注册地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$|^0\d{2,3}-?\d{7,8}$/, message: '请输入正确的联系电话', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 联系人表单验证规则
const contactRules = {
  name: [
    { required: true, message: '请输入联系人姓名', trigger: 'blur' }
  ],
  position: [
    { required: true, message: '请输入职位', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$|^0\d{2,3}-?\d{7,8}$/, message: '请输入正确的联系电话', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 通话记录表单验证规则
const callRecordRules = {
  callTime: [
    { required: true, message: '请选择通话时间', trigger: 'change' }
  ],
  duration: [
    { required: true, message: '请输入通话时长', trigger: 'blur' }
  ],
  callType: [
    { required: true, message: '请选择通话类型', trigger: 'change' }
  ],
  result: [
    { required: true, message: '请选择通话结果', trigger: 'change' }
  ],
  notes: [
    { required: true, message: '请输入通话记录', trigger: 'blur' }
  ]
}

// 获取状态标签样式
const getStatusTagType = (status) => {
  const statusMap = {
    active: 'success',
    existing: 'primary',
    revoked: 'warning',
    cancelled: 'danger',
    moved: 'info'
  }
  return statusMap[status] || 'info'
}

// 获取状态标签文本
const getStatusLabel = (status) => {
  const statusMap = {
    active: '在业',
    existing: '存续',
    revoked: '吊销',
    cancelled: '注销',
    moved: '迁出'
  }
  return statusMap[status] || '未知'
}

// 获取企业类型标签文本
const getTypeLabel = (type) => {
  const typeMap = {
    limited: '有限责任公司',
    joint: '股份有限公司',
    individual: '个人独资企业',
    partnership: '合伙企业',
    state: '国有企业',
    foreign: '外资企业'
  }
  return typeMap[type] || '未知'
}

// 获取行业标签文本
const getIndustryLabel = (industry) => {
  const industryMap = {
    manufacturing: '制造业',
    it: '信息技术',
    finance: '金融业',
    realestate: '房地产业',
    education: '教育',
    healthcare: '医疗健康',
    retail: '零售业',
    other: '其他'
  }
  return industryMap[industry] || '未知'
}

// 格式化注册资本
const formatCapital = (capital) => {
  if (capital >= 10000) {
    return `${(capital / 10000).toFixed(2)}亿元`
  } else {
    return `${capital.toFixed(2)}万元`
  }
}

// 获取通话类型标签样式
const getCallTypeTagType = (type) => {
  const typeMap = {
    incoming: 'success',
    outgoing: 'primary',
    missed: 'warning',
    rejected: 'danger'
  }
  return typeMap[type] || 'info'
}

// 获取通话类型标签文本
const getCallTypeLabel = (type) => {
  const typeMap = {
    incoming: '呼入',
    outgoing: '呼出',
    missed: '未接',
    rejected: '拒接'
  }
  return typeMap[type] || '未知'
}

// 获取通话结果标签样式
const getCallResultTagType = (result) => {
  const resultMap = {
    success: 'success',
    failed: 'danger',
    pending: 'warning',
    closed: 'primary',
    no_interest: 'info'
  }
  return resultMap[result] || 'info'
}

// 获取通话结果标签文本
const getCallResultLabel = (result) => {
  const resultMap = {
    success: '成功',
    failed: '失败',
    pending: '待跟进',
    closed: '已成交',
    no_interest: '无兴趣'
  }
  return resultMap[result] || '未知'
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

// 新增企业
const handleAddEnterprise = () => {
  dialogTitle.value = '新增企业'
  resetForm()
  dialogVisible.value = true
}

// 编辑企业
const handleEditEnterprise = (enterprise) => {
  dialogTitle.value = '编辑企业'
  Object.assign(form, enterprise)
  dialogVisible.value = true
}

// 查看企业详情
const handleViewEnterpriseDetail = (enterprise) => {
  currentEnterprise.value = { ...enterprise }
  detailDialogVisible.value = true
  loadContactList(enterprise.id)
}

// 查看企业
const handleViewEnterprise = (enterprise) => {
  ElMessage.info(`查看企业：${enterprise.name}`)
}

// 删除企业
const handleDeleteEnterprise = (enterprise) => {
  ElMessageBox.confirm(
    `确定要删除企业"${enterprise.name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    const index = enterpriseList.value.findIndex(item => item.id === enterprise.id)
    if (index > -1) {
      enterpriseList.value.splice(index, 1)
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
        const index = enterpriseList.value.findIndex(item => item.id === form.id)
        if (index > -1) {
          Object.assign(enterpriseList.value[index], { ...form })
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newId = Math.max(...enterpriseList.value.map(item => item.id)) + 1
        enterpriseList.value.push({
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
    form[key] = key === 'registeredCapital' ? 0 : key === 'status' ? 'active' : ''
  })
  form.id = null
}

// 加载联系人列表
const loadContactList = (enterpriseId) => {
  contactLoading.value = true
  // 模拟加载联系人数据
  setTimeout(() => {
    contactList.value = [
      {
        id: 1,
        name: '张经理',
        position: '销售经理',
        phone: '13800138001',
        email: 'zhang@company.com',
        department: '销售部',
        lastContactDate: '2024-03-15',
        notes: '主要联系人，负责产品采购'
      },
      {
        id: 2,
        name: '李总监',
        position: '技术总监',
        phone: '13800138002',
        email: 'li@company.com',
        department: '技术部',
        lastContactDate: '2024-03-10',
        notes: '技术对接负责人'
      }
    ]
    contactLoading.value = false
    // 默认加载所有通话记录
    loadAllCallRecords()
  }, 500)
}

// 选择联系人
const selectContact = (contact) => {
  selectedContact.value = contact
  loadCallRecords(contact.id)
}

// 显示全部联系人
const showAllContacts = () => {
  selectedContact.value = null
  loadAllCallRecords()
}

// 加载所有通话记录
const loadAllCallRecords = () => {
  callRecordLoading.value = true
  // 模拟加载所有联系人的通话记录数据
  setTimeout(() => {
    callRecords.value = [
      {
        id: 1,
        contactName: '张经理',
        callTime: '2024-03-15 14:30:00',
        duration: 15,
        callType: 'outgoing',
        result: 'success',
        nextFollowUp: '2024-03-20 10:00:00',
        notes: '客户对我们的产品很感兴趣，需要进一步了解技术细节。约定下周再次通话讨论具体合作方案。'
      },
      {
        id: 2,
        contactName: '张经理',
        callTime: '2024-03-10 09:15:00',
        duration: 8,
        callType: 'incoming',
        result: 'pending',
        nextFollowUp: '2024-03-15 14:00:00',
        notes: '客户来电咨询产品价格，已发送报价单，需要跟进确认。'
      },
      {
        id: 3,
        contactName: '张经理',
        callTime: '2024-03-05 16:45:00',
        duration: 0,
        callType: 'missed',
        result: 'failed',
        nextFollowUp: '2024-03-08 10:00:00',
        notes: '客户未接电话，需要重新安排时间联系。'
      },
      {
        id: 4,
        contactName: '李总监',
        callTime: '2024-03-12 11:20:00',
        duration: 25,
        callType: 'outgoing',
        result: 'success',
        nextFollowUp: '2024-03-18 15:00:00',
        notes: '技术对接会议，讨论了产品技术架构和集成方案。客户对技术方案满意，准备进入商务谈判阶段。'
      },
      {
        id: 5,
        contactName: '李总监',
        callTime: '2024-03-08 16:30:00',
        duration: 12,
        callType: 'incoming',
        result: 'pending',
        nextFollowUp: '2024-03-12 11:00:00',
        notes: '客户咨询技术文档和API接口，已发送相关资料，约定下周进行技术对接。'
      }
    ]
    callRecordLoading.value = false
  }, 300)
}

// 加载通话记录
const loadCallRecords = (contactId) => {
  callRecordLoading.value = true
  // 根据联系人ID筛选通话记录
  setTimeout(() => {
    const allRecords = [
      {
        id: 1,
        contactName: '张经理',
        callTime: '2024-03-15 14:30:00',
        duration: 15,
        callType: 'outgoing',
        result: 'success',
        nextFollowUp: '2024-03-20 10:00:00',
        notes: '客户对我们的产品很感兴趣，需要进一步了解技术细节。约定下周再次通话讨论具体合作方案。'
      },
      {
        id: 2,
        contactName: '张经理',
        callTime: '2024-03-10 09:15:00',
        duration: 8,
        callType: 'incoming',
        result: 'pending',
        nextFollowUp: '2024-03-15 14:00:00',
        notes: '客户来电咨询产品价格，已发送报价单，需要跟进确认。'
      },
      {
        id: 3,
        contactName: '张经理',
        callTime: '2024-03-05 16:45:00',
        duration: 0,
        callType: 'missed',
        result: 'failed',
        nextFollowUp: '2024-03-08 10:00:00',
        notes: '客户未接电话，需要重新安排时间联系。'
      },
      {
        id: 4,
        contactName: '李总监',
        callTime: '2024-03-12 11:20:00',
        duration: 25,
        callType: 'outgoing',
        result: 'success',
        nextFollowUp: '2024-03-18 15:00:00',
        notes: '技术对接会议，讨论了产品技术架构和集成方案。客户对技术方案满意，准备进入商务谈判阶段。'
      },
      {
        id: 5,
        contactName: '李总监',
        callTime: '2024-03-08 16:30:00',
        duration: 12,
        callType: 'incoming',
        result: 'pending',
        nextFollowUp: '2024-03-12 11:00:00',
        notes: '客户咨询技术文档和API接口，已发送相关资料，约定下周进行技术对接。'
      }
    ]
    
    // 根据联系人ID筛选记录
    const contact = contactList.value.find(c => c.id === contactId)
    if (contact) {
      callRecords.value = allRecords.filter(record => record.contactName === contact.name)
    } else {
      callRecords.value = []
    }
    callRecordLoading.value = false
  }, 300)
}

// 拨打电话
const handleCall = (contact) => {
  ElMessage.success(`正在拨打 ${contact.name} 的电话：${contact.phone}`)
  // 这里可以集成真实的电话系统
}

// 新增联系人
const handleAddContact = () => {
  contactDialogTitle.value = '新增联系人'
  resetContactForm()
  contactDialogVisible.value = true
}

// 编辑联系人
const handleEditContact = (contact) => {
  contactDialogTitle.value = '编辑联系人'
  Object.assign(contactForm, contact)
  contactDialogVisible.value = true
}

// 删除联系人
const handleDeleteContact = (contact) => {
  ElMessageBox.confirm(
    `确定要删除联系人"${contact.name}"吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    const index = contactList.value.findIndex(item => item.id === contact.id)
    if (index > -1) {
      contactList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 提交联系人表单
const handleContactSubmit = () => {
  contactFormRef.value.validate((valid) => {
    if (valid) {
      if (contactForm.id) {
        // 编辑
        const index = contactList.value.findIndex(item => item.id === contactForm.id)
        if (index > -1) {
          Object.assign(contactList.value[index], { ...contactForm })
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newId = Math.max(...contactList.value.map(item => item.id)) + 1
        contactList.value.push({
          ...contactForm,
          id: newId
        })
        ElMessage.success('新增成功')
      }
      contactDialogVisible.value = false
    }
  })
}

// 重置联系人表单
const resetContactForm = () => {
  Object.keys(contactForm).forEach(key => {
    contactForm[key] = ''
  })
  contactForm.id = null
}

// 新增通话记录
const handleAddCallRecord = () => {
  callRecordDialogTitle.value = '新增通话记录'
  resetCallRecordForm()
  callRecordDialogVisible.value = true
}

// 编辑通话记录
const handleEditCallRecord = (callRecord) => {
  callRecordDialogTitle.value = '编辑通话记录'
  Object.assign(callRecordForm, callRecord)
  callRecordDialogVisible.value = true
}

// 删除通话记录
const handleDeleteCallRecord = (callRecord) => {
  ElMessageBox.confirm(
    `确定要删除这条通话记录吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    const index = callRecords.value.findIndex(item => item.id === callRecord.id)
    if (index > -1) {
      callRecords.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
}

// 提交通话记录表单
const handleCallRecordSubmit = () => {
  callRecordFormRef.value.validate((valid) => {
    if (valid) {
      if (callRecordForm.id) {
        // 编辑
        const index = callRecords.value.findIndex(item => item.id === callRecordForm.id)
        if (index > -1) {
          Object.assign(callRecords.value[index], { ...callRecordForm })
        }
        ElMessage.success('编辑成功')
      } else {
        // 新增
        const newId = Math.max(...callRecords.value.map(item => item.id)) + 1
        callRecords.value.push({
          ...callRecordForm,
          id: newId
        })
        ElMessage.success('新增成功')
      }
      callRecordDialogVisible.value = false
    }
  })
}

// 重置通话记录表单
const resetCallRecordForm = () => {
  Object.keys(callRecordForm).forEach(key => {
    callRecordForm[key] = key === 'duration' ? 0 : ''
  })
  callRecordForm.id = null
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
  setTimeout(() => {
    loading.value = false
    total.value = enterpriseList.value.length
  }, 500)
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.enterprise-container {
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

.enterprise-list {
  margin-bottom: 20px;
}

.enterprise-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 16px;
  padding: 20px;
  background: #fff;
  transition: all 0.3s ease;
  cursor: pointer;
}

.enterprise-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.enterprise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.enterprise-name {
  display: flex;
  align-items: center;
  gap: 12px;
}

.enterprise-name .name {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.enterprise-actions {
  display: flex;
  gap: 8px;
}

.enterprise-info {
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  margin-bottom: 12px;
}

.info-item {
  flex: 1;
  display: flex;
  align-items: center;
}

.info-item.full-width {
  flex: 2;
}

.info-item .label {
  color: #606266;
  font-weight: 500;
  min-width: 120px;
  margin-right: 8px;
}

.info-item .value {
  color: #303133;
  flex: 1;
}

.enterprise-footer {
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.footer-item {
  display: flex;
  align-items: flex-start;
}

.footer-item .label {
  color: #606266;
  font-weight: 500;
  min-width: 120px;
  margin-right: 8px;
  margin-top: 2px;
}

.footer-item .value {
  color: #303133;
  flex: 1;
  line-height: 1.6;
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

/* 企业详情弹窗样式 */
.enterprise-detail-dialog :deep(.el-dialog__body) {
  padding: 20px;
}

.enterprise-detail {
  max-height: 600px;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header .section-title {
  margin: 0;
}

.detail-item {
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
}

.detail-item .label {
  color: #606266;
  font-weight: 500;
  min-width: 140px;
  margin-right: 10px;
  flex-shrink: 0;
}

.detail-item .value {
  color: #303133;
  flex: 1;
  line-height: 1.6;
}

/* 企业名称点击样式 */
.enterprise-name .name {
  cursor: pointer;
  color: #409eff;
  transition: color 0.3s ease;
}

.enterprise-name .name:hover {
  color: #66b1ff;
}

/* 联系人列表样式 */
.contact-list {
  margin-bottom: 20px;
}

.contact-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 16px;
  background: #fff;
  transition: all 0.3s ease;
  cursor: pointer;
}

.contact-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
}

.contact-item.active {
  border-color: #409eff;
  background: #f0f9ff;
}

.contact-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.contact-position {
  font-size: 14px;
  color: #606266;
}

.contact-actions {
  display: flex;
  gap: 8px;
}

.contact-details {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #606266;
}

.contact-phone,
.contact-email {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 通话记录区域样式 */
.call-records-section {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
}

.sub-section-title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}
</style> 