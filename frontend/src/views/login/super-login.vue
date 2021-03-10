<template>
    <div class="container">
        <div class="main">
            <h1 class="title">超级管理员登录</h1>
            <a-input class="usr-input" v-model:value="usr" placeholder="admin"></a-input>
            <a-input-password class="pwd-input" v-model:value="pwd" placeholder="password" @pressEnter="handleLogin"></a-input-password>
            <a-button class="button" type="primary" shape="round" size="large" @click="handleLogin">立即登录</a-button>
        </div>
        <div class="footer" @click="$router.push('/login')">Token Team ©2021 Created by Token团队 技术部</div>
    </div>
</template>

<script>
import { ref } from "vue"
import { useStore } from "vuex"
import { useRouter } from "vue-router"

export default {
    setup() {
        const usr = ref("")
        const pwd = ref("")

        
        const router = useRouter()
        const store = useStore()
        const handleLogin = () => {
            let form = new FormData()
            form.append("username", usr.value)
            form.append("password", pwd.value)
            store.dispatch("handleSuperLogin", form).then(() => {
                store.commit("GET_USER_INFO")
                router.push("/admin/index")
            })
        }
        return {
            usr,
            pwd,
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
            font-size 36px
            font-family yahei 
            font-weight bold
            margin 30px 0 
        .usr-input
            width 250px
            margin 15px 0
            border-radius 16px
        .pwd-input
            width 250px
            margin 15px 0 
            border-radius 16px

        .button
            width 180px
            margin 30px 0
    .footer
        color gray
        height 30px
        font-weight bold
        text-align center
</style>