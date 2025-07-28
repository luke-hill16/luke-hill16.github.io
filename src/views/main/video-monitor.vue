<template>
  <div class="video-monitor-container">
    <div class="header-section">
      <h2 class="main-title">hhhhhh监控</h2>
      <div class="header-actions">
        <el-button type="primary" :icon="Refresh" @click="refreshVideos">刷新</el-button>
        <el-button type="primary" :icon="FullScreen" @click="fullscreenMode">全屏</el-button>
      </div>
    </div>
    <div class="main-content">
      <div class="category-sidebar">
        <div class="sidebar-header">
          类别
        </div>
        <div class="category-list">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-item"
            :class="{ active: selectedCategory === category.id }"
            @click="selectCategory(category.id)"
          >
            <el-icon><component :is="category.icon" /></el-icon>
            <span>{{ category.name }}</span>
            <span class="category-badge">{{ category.count }}</span>
          </div>
        </div>
      </div>
      <div class="video-main">
        <div class="video-grid">
          <div v-for="(video, index) in currentVideos" :key="video.id" class="video-item">
            <div class="video-header">
              <h4 class="video-title">{{ video.name }}</h4>
              <div class="video-controls">
                <el-button type="primary" :icon="video.playing ? VideoPause : VideoPlay" @click="toggleVideo(index)" />
                <el-button type="primary" :icon="FullScreen" @click="fullscreenVideo(index)" />
              </div>
            </div>
            <div class="video-container">
              <div class="video-player">
                <el-icon class="video-icon"><VideoCamera /></el-icon>
                <p class="video-status">状态：{{ video.status }}</p>
                <div class="video-info">
                  <div class="info-item">
                    <span class="label">分辨率：</span>
                    <span>{{ video.resolution }}</span>
                  </div>
                  <div class="info-item">
                    <span class="label">帧率：</span>
                    <span>{{ video.fps }}fps</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="video-controls-bar">
              <span class="status-text">当前状态：{{ video.playing ? '播放中' : '已暂停' }}</span>
              <div class="video-controls">
                <el-button type="primary" :icon="video.playing ? VideoPause : VideoPlay" @click="toggleVideo(index)" />
                <el-button type="primary" :icon="FullScreen" @click="fullscreenVideo(index)" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Refresh, FullScreen, VideoCamera, VideoPlay, VideoPause } from '@element-plus/icons-vue'

// 假设类别和视频数据
const categories = [
  { id: 1, name: '变电站', icon: 'VideoCamera', count: 2 },
  { id: 2, name: '输电线路', icon: 'VideoCamera', count: 2 },
  { id: 3, name: '配电房', icon: 'VideoCamera', count: 2 },
  { id: 4, name: '其他', icon: 'VideoCamera', count: 2 }
]
const selectedCategory = ref(1)

const allVideos = [
  // 这里只是模拟数据，实际可从后端获取
  { id: 101, name: '变电站1号', category: 1, status: 'online', resolution: '1080p', fps: 25, playing: true },
  { id: 102, name: '变电站2号', category: 1, status: 'online', resolution: '720p', fps: 20, playing: false },
  { id: 201, name: '输电线路1号', category: 2, status: 'offline', resolution: '1080p', fps: 25, playing: false },
  { id: 202, name: '输电线路2号', category: 2, status: 'online', resolution: '720p', fps: 20, playing: true },
  { id: 301, name: '配电房1号', category: 3, status: 'online', resolution: '1080p', fps: 25, playing: false },
  { id: 302, name: '配电房2号', category: 3, status: 'offline', resolution: '720p', fps: 20, playing: false },
  { id: 401, name: '其他1号', category: 4, status: 'online', resolution: '1080p', fps: 25, playing: false },
  { id: 402, name: '其他2号', category: 4, status: 'online', resolution: '720p', fps: 20, playing: false }
]

const currentVideos = computed(() => {
  // 只显示当前类别的前4个视频
  return allVideos.filter(v => v.category === selectedCategory.value).slice(0, 4)
})

const onlineCount = computed(() => currentVideos.value.filter(v => v.status === 'online').length)

function selectCategory(id) {
  selectedCategory.value = id
}
function refreshVideos() {
  // 实际项目中这里可以重新拉取视频流
}
function fullscreenMode() {
  // 这里可以实现全屏切换
}
function toggleVideo(index) {
  currentVideos.value[index].playing = !currentVideos.value[index].playing
}
function fullscreenVideo(index) {
  // 这里可以实现单个视频全屏
}
function playAll() {
  currentVideos.value.forEach(v => v.playing = true)
}
function pauseAll() {
  currentVideos.value.forEach(v => v.playing = false)
}
function stopAll() {
  currentVideos.value.forEach(v => v.playing = false)
}
</script>

<style scoped>
.video-monitor-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px 10px 30px;
}
.main-title {
  font-size: 22px;
  font-weight: bold;
  color: #303133;
}
.header-actions {
  display: flex;
  gap: 12px;
}
.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.category-sidebar {
  width: 150px;
  background: #fff;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}
.sidebar-header {
  padding: 18px 0 8px 0;
  text-align: center;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #e0e0e0;
}
.category-list {
  flex: 1;
  padding: 10px 0;
}
.category-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  cursor: pointer;
  transition: background 0.2s;
  color: #333;
}
.category-item.active, .category-item:hover {
  background: #e3f2fd;
  color: #409EFF;
}
.category-badge {
  margin-left: auto;
}
.video-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: auto;
}
.video-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 18px;
  flex: 1;
}
.video-item {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  padding: 12px;
  min-width: 0;
}
.video-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.video-title {
  font-weight: bold;
  color: #303133;
}
.video-controls {
  display: flex;
  gap: 6px;
}
.video-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.video-player {
  width: 100%;
  height: 180px;
  background: #222;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-direction: column;
}
.video-icon {
  font-size: 40px;
  margin-bottom: 8px;
}
.video-status {
  font-size: 12px;
  color: #90caf9;
}
.video-info {
  margin-top: 8px;
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
}
.info-item {
  font-size: 13px;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}
.label {
  color: #999;
}
.video-controls-bar {
  margin-top: 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.status-text {
  color: #409EFF;
  font-size: 14px;
}
</style>
