<template>
    <!-- <a-skeleton active :paragraph="{ rows: 16 }" :loading="loading"> -->
        <div class="container">
            <div class="selector-area">
                <div class="content">
                    <div class="header">
                        <div>
                            <label style="margin-right:7px">时间段</label>
                            <a-select 
                                style="width:120px;color:rgb(79,203,215)"
                                v-model:value="selected"
                                @select="handleSelected"
                                >
                            <a-select-option :value="value" v-for="(value, index) in selectList" :key="index">{{value}}</a-select-option>
                            </a-select>
                        </div>
                        <span>日投递人数</span>
                    </div>
                    
                    <a-divider style="margin:12px 0"></a-divider>

                    <div class="list-items" v-if="Object.keys(list_data).length">
                        <div class="item" v-for="(value, key) in list_data" :key="key">
                            <span>{{ key }}</span>
                            <span>{{ value }}</span>
                        </div>
                    </div>
                    <div v-else style="display:flex;justify-content:center;align-items:center;height:300px">
                        <a-empty />
                    </div>

                </div>
            </div>

            <div id="pie-area"></div>
            
        </div>
    <!-- </a-skeleton> -->
</template>

<script>
import { onUnmounted, ref } from "vue"
import { getTimeSection, getStatistics } from "@/api/cv"
import * as echarts from 'echarts/core';
import {
    TooltipComponent,
    LegendComponent
} from 'echarts/components';
import {
    PieChart
} from 'echarts/charts';
import {
    CanvasRenderer
} from 'echarts/renderers';

echarts.use(
    [TooltipComponent, LegendComponent, PieChart, CanvasRenderer]
);

export default {
    setup() {
        // const loading = ref(true)
        const myChart = ref()

        const list_data = ref({})
        const pie_data = ref([])
        const option = ref({
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: "vertical",
                top: "60%",
                formatter: name => {
                    let target = pie_data.value.filter(item => {
                        return name == item.name
                    })
                    return `${name}     ${target[0].value}`
                }
            },
            series: [{
                name: '访问来源',
                type: 'pie',
                radius: ["17%", "50%"],
                center: ["50%", "30%"],
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '28',
                        fontWeight: 'bold',
                        formatter: "{d}%"
                    }
                },
                labelLine: {
                    show: true
                },
                data: pie_data.value
            }]
        })
        

        const selectList = ref([])
        const selected = ref("")

        // 更新饼图数据
        const handleSelected = (val) => {
            let year = String(new Date().getFullYear())
            let date = val.split("-")
            getStatistics({
                start: `${year}-${date[0].replace(".", "-")}`,
                end: `${year}-${date[1].replace(".", "-")}`
            }).then(res => {
                let res_pie = res.data.pie_data
                for(let i = 0; i < res_pie.length; i++) {
                    pie_data.value.splice(i, 1, res_pie[i])
                }
                list_data.value = res.data.list_data
                myChart.value.setOption(option.value)
            })
        }

        onUnmounted(() => {
            window.removeEventListener("resize", myChart.value.resize)
        })

        return {
            // loading,
            selected,
            handleSelected,
            selectList,
            list_data,
            myChart,
            option,
            pie_data
        }
    },
    async mounted() {
        // 获取时间段
        let { section } = await getTimeSection()
        if(section.length) {

            this.selectList = section
            this.selected = this.selectList[0]
            
            // 以时间段的第一项初始化饼图数据
            let year = String(new Date().getFullYear())
            let date = this.selected.split("-")
            let { data } = await getStatistics({
                start: `${year}-${date[0].replace(".", "-")}`,
                end: `${year}-${date[1].replace(".", "-")}`
            })
            this.list_data = data.list_data
            for(let i = 0; i < data.pie_data.length; i++) {
                this.pie_data.splice(i, 1, data.pie_data[i])
            }
        }else {
            this.pie_data.push({name: "无数据", value: 0})
        }
        // this.loading = false

        this.$nextTick(() => {
            this.myChart = echarts.init(document.getElementById("pie-area"))
            this.myChart.setOption(this.option)
            window.addEventListener("resize", this.myChart.resize)
        })
        
    }
}
</script>

<style lang="stylus" scoped>
    .container
        height 100%
        display grid
        grid-template-columns 40% 60%
        .selector-area
            padding 100px 60px
            .content
                height 100%
                font-weight 700         
                .header
                    display flex
                    height 40px
                    align-items center
                    justify-content space-between
                .list-items
                    overflow-y auto
                    height 360px
                    .item
                        display flex
                        margin 12px 7px
                        justify-content space-around
                        align-items center
                        height 30px
                        background rgb(245,245,245)
                        border-radius 18px
                        box-shadow 0px 1px 5px 2px rgb(220,220,220)
        // #pie-area
        //     background rgb(16,12,42)
</style>