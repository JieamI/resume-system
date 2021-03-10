<template>
    <div class="mytable">
        <!-- 表格头 -->
        <div class="header grid-box">
            <div class="selection" v-if="rowSelection" @click.stop="onChangeAll">
                <IconFont type="icon-xuanze" v-if="selectedAll"/>
                <IconFont type="icon-weixuan" v-else/>
            </div>
            
            <div v-for="(item, index) in $props.columnSource" :key="index">
                <span>{{ item.title }}</span>
                <a-popover v-if="item.filter && item.onFilter" :visible="item.visible" @click="item.visible = !item.visible" placement="bottom">
                    <template #content>
                        <a-checkbox-group v-model:value="item.selectedValue" :options="item.filter" style="display:flex;flex-direction:column;"></a-checkbox-group>
                        <div style="display:flex;justify-content:space-evenly;margin-top:8px">
                            <a @click="handleFilter(item)">确定</a><a @click="resetFilter(item)">重置</a>
                        </div>
                        
                    </template>
                    <DownOutlined style="margin-left: 8px"/>
                </a-popover>
            </div>
        </div>
        <!-- 表格体 -->
        <!-- 如果存在数据则渲染表格 -->
        <ul class="list-items" v-if="$props.dataSource.length">
            <li class="list-item grid-box" v-for="(item, index) in filteredData" :key="index" @click="$emit('click-record', item)">
                <div class="selection" v-if="rowSelection" @click.stop="onChange(item)">
                    <IconFont type="icon-xuanze" v-if="item.selected"/>
                    <IconFont type="icon-weixuan" v-else/>
                </div>

                <div v-for="(column, index) in $props.columnSource" :key="index">
                    <slot :name="column.dataIndex" v-if="$slots[column.dataIndex]" :record="item"></slot>
                    <span v-else>{{ item[column.dataIndex] }}</span>
                </div>
            </li>
        </ul>
        <!-- 否则则渲染为空状态 -->
        <div class="empty" v-else>
            <a-empty />
        </div>

    </div>
</template>

<script>
import { computed, nextTick, ref, onActivated } from "vue"
import { DownOutlined } from "@ant-design/icons-vue"
import { createFromIconfontCN } from '@ant-design/icons-vue'
const IconFont = createFromIconfontCN({
  scriptUrl: "//at.alicdn.com/t/font_2384222_f2a5b4gnpgr.js"
});
export default {
    props: {
        dataSource: Array,
        columnSource: Array,
        rowSelection: Object,
        height: String
    },
    components: {
        DownOutlined,
        IconFont
    },
    emits: ["click-record"],
    setup(props) {   
        // 过滤器配置处理
        props.columnSource.map(item => {
            if(item.filter && item.onFilter) {
                item.visible = false
                item.selectedValue = []
            }
            return item
        })
        
        // 当前激活的过滤项
        const current_item = ref(null)

        const filteredData = computed(() => {
            if(!current_item.value) return props.dataSource
            else {
                return props.dataSource.filter(record => {
                    for(let value of current_item.value.selectedValue) {
                        if(current_item.value.onFilter(record, value)) {
                            return true
                        }
                    }
                    return false
                })
            }
        })

        // 过滤器处理
        const handleFilter = (item) => {
            current_item.value = item
            item.visible = false
        }

        // 重置过滤器
        const resetFilter = (item) => {
            current_item.value = null
            item.visible = false
        }
        
        // 如果配置了可选，则在对象中添加不可迭代的选择列
        if(props.rowSelection) {
            props.dataSource.map(item => {
                Object.defineProperty(item, "selected", {
                    value: false,
                    writable: true,
                    enumerable: false,
                    configurable: true
                })
                return item
            })
        }

        // 全选状态
        const selectedAll = ref(false)

        // 获取选中的行记录
        // eslint-disable-next-line vue/no-mutating-props
        props.rowSelection.selectedRows = computed(() => {
            return props.dataSource.filter((item) => {
                return item.selected
            })
        })
       
        // 选择点击事件处理
        const onChange = (item) => {
            if(item.selected) {
                item.selected = false
                selectedAll.value = false
            }else {
                item.selected = true
                if(!filteredData.value.some(item => {
                    return !item.selected
                })) {
                    selectedAll.value = true
                }
            }
        }
        
        // 全选点击事件处理
        const onChangeAll = () => {
            if(selectedAll.value) {
                filteredData.value.forEach((item) => {
                    item.selected = false
                })
            }else {
                filteredData.value.forEach((item) => {
                    item.selected = true
                })
            }
            selectedAll.value = !selectedAll.value
        }

        // 在dom更新后根据height, columnSource配置网格布局策略
        const renderGridLayOut = () => {
            if(props.height && typeof props.height == "string") {
                let ul = document.querySelector(".mytable")
                ul.setAttribute("style", `height: ${props.height}`)
            }
            
            let valueList = []
            // 如果配置了可选，设定选项列宽度为20px
            if(props.rowSelection) valueList.push("20px")
            
            // 如果columnSource中配置了列的宽度则设置宽度，否则默认为比例宽度1fr
            for(let item of props.columnSource) {
                if(item.width) {
                    valueList.push(item.width);continue
                }
                item.min_width && item.max_width? valueList.push(`minmax(${item.min_width}, ${item.max_width})`) :
                item.min_width? valueList.push(`minmax(${item.min_width}, 1fr)`) :
                item.max_width? valueList.push(`minmax(auto, ${item.max_width})`) :
                valueList.push("1fr")
            }

            let styleNode = document.createElement("style")
            styleNode.innerHTML = `.grid-box { grid-template-columns: ${valueList.join(" ")}}`
            document.querySelector("head").appendChild(styleNode)
        }
        nextTick(renderGridLayOut)
        onActivated(renderGridLayOut)
        return {
            filteredData,
            selectedAll,
            onChange,
            onChangeAll,
            handleFilter,
            resetFilter
        }
    }
}
</script>

<style lang="stylus" scoped>
    .selection
        cursor pointer
    .mytable
        font-weight 550
        height 100%
        margin 0 16px
        .header
            display grid
            align-items center
            padding 0 36px
            box-shadow 0px 1px 8px 3px rgb(220,220,220)
            height 60px
            text-align center
        .list-items
            padding-left 0
            height calc(100% - 60px)
            margin-bottom 0
            padding 0 16px
            overflow-y auto
            overflow-x hidden
            .list-item
                display grid
                align-items center
                list-style none
                background rgb(245,245,245)
                border-radius 18px
                box-shadow 0px 1px 5px 2px rgb(220,220,220)
                margin 20px 0
                padding 0 20px
                height 50px
                transition transform 0.3s
                text-align center
            .list-item:hover
                transform scale(1.02)
        .empty
            height calc(100% - 60px)
            display flex
            justify-content center
            align-items center
        
</style>
<style>
.list-items::-webkit-scrollbar {
    display: none;
}
</style>