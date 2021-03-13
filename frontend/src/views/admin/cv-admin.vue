<template>
    <a-skeleton :loading="loading" :paragraph="{ rows: 16 }" active>
        <div class="btn-group">
            <a-button class="btn-action" shape="round" @click="mailVisible = true" :disabled="!checkPermission({value: ['administrator', 'supervisor']})">发送邮件</a-button>
            <a-button class="btn-action" shape="round" @click="exportVisible = true">导出简历</a-button>
            <a-button class="btn-action" shape="round" @click="removeVisible = true" :disabled="!checkPermission({value: ['administrator', 'supervisor']})">删除简历</a-button>
        </div>
        <my-table 
            :dataSource="data" 
            :columnSource="columns" 
            :rowSelection="rowSelection" 
            :height="'calc(100% - 70px)'"
            @click-record="viewDetails">
            <template #sign="{ record }">
                <div @click.stop="handleSign(record)">
                    <StarFilled v-if="record.sign"/>
                    <StarOutlined v-else/>
                </div>
            </template>

            <template #state="{ record }">
                <a-select 
                    v-model:value="record.state" 
                    @select="handleStateChange(record)" 
                    style="width:100%;" 
                    @click.stop 
                    :disabled="!checkPermission({value: ['administrator', 'supervisor']})">
                    <a-select-option value="未审核">未审核</a-select-option>
                    <a-select-option value="简历通过">简历通过</a-select-option>
                    <a-select-option value="笔试完成">笔试完成</a-select-option>
                    <a-select-option value="面试完成">面试完成</a-select-option>
                    <a-select-option value="已录取">已录取</a-select-option>
                    <a-select-option value="未录取">未录取</a-select-option>
                </a-select>
            </template>

            <template #comment="{ record }">
                <a-button class="btn-comment" shape="round" @click.stop="handleComment(record)">面试评价</a-button>
            </template>
        </my-table>
        <!-- 面试评价对话框 -->
        <a-modal class="custom-modal" v-model:visible="commentVisible" title="面试评价" :centered="true" :width="350">
            <template #footer>
                <a-button @click="commentVisible = false" shape="round">取消</a-button>
                <a-button type="primary" @click="commentOk" shape="round" :loading="commentLoading">确认</a-button>
            </template>
            <label class="custom-label">评价内容</label>
            <textarea class="custom-area" v-model="commentContent"></textarea>
            <a-rate v-model:value="commentScore" />
        </a-modal>
        <a-modal class="custom-modal" v-model:visible="infoVisible" title="简历信息" :centered="true" :width="550">
            <template #footer>
                <a-button @click="infoVisible = false" shape="round">取消</a-button>
                <a-button type="primary" @click="handleSwitch" shape="round">
                    {{ current_page == "info"? "面试评价" : "简历信息"}}
                </a-button>
            </template>
            <div class="info-grid" v-if="current_page == 'info'">
                <div class="base-info">
                    <span>姓名：{{infoRecord.name}}</span>
                    <span>性别：{{infoRecord.sex}}</span>
                    <span>学号：{{infoRecord.sno}}</span>
                    <span>生日：{{infoRecord.birthday}}</span>
                    <span>籍贯：{{infoRecord.hometown}}</span>
                    <span>民族：{{infoRecord.nation}}</span>
                    <span>学院：{{infoRecord.college}}</span>
                    <span>年级：{{infoRecord.grade}}</span>
                    <span>专业班级：{{infoRecord.proclass}}</span>
                    <span>宿舍：{{infoRecord.dormitory}}</span>
                    <span>手机：{{infoRecord.phone}}</span>
                    <span>QQ：{{infoRecord.qq}}</span>
                    <span>邮箱：{{infoRecord.mail}}</span>
                </div>
                <div class="state-info">
                    <span>投递部门：{{infoRecord.department}}</span>
                    <span>简历状态：{{infoRecord.state}}</span>
                    <span>
                        <a-rate v-model:value="averageScore" :disabled="true"/>
                    </span>
                </div>
                <div class="detail-info">
                    <div class="section">
                        <label>自我介绍</label>
                        <div class="textarea">{{infoRecord.introduce}}</div>
                    </div>
                    <div class="section">
                        <label>加入理由</label>
                        <div class="textarea">{{infoRecord.reason}}</div>
                    </div>
                    <div class="section">
                        <label>个人经历</label>
                        <div class="textarea">{{infoRecord.experience}}</div>
                    </div>
                </div>
            </div>
            <div class="comment" v-else-if="current_page == 'comment'">
                <div class="content" v-if="commentList.length">
                    <a-comment v-for="(item, index) in commentList" :key="index">
                        <template #author><a>{{ item.nick }}</a></template>
                        <template #content>
                            <p>{{ item.content }}</p>
                        </template>
                        <template #actions>
                            <a-rate :value="item.score" :disabled="true" />
                        </template>
                    </a-comment>
                </div>
                <div v-else class="empty-content">
                    <a-empty />
                </div>
            </div>
        </a-modal>
        <!-- action处理对话框 -->
        <!-- 删除简历 -->
        <a-modal class="custom-modal" v-model:visible="removeVisible" title="删除模板" :centered="true" :width="350">
            <template #footer>
                <a-button @click="removeVisible = false" shape="round">取消</a-button>
                <a-button type="primary" @click="removeOk" shape="round" :loading="removeLoading">删除</a-button>
            </template>
            <label class="label">已选简历</label>
            <div class="selected-container">
                <label class="selected-items" v-for="(item, index) in rowSelection.selectedRows.value" :key="index">{{ item.name }}</label>
            </div>
        </a-modal>
        <!-- 导出简历 -->
        <a-modal class="custom-modal" v-model:visible="exportVisible" title="导出模板" :centered="true" :width="350">
            <template #footer>
                <a-button @click="exportVisible = false" shape="round">取消</a-button>
                <a-button type="primary" @click="exportOk" shape="round" :loading="exportLoading">导出</a-button>
            </template>
            <label class="label">已选简历</label>
            <div class="selected-container">
                <label class="selected-items" v-for="(item, index) in rowSelection.selectedRows.value" :key="index">{{ item.name }}</label>
            </div>
        </a-modal>
        <!-- 发送邮件 -->
        <a-modal class="custom-modal" v-model:visible="mailVisible" title="发送邮件" :centered="true" :width="350">
            <template #footer>
                <a-button @click="mailVisible = false" shape="round">取消</a-button>
                <a-button type="primary" @click="mailOk" shape="round" :loading="mailLoading">发送</a-button>
            </template>
            <label class="label">已选简历</label>
            <div class="selected-container">
                <label class="selected-items" v-for="(item, index) in rowSelection.selectedRows.value" :key="index">{{ item.name }}</label>
            </div>
            <label class="custom-label">邮件主题</label>
            <input class="custom-input" v-model="mailSubject" />
            <label class="custom-label">邮件内容</label>
            <a-select @select="selectTemplate" style="width:100%;margin-bottom: 10px">
              <a-select-option :value="item.content" v-for="(item, index) in template" :key="index">{{ item.title }}</a-select-option>
            </a-select>
            <textarea class="custom-area" v-model="mailContent"></textarea>
            <div class="upload">
                <a-upload
                    v-model:file-list="fileList"
                    :beforeUpload="beforeUpload">
                    <a-button type="primary">上传</a-button>
                </a-upload>
            </div>
        </a-modal>
    </a-skeleton>
