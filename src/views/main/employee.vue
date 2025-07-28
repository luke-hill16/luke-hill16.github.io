<template>
    <div class="employee-list-container">
      <el-card>
        <div class="header">
          <span>员工列表</span>
          <el-button type="primary" @click="fetchEmployees" size="small" style="float:right;">刷新</el-button>
        </div>
        <el-table :data="employees" style="width: 100%; margin-top: 20px;" fit="true">
            <el-table-column prop="realname" label="姓名" min-width="120">
                <template #default="scope">
                    <span class="clickable-name" @click="showEmployeeDetail(scope.row)">{{ scope.row.realname }}</span>
                </template>
            </el-table-column>
          <el-table-column prop="email" label="邮箱" min-width="200"/>
          <el-table-column prop="department.name" label="部门" min-width="120"/>
          <el-table-column prop="status" label="状态" min-width="100">
            <template #default="scope">
              <el-tag v-if="scope.row.status===1" type="success">已激活</el-tag>
              <el-tag v-else-if="scope.row.status===2" type="info">未激活</el-tag>
              <el-tag v-else type="danger">锁定</el-tag>
            </template>
          </el-table-column>
          <!-- 你可以继续加更多列 -->
          <el-table-column prop="date_joined" label="入职时间" min-width="120"/>
        <el-table-column label="操作" min-width="200">
          <template #default="scope">
            <el-button size="small" type="primary" @click="editEmployee(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteEmployee(scope.row)">删除</el-button>
          </template>
        </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 员工详情弹窗 -->
