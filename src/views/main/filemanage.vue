<template>
  <div>
    <h2 style="margin-bottom: 10px;">文件管理</h2>
    <div style="margin-bottom: 16px; color: #888;">
      当前共 <b>{{ fileList.length }}</b> 个文件，已用存储 <b>{{ totalSizeMB }} MB</b>
    </div>
    <el-upload
      class="upload-demo"
      action="/api/auth/files/upload/"
      name="file"
      :headers="uploadHeaders"
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-success="handleUploadSuccess"
      :on-error="handleUploadError"
      style="margin-bottom: 20px;"
    >
      <el-button type="primary">上传文件</el-button>
      <span style="margin-left: 12px; color: #aaa;">支持图片、文档、文本等类型，单文件不超过10MB</span>
    </el-upload>

    <el-table :data="fileList" style="width: 100%; margin-bottom: 20px;">
      <el-table-column prop="original_name" label="文件名" />
      <el-table-column prop="upload_time" label="上传时间" />
      <el-table-column prop="uploader_name" label="上传者" />
      <el-table-column prop="size_display" label="大小" width="100" />
      <el-table-column prop="file_type_display" label="类型" width="80" />
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button size="small" @click="handlePreview(scope.row)">预览</el-button>
          <el-button size="small" type="success" @click="handleDownload(scope.row)">下载</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div v-if="fileList.length === 0" style="text-align:center; color:#aaa; margin-top:40px;">
      <div style="width:100px; height:100px; margin:0 auto 16px; background:#f5f5f5; border-radius:8px; display:flex; align-items:center; justify-content:center;">
        <el-icon style="font-size:40px; color:#ddd;"><Folder /></el-icon>
      </div>
      <div>暂无文件，快来上传你的第一个文件吧！</div>
    </div>

    <el-card style="margin-top: 32px;">
      <template #header>
        <span>操作说明</span>
      </template>
      <ul>
        <li>点击“上传文件”按钮选择并上传文件。</li>
        <li>支持图片、文档、文本等常见类型，单文件最大10MB。</li>
        <li>上传后可在列表中预览、下载文件。</li>
        <li>如遇上传失败，请检查网络或文件类型/大小。</li>
      </ul>
    </el-card>

    <!-- 预览弹窗 -->
    <el-dialog v-model="previewVisible" title="文件预览" width="60%">
      <div v-if="previewLoading">加载中...</div>
      <div v-else-if="previewError">{{ previewError }}</div>
      <template v-else>
        <!-- 图片 -->
        <img v-if="previewType === 'image'" :src="previewUrl" style="max-width:100%;max-height:60vh;" />
        <!-- PDF -->
        <iframe
          v-else-if="isPdf"
          :src="pdfViewerUrl"
          style="width:100%;height:80vh;border:none;"
        ></iframe>
        <!-- Office文档（Word/Excel/PPT） -->
        <iframe
          v-else-if="isOffice"
          :src="officeViewerUrl"
          style="width:100%;height:80vh;border:none;"
        ></iframe>
        <!-- 纯文本 -->
        <pre v-else-if="previewType === 'text'" style="max-height:400px;overflow:auto;">{{ previewContent }}</pre>
        <!-- 其它类型 -->
        <div v-else>该文件类型暂不支持预览</div>
      </template>
    </el-dialog>

    <!-- 上传结果弹窗 -->
    <el-dialog v-model="uploadResultVisible" title="上传结果" width="30%">
      <div>{{ uploadResultMsg }}</div>
      <template #footer>
        <el-button type="primary" @click="uploadResultVisible = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const fileList = ref([])
const previewVisible = ref(false)
const previewUrl = ref('')
const previewContent = ref('')
const previewType = ref('')
const previewMime = ref('')
const previewName = ref('')
const previewLoading = ref(false)
const previewError = ref('')
const uploadResultVisible = ref(false)
const uploadResultMsg = ref('')

const uploadHeaders = {
  Authorization: 'JWT ' + localStorage.getItem('OA_TOKEN_KEY')
}

const fetchFiles = async () => {
  try {
    if (!authStore.is_logined) {
      ElMessage.error('请先登录')
      router.push('/login')
      return
    }
    const { data } = await axios.get('/api/auth/files/', {
      headers: uploadHeaders
    })
    fileList.value = Array.isArray(data) ? data : []
  } catch (e) {
    fileList.value = []
    ElMessage.error('获取文件列表失败')
  }
}

const totalSizeMB = computed(() => {
  return (fileList.value.reduce((sum, f) => sum + (f.size || 0), 0) / (1024 * 1024)).toFixed(2)
})

const beforeUpload = (file) => {
  if (!authStore.is_logined) {
    ElMessage.error('请先登录')
    router.push('/login')
    return false
  }
  const allowedTypes = [
    'image/png', 'image/jpeg', 'image/gif', 'application/pdf', 'text/plain',
    'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
  ]
  if (!allowedTypes.includes(file.type)) {
    uploadResultMsg.value = '不支持的文件类型'
    uploadResultVisible.value = true
    return false
  }
  if (file.size > 10 * 1024 * 1024) {
    uploadResultMsg.value = '文件不能超过10MB'
    uploadResultVisible.value = true
    return false
  }
  return true
}

const handleUploadSuccess = (response, file) => {
  uploadResultMsg.value = '上传成功'
  uploadResultVisible.value = true
  fetchFiles()
}

const handleUploadError = (err, file) => {
  uploadResultMsg.value = '上传失败'
  uploadResultVisible.value = true
}

const handlePreview = async (file) => {
  console.log('handlePreview 被调用', file)
  previewVisible.value = true
  previewLoading.value = true
  previewError.value = ''
  previewUrl.value = ''
  previewContent.value = ''
  previewType.value = ''
  previewMime.value = ''
  previewName.value = ''
  try {
    const { data } = await axios.get(`/api/auth/files/${file.id}/preview/`, {
      headers: uploadHeaders
    })
    console.log('预览接口返回:', data)
    previewType.value = data.file_type
    previewMime.value = data.mime_type || ''
    previewName.value = data.name || ''
    if (data.file_type === 'image') {
      previewUrl.value = data.preview_url
    } else if (data.file_type === 'text') {
      // 文本内容需要二次请求
      const contentResponse = await axios.get(data.preview_url)
      previewContent.value = contentResponse.data
    } else if (data.file_type === 'document' || data.file_type === 'other') {
      previewUrl.value = data.preview_url
    }
  } catch (error) {
    previewError.value = '预览失败'
  } finally {
    previewLoading.value = false
  }
}

const handleDownload = async (file) => {
  try {
    const { data } = await axios.get(`/api/auth/files/${file.id}/download/`, {
      headers: uploadHeaders
    })
    const link = document.createElement('a')
    link.href = data.download_url
    link.download = data.filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.success('开始下载文件')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const isPdf = computed(() =>
  previewMime.value === 'application/pdf' ||
  (previewName.value && previewName.value.toLowerCase().endsWith('.pdf'))
)
const isOffice = computed(() => {
  const ext = previewName.value.toLowerCase()
  return (
    ext.endsWith('.doc') ||
    ext.endsWith('.docx') ||
    ext.endsWith('.xls') ||
    ext.endsWith('.xlsx') ||
    ext.endsWith('.ppt') ||
    ext.endsWith('.pptx')
  )
})
const officeViewerUrl = computed(() =>
  `https://view.officeapps.live.com/op/view.aspx?src=${encodeURIComponent(previewUrl.value)}`
)
const pdfViewerUrl = computed(() => previewUrl.value)

onMounted(fetchFiles)
</script>
