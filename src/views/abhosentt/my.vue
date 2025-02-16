<template>
  <el-space direction="vertical" fill :size="20" style="width: 100%">
    <OAPageHeader content="个人考勤"></OAPageHeader>

    <el-card style="border-bottom: 1px solid#fff" shadow="none">
      邮箱<el-input
        v-model="input"
        style="width: 240px; text-align: left; margin: 20px"
        placeholder="Please input"
      />
      姓名<el-input
        v-model="input"
        style="width: 240px; text-align: left; margin: 20px"
        placeholder="Please input"
      />
      地址<el-select
        v-model="value"
        placeholder="Select"
        size="middle"
        style="width: 240px; margin: 20px"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-button type="primary">编辑</el-button>
      <el-button>重置</el-button>
      <div style="text-align: right">
        <el-button type="primary" @click="onShowDialog"
          ><el-icon><Plus /></el-icon>发起考勤</el-button
        >
      </div>
    </el-card></el-space
  >
  <el-dialog v-model="dialogFormVisible" title="发起考勤" width="600">
    <el-form :model="absentForm"  :rules="rules" ref='absentFormRef'>
      <el-form-item label="标题" :label-width="formLabelWidth" prop='title'>
        <el-input v-model="absentForm.title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="请假类型" :label-width="formLabelWidth" prop='absent_type_id'>
        <el-select
          v-model="absentForm.absent_type_id"
          placeholder="请选择请假类型"
        >
          <el-option
            v-for="item in absent_types"
            :label="item.name"
            :value="item.id"
            :key="item.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="起止日期" :label-width="formLabelWidth" prop='date_range'>
        <el-date-picker
          v-model="absentForm.date_range"
          type="daterange"
          range-separator="到"
          start-placeholder="起始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
        value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="审批人" :label-width="formLabelWidth">
        <el-input :value="responder_str" readonly disabled autocomplete="off" />
      </el-form-item>
      <el-form-item label="请假理由" :label-width="formLabelWidth" prop='request_content'>
        <el-input type="textarea"   v-model="absentForm.request_content" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmitAbsent">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
<el-card>
  <el-table
    :data="absents"
    stripe
    style="width: 100%"
    :default-sort="{ prop: 'date', order: 'descending' }"
    fit="False"
  >
  
    <el-table-column type="selection" :selectable="selectable" width="55" />
    <el-table-column type="index" width="50" />
    <el-table-column prop="title" label="标题" sortable />
    <el-table-column prop="absent_type.name" label="类型"  />
    <el-table-column prop="request_content" label="原因" />
    <el-table-column prop="start_date" label="开始时间" sortable />
    <el-table-column prop="end_date" label="结束时间" />
    <el-table-column prop="create_time.format('YYYY-MM-DD')" label="发起它的时间" />
    <el-table-column label="审核领导" >
      {{responder_str}}
    </el-table-column>
    <el-table-column prop="response_content" label="反馈意见" />
    <el-table-column  label="审核状态" >
    <template #default="scope">
      <el-tag type="info" v-if="scope.row.status==1">审核中</el-tag>
      <el-tag type="success" v-else-if="scope.row.status==2">已通过</el-tag>
      <el-tag type="danger" v-else>已拒绝</el-tag>
    </template>
    </el-table-column>
    
    <el-table-column label="Operations">
      <template #default="scope">
        <el-button
          size="small"
          type="primary"
          @click="handleEdit(scope.$index, scope.row)"
        >
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
  </el-table></el-card>
  <div
    class="demo-pagination-block"
    style="display: flex; align-items: right; justify-content: right"
  >
    <div class="demonstration"></div>
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

<script setup name='my_abhosentt'>
import OAPageHeader from "@/components/OAPageHeader.vue";
import { ref, reactive ,onMounted,computed} from "vue";
import absentHttp from "@/api/absentHttp"
import {ElMessage} from "element-plus"
let dialogFormVisible = ref(false);
let formlabelWidth = "100px";
let absent_types = ref([]);
let responder=reactive({
  email:'',
  realname:''
})
let absents=ref([])
let responder_str=computed(()=>{
  if (responder.email){
    return '['+ responder.email+']'+responder.realname
  }else{
    return'无'
  }
}
)
let absentForm = reactive({
  title: "",
  absent_type_id: null,
  date_range: [],
  request_content: "",
});
const onShowDialog = () => {
  absentForm.title = "";
  absentForm.absent_type_id = null;
  absentForm.date_range = [];
  absentForm.request_content = "";
  dialogFormVisible.value = true;
};
const tableData = [
  {
    date: "2016-05-03",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "进行中",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-02",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "进行中",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-04",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "进行中",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
    tag: "未完成",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
  },
  {
    date: "2016-05-01",
    name: "Tom",
    address: "No. 189, Grove St, Los Angeles",
    tag: "未完成",
    email: "1164800955@qq.com",
  },
];
let rules=reactive({
  title:[
    {required:true,message:'请输入标题！',trigger: 'blur'}
  ],
  absent_type_id:[
  {required:true,message:'请选择请假类型！',trigger: 'change'}
  ],
  date_range:[
    {required:true,message:'请选择请假时间！',trigger: 'blur'}
  ],
  request_content:[
    {required:true,message:'请输入请假理由！',trigger: 'blur'}
  ]

})
let absentFormRef=ref()
const onSubmitAbsent=()=>{
  absentFormRef.value.validate(async(valid,fields)=>{
    if(valid){
      let data={
        title:absentForm.title,
        absent_type_id:absentForm.absent_type_id,
        start_date:absentForm.date_range[0],
        end_date:absentForm.date_range[1],
        request_content:absentForm.request_content,
      }
      try{
        let absent=await absentHttp.applyAbsent(data) 
        console.log(absent);
        dialogFormVisible.value  = false
      }catch(detail){
        ElMessage.error(detail)
    }}})
  
  }

onMounted(async()=>{
  try{
    let absent_types_data=await absentHttp.getAbhsentTypes()
    absent_types.value=absent_types_data
    let responder_data=await absentHttp.getResponder()
    Object.assign(responder,responder_data)
    let absents_data=await absentHttp.getMyAbsents()
    absents.value=absents_data
    console.log(absents.value)
  }catch(detail){
    ElMessage.error(detail)
  }
})
//<el-table-column prop="absent_type.name" label="类型" width="180" />?
</script>

<style>
</style>