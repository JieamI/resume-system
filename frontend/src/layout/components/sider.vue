<template>
    <div class="logo"><span>Token</span> 招新系统</div>
    
    <a-divider></a-divider>

    <div class="info">
        <div class="stress">Hi, {{ nick || "NULL" }}</div>
        <div class="normal">{{ `${role} | ${dept}` || "NUll" }}</div>
        <div class="deptinfo">
            <span class="normal">部门状态：</span>
            <a-switch v-switchPermission="['administrator', 'supervisor']" :checked="show" size="small" @change="handleSwitch"></a-switch>
        </div>
    </div>

    <a-divider></a-divider>

    <a-menu v-model:selectedKeys="selectedKeys" mode="inline">
        <a-menu-item key="1">
            <router-link to="/admin/index">
                <HomeOutlined />
                <span>首页</span>
            </router-link>
        </a-menu-item>
        <a-menu-item key="2">
            <router-link to="/admin/cvadmin">
                <UserOutlined />
                <span>招新简历系统</span>
            </router-link>
        </a-menu-item>
        <a-menu-item key="3">
            <router-link to="/admin/mailtemplate">
                <MailOutlined />
                <span>邮件模板管理</span>
            </router-link>
        </a-menu-item>
        <a-menu-item key="4" :disabled="tab_disabled">
            <router-link to="/admin/setting">
                <SettingOutlined />
                <span>管理员权限设定</span>
            </router-link>
        </a-menu-item>
        <a-menu-item key="5" :disabled="tab_disabled">
            <router-link to="/admin/record">
                <FormOutlined />
                <span>管理员操作记录</span>
            </router-link>
        </a-menu-item>
        <a-menu-item key="6">
            <router-link to="/admin/document">
                <ProfileOutlined />
                <span>使用文档</span>
            </router-link>
        </a-menu-item>

        <a-divider></a-divider>
        
        <a-menu-item class="logout" @click="handleLogout">
            <PoweroffOutlined />
            <span>登出</span>
        </a-menu-item>
    </a-menu>
     

</template>

<script>
import { ref, computed } from "vue"
import { useRouter } from "vue-router" 
import { useStore } from "vuex"
import {
    HomeOutlined,
    UserOutlined,
    MailOutlined,
    SettingOutlined,
    FormOutlined,
    ProfileOutlined,
    PoweroffOutlined
} from "@ant-design/icons-vue"
import { message } from "ant-design-vue"
import { switchPermission } from "@/directives/permission/sider.js"

export default {
    components: {
        HomeOutlined,
        UserOutlined,
        MailOutlined,
        SettingOutlined,
        FormOutlined,
        ProfileOutlined,
        PoweroffOutlined
    },
    directives: { switchPermission },
    setup() {
        const store = useStore()
        
        const show = computed(() => {
            return store.state.deptInfo.show
        })

        // 基本信息获取逻辑
        const nick = computed(() => store.state.userInfo.nick)
        const role = computed(() => store.getters.computeRole)
        const dept = computed(() => store.state.userInfo.department)
        const selectedKeys = ref(["1"])

        // 登出逻辑
        const router = useRouter()
        const handleLogout = () => {
            window.localStorage.removeItem("userInfo")
            router.push("/login/super")
        }

        // 部门状态按钮切换逻辑
        const handleSwitch = (checked) => {
            store.dispatch("updateState", { show: checked }).then(() => {
                message.success("部门状态切换成功")
            })
        }

        // 由于菜单栏无法使用指令进行组件级权限控制，故在此进行边界处理
        const tab_disabled = computed(() => {
            let disabled
            role.value === "普通成员"? disabled = true : disabled = false
            return disabled
        })

        return {
            selectedKeys,
            nick,
            role,
            dept,
            show,
            handleLogout,
            handleSwitch,
            tab_disabled
        }
    }
}
</script>

<style lang="stylus" scoped>
    .logo
        font-size 20px
        text-align left
        padding 10px 20px
        overflow hidden
        white-space nowrap
        span
            display: block
            font-weight: bold
            font-size: 38px
    .ant-divider-horizontal
        margin 14px 18px
        width initial
        min-width  initial
    .info
        text-align left
        padding 0 20px
        white-space nowrap
        overflow hidden
        .stress
            font-size 25px
            color black
        .normal
            font-size 12px
            color gray
        .deptinfo
            white-space normal
            word-break keep-all      
    .ant-menu
        color gray
        .ant-menu-item-selected
            background initial
    .logout
        color black
    .logout::after  // 去除登出菜单的选定样式
        opacity 0
</style>
<style>
.ant-layout-sider::-webkit-scrollbar {
    display: none;
}
</style>
