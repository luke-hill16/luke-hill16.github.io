// oafront/src/api/fileHttp.js
import axios from './http'

export function getFilePreview(fileId) {
  console.log('fileId:', fileId)
  return axios.get(`/api/auth/files/${fileId}/preview/`)
}