</template>

<script>
import { computed, ref, watchEffect } from "vue"
import myTable from "@/components/myTable.vue"
import { StarOutlined, StarFilled } from "@ant-design/icons-vue"
import { getCvInfo, updateState, updateSign, pushComment, getComment, removeCv, sendEmail } from "@/api/cv"
import { message } from "ant-design-vue"
import checkPermission from "@/directives/permission/index.js"
import { toCsv } from "@/utils/exportExcel.js"
import { useStore } from 'vuex'
// import { useStore } from 'vuex'
// import config from "@/config/basic.js"

export default {
    components: {
        myTable,
        StarOutlined,
        StarFilled
    },
    setup() {
        const loading = ref(true)
        const data = ref()
        const columns = ref()
       
        getCvInfo().then(res => {
            data.value = res.cvList
            columns.value = [{
                title: "姓名",
                dataIndex: "name"
            },{
                title: "标签",
                min_width: "55px",
                dataIndex: "sign",
                filter: [{
                    label: "已标记",
                    value: true
                }, {
                    label: "未标记",
                    value: false
                }],
                onFilter: (record, value) => record.sign == value
                
            },{
                title: "状态",
                dataIndex: "state",
                width: "100px",
                filter: data.value.reduce((pre, item) => {
                    !pre.includes(item.state) && pre.push(item.state)
                    return pre
                }, []).map((el) => ({
                    label: el,
                    value: el
                })),
                onFilter: (record, value) => record.state === value
            },{
                title: "性别",
                dataIndex: "sex",
            },{
                title: "年级",
                dataIndex: "grade",
            },{
                title: "投递部门",
                min_width: "90px",
                dataIndex: "department",
                filter: data.value.reduce((pre, item) => {
                    !pre.includes(item.department) && pre.push(item.department)
                    return pre
                }, []).map((el) => ({
                    label: el,
                    value: el
                })),
                onFilter: (record, value) => record.department === value
            },{
                title: "专业班级",
                dataIndex: "proclass",
            },{
                title: "申请时间",
                dataIndex: "time",
                min_width: "150px"
            },{
                title: "面试评价",
                dataIndex: "comment",
                width: "100px"
            }]
            
            loading.value = false
        })
        
        // 选中状态
        const rowSelection = {
            selectedRows: []
        }
        // 切换简历状态
        const handleStateChange = (record) => {
            updateState({
                sno: record.sno,
                name: record.name,
                state: record.state
            }).then(() => {
                message.success("状态切换成功")
            })
        }

        // 切换简历标记状态
        const handleSign = (record) => {
            if(!checkPermission({
                value: ["administrator", "supervisor"]
            })) {
                message.warn("权限不足")
                return
            }
            updateSign({
                sno: record.sno,
                name: record.name,
                sign: !record.sign
            }).then(() => {
                message.success("标记切换成功")
                record.sign = !record.sign
            })
        }
        
        // 面试评价逻辑
        const commentVisible = ref(false)
        const commentLoading = ref(false)
        const commentContent = ref("")
        const commentScore = ref(3)
        const targetSno = ref("")

        const handleComment = (record) => {
            commentVisible.value = true
            targetSno.value = record.sno
        }

        const commentOk = () => {
            if(!commentContent.value) {
                message.warn("内容不能为空")
                commentVisible.value = false
                return
            }
            commentLoading.value = true
            pushComment({
                sno: targetSno.value,
                content: commentContent.value,
                score: commentScore.value
            }).then(() => {
                message.success("评价提交成功")
                commentLoading.value = false
                commentVisible.value = false
            })
        }

        // 点击简历行查看详细信息
        const infoVisible = ref(false)
        const infoRecord = ref("")
        const averageScore = ref(0)
        const viewDetails = (record) => {
            getComment({
                    sno: record.sno
                }).then(res => {
                    commentList.value = res.data
                    // 计算平均分
                    let total = commentList.value.reduce((pre, item) => {
                        return pre + item.score
                    }, 0)
                    averageScore.value = Math.round(total / commentList.value.length)
                })
            infoRecord.value = record
            infoVisible.value = true
        }
        
        const commentList = ref([])
        const current_page = ref("info")
        // 确保关闭简历信息对话框后current_page的状态为info
        watchEffect(() => {
            if(!infoVisible.value) {
                current_page.value = "info"
            }
        })
        
        // 详情页面试评价逻辑
        const handleSwitch = () => {
            if(current_page.value == "info") {
                current_page.value = "comment"
            }else {
                current_page.value = "info"
            }
        }



        // 删除简历逻辑
        const removeVisible = ref(false)
        const removeLoading = ref(false)
        const removeOk = () => {
            if(!rowSelection.selectedRows.value.length) {
                message.warn("至少选中一个简历")
                removeVisible.value = false
                return
            }
            removeLoading.value = true
            let targetList = []
            let selectedRows = rowSelection.selectedRows.value
            selectedRows.forEach(item => {
                targetList.push({
                    sno: item.sno,
                    name: item.name
                })
            })
            removeCv({ target: targetList }).then(() => {
                for(let item of selectedRows) {
                    let index = data.value.indexOf(item)
                    data.value.splice(index, 1)
                }

                message.success("简历删除成功")
                removeLoading.value = false
                removeVisible.value = false
            })
        }

        // 导出简历逻辑
        const exportVisible = ref(false)
        const exportLoading = ref(false)
        const exportOk = () => {
            if(!rowSelection.selectedRows.value.length) {
                message.warn("至少选中一个简历")
                exportVisible.value = false
                return
            }
            toCsv(rowSelection.selectedRows.value)
            exportVisible.value = false
        }

        // 发送邮件逻辑
        const mailVisible = ref(false)
        const mailLoading = ref(false)
        const mailSubject = ref("")
        const mailContent = ref("")
        const store = useStore()
        const template = computed(() => {
            return store.state.deptInfo.mail_template
        })
        const selectTemplate = (val) => {
            mailContent.value = val
        }
        const fileList = ref([])

        const beforeUpload = (file) => {
            // 限制上传文件数为一个
            if(fileList.value.length !== 0) {
                fileList.value.shift()
            }
            fileList.value.push(file)
            return false
        }
      
        const mailOk = () => {
            if(!rowSelection.selectedRows.value.length) {
                message.warn("至少选中一个简历")
                mailVisible.value = false
                return
            }
            if(!mailSubject.value.trim() || !mailContent.value.trim()) {
                message.warn("内容不能为空")
                return
            }
            mailLoading.value = true
            let selectedRows = rowSelection.selectedRows.value
            let recipients = selectedRows.map(item => {
                return item.mail
            })

            let form = new FormData()
            form.append("content", mailContent.value)
            form.append("subject", mailSubject.value)
            for(let val of recipients) {
                form.append("recipients", val)
            }
            if(fileList.value.length) {
                form.append("file", fileList.value[0])
            }
            
            sendEmail(form).then(() => {
                message.success("邮件发送成功")
                mailLoading.value = false
                mailVisible.value = false
            })
        }

        return {
            data,
            checkPermission,
            columns,
            loading,
            rowSelection,
            handleSign,
            handleComment,
            handleStateChange,
            commentVisible,
            commentContent,
            commentScore,
            commentOk,
            commentLoading,
            handleSwitch,
            current_page,
            commentList,
            viewDetails,
            infoVisible,
            infoRecord,
            averageScore,
            removeVisible,
            removeLoading,
            removeOk,
            exportVisible,
            exportLoading,
            exportOk,
            mailVisible,
            mailLoading,
            selectTemplate,
            template,
            beforeUpload,
            mailOk,
            mailSubject,
            mailContent,
            fileList,
        }
    }
}
</script>

