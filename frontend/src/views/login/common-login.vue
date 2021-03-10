<template>
    <div class="container">
        <div class="main">
            <h1 class="title">Token 团队招新系统</h1>
            <a-button class="button" type="primary" shape="round" size="large" @click="handleLogin">钉钉扫码登录</a-button>
        </div>
        <div class="footer" @click="$router.push('/superlogin')">Token Team ©2021 Created by Token团队 技术部</div>
    </div>
</template>

<script>
import { useRouter, useRoute } from "vue-router"
import { useStore } from "vuex"
import config from "@/config/basic.js"
export default {
    setup() {
        const router = useRouter()
        const store = useStore()
        store.commit("GET_USER_INFO")
        let userInfo = store.state.userInfo
        if(userInfo) {
            // 如果存在本地用户信息则更新信息
            store.dispatch("handleUpdateInfo", userInfo).then(() => {
                store.commit("GET_USER_INFO")
                router.push("/admin/index")
            })
        }

        const route = useRoute()
        let code = route.query.code
        if(code) {
            store.dispatch("handleCommonLogin", code).then(() => {
                store.commit("GET_USER_INFO")
                router.push("/admin/index")
            })
        }
        
        
        // 点击登录按钮跳转扫码页面
        const handleLogin = () => {
            window.location.href = `https://oapi.dingtalk.com/connect/qrconnect?appid=${config.DingAppId}&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=${config.FrontDomain}/login`
        }
        return {
            handleLogin
        }

    }
   
}
</script>

<style lang="stylus" scoped>

@import "../../style/common.styl"

.container
    width 100%
    height 100%
    display flex
    flex-direction column
    background BACK_COLOR
    .main
        height 100%
        display flex
        flex-direction column
        justify-content center
        align-items center
        padding 10px
        .title
            color gray
            font-size 34px
            font-family yahei 
            font-weight bold
            margin 30px 0 
        .button
            width 180px
            margin 30px 0
    .footer
        color gray
        height 30px
        font-weight bold
        text-align center
</style>