<template>
    <div class="btn-group">
        <a-button class="btn-action" shape="round" @click="addVisible = true">新增模板</a-button>
        <a-button class="btn-action" shape="round" @click="removeVisible = true">删除模板</a-button>
    </div>
    <my-table 
        :columnSource="columnSource" 
        :dataSource="dataSource" 
        :rowSelection="rowSelection" 
        :height="'calc(100% - 70px)'"
        @click-record="editTemplate">
    </my-table>
    <!-- 增添模板对话框 -->
    <a-modal class="custom-modal" v-model:visible="addVisible" title="新增模板" :centered="true" :width="350">
        <template #footer>
            <a-button @click="addVisible = false" shape="round">取消</a-button>
            <a-button type="primary" @click="addOk" shape="round" :loading="addLoading">确认</a-button>
        </template>
        <label class="label">模板名称</label>
        <input v-model="newTitle" class="title-input" maxlength="8" placeholder="最多不超过8字符" checked/>
        <label class="label">模板内容</label>
        <textarea v-model="newContent" class="area-input" placeholder="请输入模板内容"></textarea>
    </a-modal>
    <!-- 删除模板对话框 -->
    <a-modal class="custom-modal" v-model:visible="removeVisible" title="删除模板" :centered="true" :width="350">
        <template #footer>
            <a-button @click="removeVisible = false" shape="round">取消</a-button>
            <a-button type="primary" @click="removeOk" shape="round" :loading="removeLoading">删除</a-button>
        </template>
        <label class="label">已选模板</label>
        <div class="selected-container">
            <label class="selected-items" v-for="(item, index) in rowSelection.selectedRows.value" :key="index">{{ item.title }}</label>
        </div>
    </a-modal>
    <!-- 模板更新对话框 -->
    <a-modal class="custom-modal" v-model:visible="editVisible" title="编辑模板" :centered="true" :width="350">
        <template #footer>
            <a-button @click="addVisible = false" shape="round">取消</a-button>
            <a-button type="primary" @click="editOk" shape="round" :loading="editLoading">更新</a-button>
        </template>
        <label class="label">模板名称</label>
        <input v-model="updateTitle" class="title-input" maxlength="8" placeholder="最多不超过8字符" checked disabled/>
        <label class="label">模板内容</label>
        <textarea v-model="updateContent" class="area-input" placeholder="请输入模板内容"></textarea>
    </a-modal>
</template>

<script>
import myTable from "@/components/myTable.vue"
import { computed, ref } from "vue"
import { useStore } from 'vuex'
import { message } from "ant-design-vue"

export default {
    components: {
        myTable
    },
    setup() {
        const store = useStore()
        // 数据初始化逻辑
        const dataSource = computed(() => {
            return store.state.deptInfo.mail_template
        })
        
        const columnSource = [{ title: "模板名称", dataIndex: "title"}]

        const rowSelection = {
            selectedRows: []
        }

        // 新增模板逻辑
        const newTitle = ref("")
        const newContent = ref("")
        const addVisible = ref(false)
        const addLoading = ref(false)
        const addOk = () => {
            if(!newTitle.value || !newContent.value) {
                message.warn("内容不能为空")
                addVisible.value = false
                return
            }
            addLoading.value = true
            store.dispatch("addTemplate", { title: newTitle.value, content: newContent.value}).then(() => {
                message.success("模板添加成功")
                addVisible.value = false
                newTitle.value = ""
                newContent.value = ""
            }).finally(() => {
                addLoading.value = false
            })
        }

        // 删除模板逻辑
        const removeVisible = ref(false)
        const removeLoading = ref(false)
        const removeOk = () => {
            if(!rowSelection.selectedRows.value.length) {
                message.warn("至少选中一个模板")
                removeVisible.value = false
                return
            }

            removeLoading.value = true
            let selectedRows = []
            rowSelection.selectedRows.value.forEach(item => {
                selectedRows.push(item.title)
            })
            store.dispatch("removeTemplate", { target: selectedRows }).then(() => {
                message.success("模板删除成功")
                removeVisible.value = false
            }).finally(() => {
                removeLoading.value = false
            })
        }

        // 查看/更新模板逻辑
        const updateTitle = ref("")
        const updateContent = ref("")
        const editVisible = ref(false)
        const editLoading = ref(false)
        const editTemplate = (record) => {
            updateTitle.value = record.title
            updateContent.value = record.content
            editVisible.value = true
        }
        const editOk = () => {
            if(!updateTitle.value || !updateContent.value) {
                message.warn("内容不能为空")
                editVisible.value = false
                return
            }
            editLoading.value = true
            store.dispatch("editTemplate", { title: updateTitle.value, content: updateContent.value }).then(() => {
                message.success("模板更新成功")
                editVisible.value = false
            }).finally(() => {
                editLoading.value = false
            })
        }
        return {
            columnSource,
            dataSource,
            rowSelection,
            newTitle,
            newContent,
            addVisible,
            addLoading,
            addOk,
            removeLoading,
            removeVisible,
            removeOk,
            updateTitle,
            updateContent,
            editVisible,
            editTemplate,
            editOk,
            editLoading
        }
    }
}
</script>

<style lang="stylus" scoped>
    :deep(.grid-box)
        text-align left !important
    .btn-group
        margin 0 16px
        padding 16px 0
        .btn-action
            margin 0 6px
            color rgb(236,255,255)
            background rgb(128,214,249)
            font-weight 550
    .label
        display block
        margin-bottom 10px
        margin-top 20px
    .title-input
        width 100%
    .area-input
        height 200px
        width 100%
    .selected-container
        text-align center
        width 100%
        height 100px
        display flex
        flex-wrap wrap
        align-content flex-start
        overflow auto
        .selected-items
            min-width 70px
            margin 3px
            padding 3px 6px
            color white
            background rgb(129,213,250)
            border-radius 15px
</style>
<style lang="stylus">
.custom-modal
    font-weight 550
    .ant-modal-body
        padding 10px 24px
        padding-top 0
    .ant-modal-footer
        display flex
        justify-content space-between
        .ant-btn
            width 100px
            margin 0 20px
            margin-bottom 10px
        .ant-btn-primary
            background rgb(62,125,191)
</style>