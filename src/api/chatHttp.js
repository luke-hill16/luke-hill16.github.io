import http from './http.js'

const chatWithAI = (message) => {
    const path = "/chat/"
    return http.post(path, { message })
}

export default {
    chatWithAI
} 