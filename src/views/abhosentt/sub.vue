<template>
  <el-space direction="vertical" fill :size="20" style="width: 100%">
    <OAPageHeader content="下属考勤"></OAPageHeader>
    
    <el-card style="border-bottom: 1px solid#fff;" shadow=none >
        邮箱<el-input v-model="input" style="width: 240px;text-align:left;margin:20px" placeholder="Please input" />
        姓名<el-input v-model="input" style="width: 240px;text-align:left;margin:20px" placeholder="Please input" />
        地址<el-select
      v-model="value"
      placeholder="Select"
      size="middle"
      style="width: 240px;margin:20px"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-button type="primary" >编辑</el-button>
    <el-button>重置</el-button>
      <div style="text-align: right "><el-button  type="primary" @click="onShowDialog"
        ><el-icon><Plus /></el-icon>发起考勤</el-button
      ></div>
    </el-card></el-space
  >
  <el-dialog v-model="dialogFormVisible" title="发起考勤" width="500">
    <el-form :model="absentForm">
      <el-form-item label="标题" :label-width="formLabelWidth">
        <el-input v-model="absentForm.title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="请假类型" :label-width="formLabelWidth">
        <el-select v-model="absentForm.absent_type_id" placeholder="请选择请假类型">
          <el-option v-for="item in absent_types" :label="item.name" :value="item.id" :key="item.name" />
          
        </el-select>
      </el-form-item>
      <el-form-item label="起止日期" :label-width="formLabelWidth">
        
      
      <el-date-picker
        v-model="absentForm.date_range"
        type="daterange"
        range-separator="到"
        start-placeholder="起始日期"
        end-placeholder="结束日期"
        
      />
    
    </el-form-item>
    <el-form-item label="审批人" :label-width="formLabelWidth">
        <el-input value="[dongdong@qq.com]" readonly disabled autocomplete="off" />
      </el-form-item>
      <el-form-item label="请假理由" :label-width="formLabelWidth">
        <el-input type="textarea"   v-model="absentForm.request_content" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          确定
        </el-button>
      </div>
      
    </template>
  </el-dialog>
  
  
  <el-table :data="tableData" stripe style="width: 100%" :default-sort="{ prop: 'date', order: 'descending' }" fit='False'>
    <el-table-column type="selection" :selectable="selectable" width="55" />
    <el-table-column type="index" width="50" />
    <el-table-column prop="date" label="Date" width="180" sortable/>
    <el-table-column prop="name" label="Name" width="180" />
    <el-table-column prop="address" label="Address" sortable/>
    <el-table-column prop="email" label="Email" />
    <el-table-column
      prop="tag"
      label="Tag"
      width="100"
      :filters="[
        { text: '进行中', value: '进行中' },
        { text: '未完成', value: '未完成' },
      ]"
      :filter-method="filterTag"
      filter-placement="bottom-end"
    >
      <template #default="scope">
        <el-tag
          :type="scope.row.tag === '进行中' ? 'primary' : 'success'"
          disable-transitions
          >{{ scope.row.tag }}</el-tag
        >
      </template></el-table-column>
    
    
  <el-table-column label="Operations">
      <template #default="scope">
        <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)">
          编辑
        </el-button>
        <el-button
          size="small"
          type="primary"
          @click="handleDelete(scope.$index, scope.row)"
        >
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <div class="demo-pagination-block" style='display: flex;align-items: right;justify-content: right;'>
    <div class="demonstration" ></div>
    <el-pagination
      
      :page-sizes="[100, 200, 300, 400]"
      :size="size"
      :disabled="disabled"
      :background="background"
      layout="total, sizes, prev, pager, next, jumper"
      :total="400"
      @size-change="handleSizeChange"
      
    />
  </div>  
</template>

<script setup name='sub_abhosentt'>
import OAPageHeader from "@/components/OAPageHeader.vue";
import {ref ,reactive}from"vue"
let dialogFormVisible =ref(false)
let formlabelWidth ="100px"
let absent_types = ref([])
let absentForm =reactive({
    title:'',
    absent_type_id: null,
    date_range:[],
    request_content:''})
const onShowDialog=()=>{
    absentForm.title=''
    absentForm.absent_type_id = null
    absentForm.date_range =[]
    absentForm.request_content =''
    dialogFormVisible.value = true;}
const tableData = [
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'进行中',email:'1164800955@qq.com',
  },
  {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'进行中',email:'1164800955@qq.com',
  },
  {
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'进行中',email:'1164800955@qq.com',
  },
  {
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
  },{
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
  },{
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
  },{
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
  },{
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
    tag :'未完成',
  },{
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
  },{
    date: '2016-05-01',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',tag :'未完成',email:'1164800955@qq.com',
  },
]

</script>

<style>
</style>