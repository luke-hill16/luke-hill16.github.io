import http from './http'

export default {
  list() {
    return http.get('/api/employee/') // 你的后端接口
  }
}