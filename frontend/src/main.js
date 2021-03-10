import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { 
    Button, 
    Layout, 
    Input, 
    Menu, 
    Divider, 
    Switch, 
    Table, 
    Skeleton, 
    Checkbox, 
    Popover, 
    Select, 
    Modal,
    Rate,
    Empty,
    Upload,
    Comment } from 'ant-design-vue'
import store from './store'

import './permission'

const app = createApp(App)
app.config.productionTip = false
app
.use(Button)
.use(Layout)
.use(Input)
.use(Menu)
.use(Divider)
.use(Switch)
.use(Table)
.use(Skeleton)
.use(Checkbox)
.use(Popover)
.use(Select)
.use(Modal)
.use(Rate)
.use(Empty)
.use(Upload)
.use(Comment)

app.use(router).use(store).mount('#app')