<el-dialog v-model="detailVisible" title="员工详情" width="900px" :before-close="handleClose">
  <div class="employee-detail" v-if="currentEmployee">
    <!-- 基本信息卡片 -->
    <el-card class="info-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
          <el-button type="primary" size="small" @click="editEmployee(currentEmployee)">编辑信息</el-button>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="detail-item">
            <label>姓名：</label>
            <span>{{ currentEmployee.realname }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="detail-item">
            <label>邮箱：</label>
            <span>{{ currentEmployee.email }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="detail-item">
            <label>电话：</label>
            <span>{{ currentEmployee.telephone }}</span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="detail-item">
            <label>部门：</label>
            <span>{{ currentEmployee.department?.name }}</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="detail-item">
            <label>状态：</label>
            <el-tag v-if="currentEmployee.status===1" type="success">已激活</el-tag>
            <el-tag v-else-if="currentEmployee.status===2" type="info">未激活</el-tag>
            <el-tag v-else type="danger">锁定</el-tag>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="detail-item">
            <label>入职时间：</label>
            <span>{{ currentEmployee.date_joined }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 工作记录表格 -->
    <el-card class="work-record-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>工作记录</span>
          <div class="header-actions">
            <el-button type="success" size="small" @click="addWorkRecord">添加记录</el-button>
            <el-button type="primary" size="small" @click="refreshWorkRecords">刷新</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="workRecords" style="width: 100%" stripe>
        <el-table-column prop="date" label="日期" width="120"/>
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.type === '请假'" type="warning">{{ scope.row.type }}</el-tag>
            <el-tag v-else-if="scope.row.type === '加班'" type="danger">{{ scope.row.type }}</el-tag>
            <el-tag v-else type="success">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="150"/>
        <el-table-column prop="description" label="描述" min-width="200"/>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === '已批准'" type="success">{{ scope.row.status }}</el-tag>
            <el-tag v-else-if="scope.row.status === '待审批'" type="warning">{{ scope.row.status }}</el-tag>
            <el-tag v-else type="danger">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="approver" label="审批人" width="100"/>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewRecordDetail(scope.row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</el-dialog>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { ElMessage, ElMessageBox  } from 'element-plus'
  import employeeApi from '@/api/employeeHttp' // 你需要实现这个API
        // 模拟员工数据
        const mockEmployees = [
        {
            uid: 'emp001',
            realname: '张三',
            email: 'zhangsan@company.com',
            telephone: '13800138001',
            department: { name: '技术部' },
            status: 1,
            date_joined: '2023-01-15'
        },
        {
            uid: 'emp002',
            realname: '李四',
            email: 'lisi@company.com',
            telephone: '13800138002',
            department: { name: '人事部' },
            status: 1,
            date_joined: '2023-02-20'
        },
        {
            uid: 'emp003',
            realname: '王五',
            email: 'wangwu@company.com',
            telephone: '13800138003',
            department: { name: '财务部' },
            status: 2,
            date_joined: '2023-03-10'
        },
        {
            uid: 'emp004',
            realname: '赵六',
            email: 'zhaoliu@company.com',
            telephone: '13800138004',
            department: { name: '市场部' },
            status: 1,
            date_joined: '2023-04-05'
        },
        {
            uid: 'emp005',
            realname: '钱七',
            email: 'qianqi@company.com',
            telephone: '13800138005',
            department: { name: '技术部' },
            status: 3,
            date_joined: '2023-05-12'
        },
        {
            uid: 'emp006',
            realname: '孙八',
            email: 'sunba@company.com',
            telephone: '13800138006',
            department: { name: '人事部' },
            status: 1,
            date_joined: '2023-06-18'
        },
        {
            uid: 'emp007',
            realname: '周九',
            email: 'zhoujiu@company.com',
            telephone: '13800138007',
            department: { name: '财务部' },
            status: 1,
            date_joined: '2023-07-22'
        },
        {
            uid: 'emp008',
            realname: '吴十',
            email: 'wushi@company.com',
            telephone: '13800138008',
            department: { name: '市场部' },
            status: 2,
            date_joined: '2023-08-30'
        }
        ]
  const employees = ref([])
  
  //const fetchEmployees = async () => {
    //try {
      //const res = await employeeApi.list() // 假设返回 {data: [...]}
      //employees.value = res.data
    //} catch (e) {
      //ElMessage.error('获取员工列表失败')
    //}
  //}
  const detailVisible = ref(false)
    const currentEmployee = ref(null)

    const showEmployeeDetail = (employee) => {
    currentEmployee.value = employee
    detailVisible.value = true
    }
  const fetchEmployees = async () => {
  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    employees.value = mockEmployees
    ElMessage.success('员工列表加载成功')
  } catch (e) {
    ElMessage.error('获取员工列表失败')
  }
}
const editEmployee = (row) => {
  ElMessage.info(`编辑员工: ${row.realname}`)
  // 这里可以实现编辑弹窗逻辑
}
const deleteEmployee = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除员工 ${row.realname} 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    // 模拟删除操作
    employees.value = employees.value.filter(emp => emp.uid !== row.uid)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}

  onMounted(fetchEmployees)
  </script>
  
  <style scoped>
.employee-list-container {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  height: calc(100vh - 160px);
  overflow: auto;
}

.employee-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.employee-card :deep(.el-card__body) {
  flex: 1;
  padding: 0;
  display: flex;
  flex-direction: column;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}
.header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 确保表格容器占满可用空间 */
.employee-list-container .el-card {
  height: 100%;
}
/* 确保表格占满剩余空间 */
.employee-card :deep(.el-table) {
  flex: 1;
}
.employee-list-container .el-card__body {
  height: 100%;
  padding: 20px;
}

/* 表格自适应 */
.employee-list-container .el-table {
  height: calc(100% - 60px);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .employee-list-container {
    padding: 10px;
  }
  
  .employee-list-container .el-card__body {
    padding: 10px;
  }
}
.clickable-name {
  color: #409eff;
  cursor: pointer;
}
.clickable-name:hover {
  text-decoration: underline;
}

.employee-detail {
  padding: 20px;
}
.detail-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}
.detail-item label {
  font-weight: bold;
  width: 100px;
  color: #606266;
}
.detail-item span {
  color: #303133;
}
</style>