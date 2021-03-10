<template>
    <div>
        <a-skeleton :loading="loading" :paragraph="{ rows: 16 }" active>
            <a-table :columns="columns" :data-source="data" :pagination="false" :scroll="{ y: 'calc(100vh - 160px)' }">
                <template #rolechange="{ text, record }">
                    <a-button type="primary" shape="round" @click="handleClick(record)">{{ text == "部门负责人"? "移除权限" : "提升权限"}}</a-button>
                </template>
            </a-table>
        </a-skeleton>
    </div>
</template>

<script>
import { ref } from "vue"
import { getAuthInfo, updateAuthority } from "@/api/authority"
import { message } from "ant-design-vue"
export default {
    setup() {
        const loading = ref(true)
        const data = ref()
        const columns = ref()
        getAuthInfo().then(res => {
            data.value = res.data
            
            columns.value = [{
            title: "姓名",
            dataIndex: "nick",
            key: "nick"
        },{
            title: "权限状态",
            dataIndex: "state",
            key: "state",
            filters: [{
                text: "普通成员",
                value: "普通成员"
            }, {
                text: "部门负责人",
                value: "部门负责人"
            }],
            onFilter: (value, record) => record.state === value,
            filterMultiple: false,
            sorter: (a, b) => a.state.length - b.state.length,
            sortDirections: ["descend", "ascend"],
        },{
            title: "所属部门",
            dataIndex: "department",
            key: "department",
            filters: data.value.reduce((pre, item) => {
                !pre.includes(item.department) && pre.push(item.department)
                return pre
            }, []).map((el) => ({
                text: el,
                value: el
            })),
            onFilter: (value, record) => record.department === value
        },{
            title: "权限变更",
            key: "rolechange",
            dataIndex: "state",
            slots: { customRender: "rolechange" }
        }]

            loading.value = false
        })
      
        // 处理按钮点击事件
        const handleClick = (record) => {
            updateAuthority({openid: record.openid}).then(() => {
                message.success("权限更改成功")
                record.state === "普通成员"? record.state = "部门负责人" : record.state = "普通成员"
            })

        }
        return {
            loading,
            data,
            columns,
            handleClick
        }
    }
}
</script>

<style lang="stylus" scoped>


</style>