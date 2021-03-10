<template>
    <a-layout id="container">
        <a-layout-sider  
        width="250"
        v-model:collapsed="collapsed"
        breakpoint="lg"
        collapsible>
            <sider></sider>
        </a-layout-sider>
        <a-layout-content style="padding: 20px">
            <router-view v-slot="{ Component }">
                <keep-alive>
                    <component :is="Component" />
                </keep-alive>
            </router-view>
        </a-layout-content>
    </a-layout>
</template>

<script>
import { ref } from 'vue'
import sider from './components/sider.vue'
import { LeftOutlined } from '@ant-design/icons-vue'
import windowAdaptor from './mixin/windowAdaptor.js'
import { useStore } from 'vuex'
export default {
    components: {
        sider,
        LeftOutlined
    },
    mixins: [windowAdaptor],
    setup() {
        const store = useStore()
        store.dispatch("getDeptInfo").then(() => {
            console.log("getDeptInfo")
        })

        const collapsed = ref(false)
        return {
            collapsed
        }
    }
    
}
</script>

<style lang="stylus" scoped>
    .ant-layout
        margin 30px
        height calc(100% - 60px)
        width calc(100% - 60px)
        .ant-layout-sider
            overflow auto
            background #fff
            margin-right 30px
            box-shadow 0 0 16px 5px rgba(0,0,0,0.2)
            perspective 1px // 当子元素设置position: fix时，使该元素为子元素的参照父元素
        .ant-layout-content
            background-color #fff
            box-shadow 0 0 16px 5px rgba(0,0,0,0.2)
            overflow auto
</style>
<style lang="stylus">
    #app
        background rgb(235,235,235)
    .ant-layout-sider-trigger
        color gray
        background initial
</style>
