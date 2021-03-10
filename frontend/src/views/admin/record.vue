<template>
    <div class="container">
        <a-skeleton :paragraph="{ rows: 16 }" :loading="loading" active>
            <div v-if="data.length">
                <div class="card" v-for="(item, index) in data" :key="index">
                    <span class="operator">{{ item.operator }}</span>
                    <span class="operation">{{ item.operation }}</span>
                    <span class="time">{{ item.time }}</span>
                </div>
            </div>
            
            <div class="empty" v-else>
                <a-empty />
            </div>
        </a-skeleton>
    </div>
</template>

<script>
import { ref } from "vue"
import { getRecord } from "@/api/department"
export default {
    setup() {
        const loading = ref(true)
        const data = ref([])
        getRecord().then(res => {
            data.value = res.data
            loading.value = false
             
        })
        return {
            loading,
            data
        }
    }
}
</script>

<style lang="stylus" scoped>
    .container
        width 100%
        height 100%
        overflow auto
        -ms-overflow-style none
        .card
            background rgb(245,245,245)
            border-radius 20px
            margin 16px 14px
            padding 10px 24px
            box-shadow 1px 3px 3px 1px rgb(230,230,230)
            display flex
            justify-content space-between
            span
                display inline-block
                padding 3px 16px
                border-radius 20px
                color white
                font-size 13px
            .operator
                background rgb(129,213,250)
            .operation
                background rgb(255,138,138)
            .time
                background rgb(141,189,68)
        .empty
            height 100%
            display flex
            justify-content center
            align-items center
</style>
<style scoped>
.container::-webkit-scrollbar {  
    display: none;
}
</style>