<style lang="stylus" scoped>
    // 上方按钮组样式
    .btn-group
        margin 0 16px
        padding 16px 0
        .btn-action
            margin 0 6px
            color rgb(236,255,255)
            background rgb(128,214,249)
            font-weight 600
    // 邮件发送面板样式
    .upload
        margin-top 14px
    
    // 面试评价样式
    .btn-comment
        color rgb(236,255,255)
        background rgb(128,214,249)
        font-weight 600
    .custom-label
        display block
        margin-top 15px
        margin-bottom 8px
    .custom-input
        width 100%
    .custom-area
        width 100%
        height 150px
    
    // 简历选中模块样式
    .selected-container
        text-align center
        width 100%
        max-height 100px
        display flex
        flex-wrap wrap
        align-content flex-start
        overflow auto
        margin-top 10px
        background rgb(245,245,245)
        .selected-items
            min-width 70px
            margin 3px
            padding 3px 6px
            color white
            background rgb(129,213,250)
            border-radius 15px
    
    // 简历信息模板样式
    .info-grid
        height 500px
        display grid
        margin-top 18px
        font-weight 550
        grid-auto-flow column
        grid-template-columns 40% 60%
        grid-template-rows 80% 20%
        .base-info
            background rgb(242,242,242)
            padding 10px 18px
            display grid
            font-size 12px
            grid-template-rows repeat(autofill, 1fr)
            overflow-y auto
            box-shadow 2px 1px 5px 3px rgb(221,221,221)
        .state-info
            background rgb(242,242,242)
            display grid
            padding 10px 18px
            grid-template-rows 1fr 1fr 1fr
            box-shadow 2px 1px 5px 3px rgb(221,221,221)
        .detail-info
            grid-row 1 / span 2
            display grid
            grid-template-rows 1fr 1fr 1fr
            .section
                margin 0 20px
                label
                    font-size 16px
                    display block
                    background rgb(128,214,249)
                    border-radius 18px
                    padding 3px 12px
                .textarea
                    word-break break-all
                    height 120px
                    padding 10px 12px
                    overflow-y auto
    .comment
        height 500px
        margin-top 18px
        .content
            height 100%
            overflow-y auto
        .empty-content
            height 100%
            display flex
            justify-content center
            align-items center


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