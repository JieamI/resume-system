import axios from "axios"
import config from "@/config/basic.js"
import store from "@/store"
import router from "@/router"
import { message } from "ant-design-vue"

// 配置全局message
message.config({
    duration: 3,
    maxCount: 1,
})

const service = axios.create({
    baseURL: config.BackendDomain,
    timeout: 5000
})

// const CancelToken = axios.CancelToken
// let cancel

service.interceptors.request.use(
    config => {
        // 取消上一次请求
        // if(typeof cancel === "function") cancel()

        // config.cancelToken = new CancelToken(function executor(c) {
        //     cancel = c
        // })

        // 如果访问的是登录API或加入api则无需拦截
        if((/\/login\/.*/.test(config.url) && config.url !== "/login/update") || /\/join\/.*/.test(config.url)) return config
        // 否则判断store内是否有token，没有则取消请求，重定向至登录页面
        let token = store.state.userInfo["access_token"]
        if (token) {
            config.headers["Authorization"] = `bearer ${token}`
        }else {
        // 如果没有token则取消当前请求并移除本地存储路由到登录页面
            // cancel()
            // window.localStorage.removeItem("userInfo")
            router.push("/superlogin")
        }
    
        return config
    },
    error => {
        console.log(error)
        return Promise.reject(error)
        }
)

service.interceptors.response.use(
response => {
    const res = response.data

    if (res.code !== 0) {
        message.error(res.message || "Error")
        return Promise.reject(new Error(res.message || "Error"))
    } else {
        delete res.code
        return res
    }
},
error => {
    console.log(error.response)
    if(!error.response) {
        message.error("未知错误 请尝试重新登录")
    }else {
        // 否则提示服务器定义的错误
        message.error(error.response.data.detail)
        if(error.response.status == 401) {
            window.localStorage.removeItem("userInfo")
            router.push("/superlogin")
        }
    }
    return Promise.reject(error)
})

export default service
