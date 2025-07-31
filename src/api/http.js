import axios from "axios"
import { useAuthStore } from "@/stores/auth";
import { ElMessage } from "element-plus";
import router from "@/router";

class Http{
    constructor(){
        // 根据环境设置不同的base URL
        const baseURL = import.meta.env.PROD 
          ? 'https://luke-hill16.github.io/api'  // 生产环境
          : 'http://127.0.0.1:8000';  // 开发环境
        
        this.instance=axios.create({
            baseURL: baseURL,
            timeout: 60000
          });
          this.instance.interceptors.request.use((config)=>{
            const authStore =useAuthStore()
            const token = authStore.token
            if(token){
                config.headers.Authorization="JWT "+ token
            }
            
            return config
          })
          
          // 添加响应拦截器
          this.instance.interceptors.response.use(
            (response) => {
              return response;
            },
            (error) => {
              // 处理403错误（token过期）
              if (error.response?.status === 403) {
                const authStore = useAuthStore();
                ElMessage.error('登录已过期，请重新登录');
                authStore.clearUserToken();
                router.push('/login');
              }
              return Promise.reject(error);
            }
          );
    }
    post(path,data){
        //path:/auth/login
        //url :http://127.0.0.1:8000/auth/login
        //return this.instance.post(path,data)
        return new Promise(async (resolve,reject) =>{
            //await:网络请求发送出去后，线程会 挂起 等待
            //等网络数据到达后，线程又会回到当前位置开始往后执行
            //如果在 某个函数中使用了await，那么这个函数就必须要定义成async
            //axios底层也是用的Promise对象，在响应的状态码不是200时，就会调用reject
            // 调用reject的结果是，外层的函数会抛出异常
            try{
                let result=await this.instance.post(path,data)
                console.log(result)
                resolve(result.data);
            }catch(err){
                //alert(err)
                console.log('请求出错:', err)
                let detail = (err.response && err.response.data && err.response.data.detail)
                    ? err.response.data.detail
                    : (err.message || '未知错误');
                //alert(detail);
                reject(detail);
            }
            
        })
    }
    get(path,params){
        return new Promise(async ( resolve,reject)=>{
            try{
                let result= await this.instance.get(path, params)
                resolve(result.data);
            }catch(err){
                console.log('请求出错:', err)
                let detail = (err.response && err.response.data && err.response.data.detail)
                    ? err.response.data.detail
                    : (err.message || '未知错误');
                //alert(detail);
                reject(detail);
            }
        })
    }
}
export default new Http()