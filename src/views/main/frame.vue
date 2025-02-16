<template>
  <el-container class="container">
    <el-aside class="aside" width="250px">
      <router-link to="/" class="brand">益客管理系统</router-link>
      <el-menu
        :router="true"
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item index="1">
          <template #title>
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </template>
        </el-menu-item>
        <el-sub-menu index="2">
          <template #title>
            <el-icon><Calendar /></el-icon>
            <span>考勤管理</span>
          </template>
          <el-menu-item index="2-1" :route="{ name: 'myabsent' }"
            ><el-icon><Avatar /></el-icon>个人管理</el-menu-item
          >
          <el-menu-item index="2-2" :route="{ name: 'subabsent' }"
            ><el-icon><UserFilled /></el-icon>下属考勤</el-menu-item
          >
        </el-sub-menu>
        <el-sub-menu index="3">
          <template #title>
            <el-icon><Files /></el-icon>
            <span>通知管理</span>
          </template>
          <el-menu-item index="3-1"
            ><el-icon><Tools /></el-icon>发布通知</el-menu-item
          >
          <el-menu-item index="3-2"
            ><el-icon><Comment /></el-icon>通知列表</el-menu-item
          >
        </el-sub-menu>
        <el-sub-menu index="5">
          <template #title>
            <el-icon><User /></el-icon>
            <span>员工管理</span>
          </template>
          <el-menu-item index="5-1"
            ><el-icon><BellFilled /></el-icon>新增通知</el-menu-item
          >
          <el-menu-item index="5-2"
            ><el-icon><Briefcase /></el-icon>员工列表</el-menu-item
          >
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="left-header">
          <el-button
            ><el-icon><Expand /></el-icon
          ></el-button>
        </div>
        <el-button
          v-show="isCollapse"
          :icon="Expand"
          @click="onCollapseAside"
        />
        <div class="right-header">
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-avatar :size="30" icon="UserFilled" /><span
                style="margin-left: 10px"
                >({{ authStore.user.department.name }}){{
                  authStore.user.realname
                }}</span
              >
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="onControlResetPwdDialog">修改密码</el-dropdown-item>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item divided @click="onExit"
                  >退出登录</el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main"><RouterView></RouterView></el-main>
    </el-container>
  </el-container>
  <el-dialog v-model="dialogVisible" title="修改密码" width="500">
    <el-form :model="resetpwdform" :rules="rules" ref='formTag'>
      <el-form-item label="旧密码" :label-width="formLabelWidth" prop="oldpwd">
        <el-input v-model="resetpwdform.oldpwd" autocomplete="off"  type="password"/>
      </el-form-item>

      <el-form-item label="新密码" :label-width="formLabelWidth" prop="pwd1">
        <el-input v-model="resetpwdform.pwd1" autocomplete="off" type="password" />
      </el-form-item>

      <el-form-item label="确认密码" :label-width="formLabelWidth" prop="pwd2">
        <el-input v-model="resetpwdform.pwd2" autocomplete="off" type="password" />
      </el-form-item>
      
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>


<script setup name="frame">
import { ref, computed ,reactive} from "vue";
import { Expand, Fold } from "@element-plus/icons-vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import authHttp from "@/api/authHttp"
import {ElMessage} from "element-plus"
let formLabelWidth = '140px'
//ref divided
let dialogVisible=ref(false)
let resetpwdform =reactive({
  oldpwd:'',
  pwd1:'',
  pwd2:'',
})
let formTag=ref()
let rules=reactive({
  oldpwd:[
    { required: true, message: '旧密码', trigger: 'blur' },
    { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' },
  ],
  pwd1:[
    { required: true, message: '新密码', trigger: 'blur' },
    { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' },
  ],
  pwd2:[
    { required: true, message: '确认密码', trigger: 'blur' },
    { min: 6, max: 20, message: 'Length should be 6 to 20', trigger: 'blur' },
  ]
})
const authStore = useAuthStore();
const router = useRouter();
//console.log("user:",authStore.user);
const onExit = () => {
  authStore.clearUserToken();
  router.push({ name: "login" });
};
const onControlResetPwdDialog = () =>{
  resetpwdform.oldpwd=''
  resetpwdform.pwd1=''
  resetpwdform.pwd2=''
  dialogVisible.value=true
}
const onSubmit= () =>{
  formTag.value.validate(async(valid,fields)=>{
    if(valid){
      //console.log('字段校验成功!');}
      try{
        await authHttp.resetPwd(resetpwdform.oldpwd,resetpwdform.pwd1,resetpwdform.pwd2)
        //await resetPwd(resetpwdform.oldpwd,resetpwdform.pwd1,resetpwdform.pwd2)
        ElMessage.success("密码修改成功")
        dialogVisible.value=false
      }catch(detail){
        ElMessage.error(detail)
      }}
    else{
      ElMessage.info('字段校验失败!')
      console.log('字段校验失败!');}
      console.log(fields)
      })
  //console.log("点击啦 提交")
  dialogVisible.value=false
}

</script>

<style scoped>
.aside {
  background-color: #e0e0e0;
}
.container {
  height: 100vh;
  background-color: #f5f6f9;
}
.aside .brand {
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid#3c3c3c;
  background-color: #5f6fd5;
  display: flex;
  height: 60px;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}
.header {
  background-color: #fff;
  border-bottom: 1px solid#e6e6e6;
  height: 60px;
  display: flex;
  justify-content: space-between;
}
.el-menu {
  border-right: none;
}
.header .left-header {
  display: flex;
  align-items: center;
  justify-content: center;
}
.header .right-header {
  display: flex;
  align-items: center;
  justify-content: center;
}
.el-dropdown-link {
  display: flex;
  align-items: center;
}
.el-dropdown-link:focus {
  outline: none;
}
</style>