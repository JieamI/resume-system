import router from "./router"
import NProgress from "nprogress"
import "nprogress/nprogress.css"
import store from "./store"
import { message } from "ant-design-vue"

NProgress.configure({ ease: "ease", showSpinner: false })


function checkPermission(authList) {
    let requestRole = authList
    let haveRole = store.state.userInfo.scopes
  
    for(let i = 0; i < haveRole.length; i++) {
        if(requestRole.indexOf(haveRole[i]) !== -1) return true
    }
    return false 
}


// eslint-disable-next-line no-unused-vars
router.beforeEach((to, from) => {
    NProgress.start()
    if(to.path == "/login" || to.path == "/superlogin" ||  /join.*/.test(to.path)) return true
    
    if(!store.state.userInfo) {
        return { path: "/login" }
    }

    // 路由级权限控制
    if(to.meta.scopes && !checkPermission(to.meta.scopes)) {
        message.error("访问权限受限")
        return { path: "/login" }
    }

    return true
})


router.afterEach(() => {
    NProgress.done()
})